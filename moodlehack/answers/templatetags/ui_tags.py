import json

from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.inclusion_tag("answers/includes/_modal_answer_delete.html")
def render_confirm_answer_delete(
    modal_id="deleteAnswerModal", object_id=None, mode="default"
):
    """
    Renders a specialized modal for answer deletion.
    'default' mode: standard redirect.
    'api' mode: inline removal.
    """
    return {
        "modal_id": modal_id,
        "mode": mode,
        "object_id": object_id,
    }


@register.inclusion_tag(
    "answers/includes/_toast_messages.html", takes_context=True
)
def render_notifications(context):
    """
    Renders the notification container and prepares messages for the JS handler
    If a message indicates a deletion, it forces the 'danger' tag
    for visual consistency.
    """
    messages = context.get("messages", [])
    msg_list = []

    for m in messages:
        text = str(m)
        tags = m.tags if m.tags else ""

        # Hardcoded check for deletion message to ensure 'danger' styling
        if text == "Ответ успешно удален!":
            tags = "danger"

        msg_list.append({"text": text, "tags": tags})

    return {
        "initial_messages_json": mark_safe(json.dumps(msg_list)),
    }
