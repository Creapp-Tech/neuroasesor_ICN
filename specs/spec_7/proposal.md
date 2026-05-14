# Spec 7 — whatsapp_client.py + manychat_client.py: Clientes de Canales

## Qué resuelve
Implementa los clientes de comunicación con WhatsApp Business API y ManyChat. WhatsApp es el canal principal de conversación clínica 24/7. ManyChat es el panel operativo del Neuroasesor y canal de preclasificación. Incluye verificación HMAC del webhook de WhatsApp.

## Por qué es necesaria
El documento (Sección 4, V6 Documento 1) define WhatsApp como canal principal con webhook permanente y verificación HMAC. ManyChat sincroniza estados de contacto, gestiona etiquetas (nuevo, en orientación, agendado, escalado, cerrado) y asigna conversaciones al Neuroasesor en escalamientos.

## Qué entrega
- `whatsapp_client.py`: funciones para enviar mensajes, parsear webhook entrante, verificar firma HMAC.
- `manychat_client.py`: funciones para actualizar estado/etiquetas del contacto, asignar conversación a humano, marcar conversación como 'vencida' (SLA incumplido).
