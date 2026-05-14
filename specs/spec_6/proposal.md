# Spec 6 — phase_router.py + prompts/: Enrutador de Fases y Prompts Versionados

## Qué resuelve
Implementa la lógica de transición entre fases F0→F1→F2→F3→F4→HUMANO/ADMIN y los prompts versionados por fase. El enrutador selecciona el prompt correcto según `fase_actual` del paciente y aplica las reglas de transición. Los prompts son archivos de texto versionados, no strings hardcodeados en código.

## Por qué es necesaria
El documento (Secciones 6, 14-20, 10) define las fases MVP: F0, F1, F2, F3, F4, ADMIN y HUMANO, cada una con su propio prompt y reglas de transición. La regla F3 obligatoria, el manejo de EPS→ADMIN y la detección de escalamiento comercial en F4 son lógica de negocio crítica que debe estar en Python, no en el LLM.

## Qué entrega
- `phase_router.py`: clase `PhaseRouter` con método `get_next_phase(paciente, response_ia, score_result) -> str` y `get_system_prompt(fase: str, paciente: Paciente) -> str`.
- `prompts/`: directorio con archivos `f0_v6.txt`, `f1_v6.txt`, `f2_v6.txt`, `f3_v6.txt`, `f4_v6.txt`, `admin_v6.txt`, `humano_v6.txt` con el contenido de cada prompt según V6/V5 del documento.
