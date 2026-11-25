from django.conf import settings

from .turn_suggestions import TurnSuggestionsViewSet

__all__ = ["TurnSuggestionsViewSet"]

if settings.EE_AVAILABLE:
    from .mcp_tools import MCPToolsViewSet as MCPToolsViewSet

    __all__.append("MCPToolsViewSet")
