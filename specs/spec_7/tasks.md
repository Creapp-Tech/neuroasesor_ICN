# Tasks — Spec 7: whatsapp_client.py + manychat_client.py

- [ ] Implementar `whatsapp_client.py` función `send_message(to: str, text: str) -> bool`: POST a WhatsApp Cloud API con token de config; retornar True si 200 OK
- [ ] Implementar `parse_webhook(payload: dict) -> tuple[str, str, str]`: extraer (numero_telefono, mensaje_texto, timestamp) del cuerpo JSON del webhook de WhatsApp Business API
- [ ] Implementar `verify_hmac(payload_raw: bytes, signature_header: str) -> bool`: verificar firma X-Hub-Signature-256 usando `config.WHATSAPP_WEBHOOK_SECRET`
- [ ] Implementar `manychat_client.py` función `update_contact_tag(telefono: str, tag: str) -> bool`: actualizar etiqueta del contacto en ManyChat (valores válidos: "nuevo", "en_orientacion", "agendado", "escalado", "cerrado")
- [ ] Implementar `assign_to_human(telefono: str, prioridad: str) -> bool`: asignar conversación al agente humano en ManyChat con campo de prioridad
- [ ] Implementar `mark_as_vencida(telefono: str) -> bool`: marcar conversación como vencida por incumplimiento de SLA
