#!/usr/bin/env python3
"""Local conversation tester for NeurOrientador.

Run from the project root:
    python chat.py

The Gemini API key must be set in .env (GEMINI_API_KEY=...).
No WhatsApp or Twilio required — messages are entered directly in the terminal.
Conversation turns are logged to Supabase if the tables exist; errors are silently swallowed.
"""

import sys
import os

# Ensure the project root is on the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.alarm_filter import check_alarm
from app.audit_log import log_turno, update_historial
from app.json_guard import parse_and_validate
from app.llm_client import LLMClient
from app.phase_router import PhaseRouter
from app.scoring import process_f3_scoring
from app.schemas import Paciente

SEPARADOR = "─" * 60

MENSAJES_TERMINAL = {
    "HUMANO": (
        "Estamos conectándote con un especialista del equipo ICN Salud. "
        "En breve te contactarán. Cuídate mucho."
    ),
    "ADMIN": (
        "Para consultas sobre autorizaciones y trámites EPS, visita "
        "icnsalud.com o comunícate con nuestra línea administrativa."
    ),
}


def _imprimir_encabezado(paciente: Paciente) -> None:
    print(SEPARADOR)
    print("  NeurOrientador ICN Salud — Prueba Local")
    print(SEPARADOR)
    print(f"  Paciente : {paciente.paciente_id}")
    print(f"  Teléfono : {paciente.telefono}")
    print(f"  Fase     : {paciente.fase_actual}")
    print(SEPARADOR)
    print("  Escribe tu mensaje y presiona Enter.")
    print("  Escribe 'salir' para terminar la sesión.")
    print(SEPARADOR)
    print()


def run_conversation() -> None:
    paciente = Paciente(
        paciente_id="PAC-LOCAL-001",
        telefono="local_test",
        fase_actual="F0",
    )

    router = PhaseRouter()

    try:
        llm = LLMClient()
    except Exception as e:
        print(f"Error al inicializar el LLM: {e}")
        print("Verifica que GEMINI_API_KEY esté configurado en .env")
        sys.exit(1)

    _imprimir_encabezado(paciente)

    turno_en_f4 = 0

    while True:
        try:
            user_input = input(f"[{paciente.fase_actual}] Tú: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n\nSesión interrumpida.")
            break

        if not user_input:
            continue

        if user_input.lower() in ("salir", "exit", "quit"):
            print("\nConversación terminada. ¡Hasta pronto!")
            break

        # ── 1. Filtro de alarmas ──────────────────────────────────────────────
        alarm_detected, keyword = check_alarm(user_input)
        if alarm_detected:
            print()
            print("  ⚠  ALARMA DETECTADA")
            print()
            print(
                "NeurOrientador: Detectamos una situación de emergencia. "
                "Por favor llama al 123 o acude a urgencias de inmediato. "
                "Nuestro equipo médico ha sido notificado."
            )
            print()
            break

        # ── 2. Prompt del sistema para la fase actual ─────────────────────────
        system_prompt = router.get_system_prompt(paciente.fase_actual, paciente)

        # ── 3. Llamada al LLM ─────────────────────────────────────────────────
        print()
        try:
            raw_response, tokens_usados = llm.call(
                system_prompt, paciente.historial_json, user_input
            )
        except Exception as e:
            print(f"  [Error LLM: {e}]")
            print()
            continue

        # ── 4. Validación JSON ────────────────────────────────────────────────
        error_json = False
        score_result = None
        response_ia = parse_and_validate(raw_response)

        if response_ia is None:
            error_json = True
            respuesta_visible = (
                "[Error interno al procesar la respuesta. "
                "Un especialista te atenderá en breve.]"
            )
            print(f"NeurOrientador: {respuesta_visible}")
        else:
            respuesta_visible = response_ia.respuesta_visible
            print(f"NeurOrientador: {respuesta_visible}")

            # ── 5. Scoring (solo en F3) ───────────────────────────────────────
            if paciente.fase_actual == "F3":
                score_result = process_f3_scoring(response_ia.puntaje_dominio)
                nivel = score_result.get("nivel_riesgo", "")
                score = score_result.get("score_total", 0)
                print(f"  [Score: {score} | Riesgo: {nivel}]")

        # ── 6. Siguiente fase ─────────────────────────────────────────────────
        if paciente.fase_actual == "F4":
            turno_en_f4 += 1
        else:
            turno_en_f4 = 0

        next_phase = router.get_next_phase(
            paciente, response_ia, score_result, error_json,
            turno_en_f4=turno_en_f4,
        )

        if next_phase != paciente.fase_actual:
            print(f"  [Transición: {paciente.fase_actual} → {next_phase}]")

        # ── 7. Actualizar historial y estado ──────────────────────────────────
        paciente.historial_json = update_historial(paciente, user_input, respuesta_visible)

        if score_result:
            paciente.nivel_riesgo = score_result.get("nivel_riesgo")
            paciente.score_total = score_result.get("score_total", 0)

        fase_anterior = paciente.fase_actual
        paciente.fase_actual = next_phase  # type: ignore[assignment]

        # ── 8. Log a Supabase (silencia errores) ──────────────────────────────
        log_turno(
            paciente_id=paciente.paciente_id,
            telefono=paciente.telefono,
            fase=fase_anterior,
            mensaje_usuario=user_input,
            respuesta_agente=respuesta_visible,
            guia_soporte_turno=response_ia.guia_soporte if response_ia else None,
            tokens_usados=tokens_usados if not error_json else 0,
            flag_alarma=alarm_detected,
            escalado_humano=(next_phase == "HUMANO"),
            version_prompt="v6.0",
        )

        print()

        # ── 9. Estados terminales ─────────────────────────────────────────────
        if next_phase in MENSAJES_TERMINAL:
            print(f"NeurOrientador: {MENSAJES_TERMINAL[next_phase]}")
            print()
            break


if __name__ == "__main__":
    run_conversation()
