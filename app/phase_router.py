import json
import os
from typing import Optional

from app.schemas import Paciente, ResponseIA


class PhaseRouter:
    """Handles phase transitions and system prompt generation."""

    def __init__(self, prompts_dir: str = "app/prompts"):
        if os.path.isabs(prompts_dir):
            self.prompts_dir = prompts_dir
        else:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            self.prompts_dir = os.path.join(base_dir, "app", "prompts")

    def _load_prompt_file(self, filename: str) -> str:
        path = os.path.join(self.prompts_dir, filename)
        try:
            with open(path, "r", encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            return ""

    def _parse_notas(self, notas: Optional[str]) -> dict:
        """Try to parse notas_internas as JSON. Falls back to empty dict."""
        if not notas:
            return {}
        try:
            result = json.loads(notas)
            return result if isinstance(result, dict) else {}
        except (json.JSONDecodeError, ValueError):
            return {}

    def get_system_prompt(self, fase: str, paciente: Paciente) -> str:
        """
        Combines base prompt with phase-specific prompt and injects patient data.
        fase_actual and nivel_riesgo are plain strings (Literal), not Enums.
        """
        base_prompt = self._load_prompt_file("base_v6.txt")
        phase_prompt = self._load_prompt_file(f"{fase.lower()}_v6.txt")
        full_prompt = f"{base_prompt}\n\n{phase_prompt}"

        replacements = {
            "{{nombre}}": paciente.nombre or "paciente",
            "{{edad}}": str(paciente.edad) if paciente.edad is not None else "no especificada",
            "{{ciudad}}": paciente.ciudad or "no especificada",
            "{{aseguramiento}}": paciente.aseguramiento or "no especificado",
            "{{fase_actual}}": paciente.fase_actual,           # str, no .value
            "{{programa_clinico}}": paciente.programa_clinico or "ninguno",
            "{{nivel_riesgo}}": paciente.nivel_riesgo or "no evaluado",  # str, no .value
            "{{fenotipo_probable}}": paciente.fenotipo_probable or "no determinado",
            "{{cie10}}": paciente.cie10 or "N/A",
        }

        for placeholder, value in replacements.items():
            full_prompt = full_prompt.replace(placeholder, value)

        return full_prompt

    def get_next_phase(
        self,
        paciente: Paciente,
        response_ia: Optional[ResponseIA],
        score_result: Optional[dict],
        error_json: bool,
        turno_en_f4: int = 0,
    ) -> str:
        """
        Determines the next phase using backend logic only — never the LLM.

        Priority order:
        1. error_json persistente → HUMANO
        2. score_result (F3 completada) → usar fase_siguiente del scorer
        3. notas_internas tipo=admin → ADMIN
        4. notas_internas requiere_escalamiento_humano → HUMANO
        5. notas_internas requiere_neuroasesor_comercial → HUMANO
        6. turno_en_f4 >= 3 sin conversión → HUMANO
        7. Flujo lineal normal
        """
        current_phase: str = paciente.fase_actual  # already a str

        # 1. JSON persistentemente inválido → derivar a humano
        if error_json:
            return "HUMANO"

        # 2. F3 completada: el scorer ya calculó la siguiente fase
        if score_result:
            return score_result.get("fase_siguiente", "F4")

        # 3-5. Leer notas_internas del modelo con doble estrategia:
        #      primero JSON, luego texto libre como fallback
        if response_ia:
            notas_data = self._parse_notas(response_ia.notas_internas)
            notas_lower = (response_ia.notas_internas or "").lower()

            # 3. Caso administrativo (EPS, autorizaciones)
            if notas_data.get("tipo") == "admin" or "tipo=admin" in notas_lower or "tipo: admin" in notas_lower:
                return "ADMIN"

            # 4. Señal clínica o emocional grave
            if notas_data.get("requiere_escalamiento_humano") is True or "requiere_escalamiento_humano=true" in notas_lower:
                return "HUMANO"

            # 5. Escalamiento comercial explícito
            if notas_data.get("requiere_neuroasesor_comercial") is True or "requiere_neuroasesor_comercial=true" in notas_lower:
                return "HUMANO"

        # 6. F4 con 3+ turnos sin conversión → Neuroasesor humano
        if current_phase == "F4" and turno_en_f4 >= 3:
            return "HUMANO"

        # 7. Flujo lineal normal
        if current_phase == "F0":
            return "F1"

        if current_phase == "F1":
            datos_completos = (
                paciente.nombre
                and paciente.edad is not None
                and paciente.consentimiento_datos_clinicos
            )
            return "F2" if datos_completos else "F1"

        if current_phase == "F2":
            # Avanzar a F3 cuando el paciente seleccionó un problema
            if paciente.programa_clinico:
                return "F3"
            return "F2"

        # F3 → manejado por score_result (regla 2 arriba)
        # F4, ADMIN, HUMANO → sin transición automática
        return current_phase
