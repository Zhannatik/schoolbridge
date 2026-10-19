from mcp.server.fastmcp import FastMCP

from schoolbridge import llm, notices, store

mcp = FastMCP("school-bridge", host="127.0.0.1", port=8000)
store.init()


@mcp.tool()
async def set_language(language: str) -> dict:
    """Set the parent's language: 'en', 'ru' or 'kk' (Kazakh)."""
    if language not in notices.LANGS:
        return {"status": "error", "reason": f"Supported languages: {', '.join(notices.LANGS)}"}
    store.set_setting("language", language)
    return {"status": "ok", "language": language}


@mcp.tool()
async def add_child(name: str, grade: str = "") -> dict:
    """Register a child so notices and tasks can be linked to them."""
    name = name.strip()[:60]
    if not name:
        return {"status": "error", "reason": "Name is empty"}
    store.add_child(name, grade.strip()[:20] or None)
    return {"status": "ok", "children": store.list_children()}


@mcp.tool()
async def add_notice(text: str, child_name: str = "") -> dict:
    """Read a school message, explain it in the parent's language and save the tasks it contains."""
    child = child_name.strip() or None
    if child and not store.child_exists(child):
        return {"status": "error", "reason": f"Unknown child: {child}. Use add_child first."}
    language = store.get_setting("language", "en")
    try:
        summary, actions = await notices.analyze(text, language)
    except (llm.LLMUnavailable, ValueError) as e:
        return {"status": "error", "reason": str(e)}
    notice_id = store.add_notice(child, text[: notices.MAX_TEXT], summary, actions)
    return {
        "status": "ok",
        "notice_id": notice_id,
        "language": language,
        "summary": summary,
        "actions": actions,
    }


@mcp.tool()
async def list_actions(include_done: bool = False) -> dict:
    """List the parent's tasks from school messages, soonest deadline first."""
    return {"actions": store.list_actions(only_open=not include_done)}


@mcp.tool()
async def complete_action(action_id: int) -> dict:
    """Mark a task as done."""
    if not store.complete_action(action_id):
        return {"status": "error", "reason": "Action not found"}
    return {"status": "ok"}


@mcp.tool()
async def draft_reply(notice_id: int, what_to_say: str) -> dict:
    """Draft a polite English reply to the school, from what the parent wants to say. Never sends anything."""
    notice = store.get_notice(notice_id)
    if notice is None:
        return {"status": "error", "reason": "Notice not found"}
    language = store.get_setting("language", "en")
    try:
        draft, back = await notices.draft_reply(
            notice["text"], notice["child"], what_to_say, language
        )
    except (llm.LLMUnavailable, ValueError) as e:
        return {"status": "error", "reason": str(e)}
    return {
        "status": "ok",
        "draft": draft,
        "back_translation": back,
        "language": language,
        "sent": False,
    }


if __name__ == "__main__":
    mcp.run(transport="streamable-http")