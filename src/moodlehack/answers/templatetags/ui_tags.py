import json

from django import template
from django.utils.safestring import mark_safe
from django.utils.translation import gettext as _

register = template.Library()


@register.inclusion_tag("answers/includes/_modal_answer_delete.html")
def render_confirm_answer_delete(
    modal_id="deleteAnswerModal", object_id=None, mode="default"
):
    """
    Renders a specialized modal for answer deletion with translated labels.
    """
    ui_labels = {
        "title": _("Delete Confirmation"),
        "record_label": _("Record #"),
        "question": _("Are you sure you want to delete this answer?"),
        "warning_text": _("This action cannot be undone."),
        "cancel_btn": _("Cancel"),
        "confirm_btn": _("Delete"),
        # Messages for the JS handler (API mode)
        "msg_success": _("Answer successfully deleted!"),
        "msg_error_prefix": _("Server error"),
        "msg_network_error": _("Network error or server unavailable"),
    }

    return {
        "modal_id": modal_id,
        "mode": mode,
        "object_id": object_id,
        "ui": ui_labels,
    }


@register.inclusion_tag(
    "answers/includes/_toast_messages.html", takes_context=True
)
def render_notifications(context):
    """
    Prepares notifications with translated UI strings for the JS handler.
    Automatically forces 'danger' tag for deletion messages to maintain
    visual consistency across languages.
    """
    messages = context.get("messages", [])
    msg_list = []

    # Translated labels for the toast UI
    ui_labels = {
        "title_success": _("Success"),
        "title_danger": _("Deletion"),
        "title_warning": _("Warning"),
        "title_info": _("Notification"),
        "time_just_now": _("just now"),
        "time_sec": _("sec. ago"),
        "time_min": _("min. ago"),
    }

    # Targeted translation for the deletion success message
    del_msg_translated = _("Answer successfully deleted!")

    for m in messages:
        text = str(m)
        tag = m.level_tag

        # Force 'danger' tag if it's a deletion message (i18n safe)
        # or if the message already has a danger/error level
        if text == del_msg_translated or "danger" in m.tags or m.level >= 40:
            tag = "danger"

        msg_list.append({"text": text, "tags": tag})

    return {
        "initial_messages_json": mark_safe(json.dumps(msg_list)),
        "ui_labels_json": mark_safe(json.dumps(ui_labels)),
    }
