"""Import viewsets on demand so reading ticket filters does not start workflow modules."""

from importlib import import_module
from typing import Any

_VIEW_MODULES = {
    "AIContextAccountPropertiesViewSet": "ai_context",
    "AIReplyPlaybookViewSet": "ai_reply_playbook",
    "IntercomImportViewSet": "intercom_import",
    "PylonImportViewSet": "pylon_import",
    "SigningSecretViewSet": "signing_secret",
    "TicketMacroViewSet": "ticket_macros",
    "TicketViewSet": "tickets",
    "TicketViewViewSet": "ticket_views",
    "WidgetMessageView": "widget",
    "WidgetMessagesView": "widget",
    "WidgetTicketsView": "widget",
    "ZendeskImportViewSet": "zendesk_import",
}

__all__ = list(_VIEW_MODULES)


def __getattr__(name: str) -> Any:
    if name not in _VIEW_MODULES:
        raise AttributeError(name)
    return getattr(import_module(f"{__name__}.{_VIEW_MODULES[name]}"), name)
