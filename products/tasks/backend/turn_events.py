"""Turn completion events shared with the agent proxy's side-effects.ts."""

TURN_COMPLETE_METHOD = "_posthog/turn_complete"
BACKGROUND_TURN_COMPLETE_METHOD = "_posthog/background_turn_complete"
STOP_REASON_END_TURN = "end_turn"
PI_RUNTIME_ERROR_MESSAGE = "The agent runtime failed during this turn."


def _notification(event: dict) -> dict:
    notification = event.get("notification")
    return notification if event.get("type") == "notification" and isinstance(notification, dict) else {}


def _pi_turn(event: dict) -> dict:
    turn = event.get("event")
    if event.get("type") == "pi_event" and isinstance(turn, dict) and turn.get("type") == "turn_completed":
        return turn
    return {}


def _payload(notification: dict) -> dict:
    field = (
        "params" if notification.get("method") in (TURN_COMPLETE_METHOD, BACKGROUND_TURN_COMPLETE_METHOD) else "result"
    )
    value = notification.get(field)
    return value if isinstance(value, dict) else {}


def is_turn_complete(event: dict) -> bool:
    notification = _notification(event)
    if _pi_turn(event) or notification.get("method") == TURN_COMPLETE_METHOD:
        return True
    result = notification.get("result")
    return isinstance(result, dict) and result.get("stopReason") == STOP_REASON_END_TURN


def is_background_turn_complete(event: dict) -> bool:
    return _notification(event).get("method") == BACKGROUND_TURN_COMPLETE_METHOD


def pi_turn_error(event: dict) -> bool:
    return _pi_turn(event).get("stopReason") == "error"


def turn_completed_successfully(event: dict) -> bool:
    if not is_turn_complete(event):
        return False
    payload = _pi_turn(event) or _payload(_notification(event))
    return payload.get("stopReason") == STOP_REASON_END_TURN


def is_idle_resume_turn_complete(event: dict) -> bool:
    notification = _notification(event)
    return (
        notification.get("method") == TURN_COMPLETE_METHOD and _payload(notification).get("stopReason") == "idle_resume"
    )


def turn_complete_trace_id(event: dict) -> str | None:
    payload = _pi_turn(event) or _payload(_notification(event))
    trace_id = payload.get("traceId")
    if not trace_id and isinstance(metadata := payload.get("_meta"), dict):
        trace_id = metadata.get("traceId")
    return trace_id if isinstance(trace_id, str) and trace_id else None
