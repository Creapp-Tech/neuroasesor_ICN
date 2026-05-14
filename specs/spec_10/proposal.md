# Spec 10 — neuroasesor_service.py + daily_reports.py: Servicio del Neuroasesor y Reportes Diarios

## Qué resuelve
Implementa el registro de intervenciones directas del Neuroasesor (NEUROASESOR_INTERACCIONES) y la generación automática del resumen diario del NeuroAsistente que se envía al Neuroasesor a las 8:00 PM hora Colombia, lunes a sábado. Incluye las métricas consolidadas del día.

## Por qué es necesaria
El documento (Secciones 16-17, V6 Documentos 3-5) define que TODO lo que haga el Neuroasesor debe quedar registrado en NEUROASESOR_INTERACCIONES. El resumen diario se genera automáticamente por el sistema con Gemini y se envía al final de la jornada. Sin estos módulos, la supervisión del NeuroAsistente no puede operarse.

## Qué entrega
- `neuroasesor_service.py`: funciones para registrar intervenciones del Neuroasesor, detectar oportunidades comerciales y clínicas.
- `daily_reports.py`: generación del resumen diario del NeuroAsistente (filtrar NEUROASISTENTE_INTERACCIONES del día, calcular métricas, generar resumen narrativo con LLM, enviar al Neuroasesor, insertar en RESUMENES_DIARIOS).
