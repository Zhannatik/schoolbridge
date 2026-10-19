# School Bridge

An MCP server and a simulated voice-assistant demo that help immigrant parents understand school messages. The parent speaks Russian or Kazakh. School Bridge explains the message in their language, extracts tasks with deadlines, and drafts an English reply with a back-translation so the parent can verify it before sending.

Built for the Amazon Developer "Build, Ship, Shape" hackathon, Alexa+ track.

## What is real and what is simulated

- **Simulated:** the Alexa+ experience. The server answers the initialize request shown in the Alexa+ MCP client docs (protocol version 2025-03-26, streamable HTTP). I could not test it against a real Alexa+ client.
- **Real:** the MCP server (Streamable HTTP, 6 tools), the SQLite state that persists between sessions, and the Gemini-based analysis and drafting.
- The web page calls the same Python functions in-process. The MCP server is a separate surface that an MCP client, including Alexa+, can connect to.

## Tools (MCP)

`set_language`, `add_child`, `add_notice`, `list_actions`, `complete_action`, `draft_reply`

## Safety design

- Nothing is ever sent to the school. Replies are drafts only.
- All LLM output is validated in code. The router's tool choice is checked against an allowlist; unknown tools become "none".
- Untrusted text (school messages, parent requests) is length-limited and delimiter-stripped before it reaches the model.
- The web page listens on 127.0.0.1 only, accepts JSON only, checks the Host header, and renders all text with `textContent`.
- Demo uses fictional data only.

## Setup

```
git clone https://github.com/Zhannatik/schoolbridge
cd schoolbridge
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env      # add GEMINI_API_KEY
python -m pytest            # 11 tests
```

Run the demo page: `python -m schoolbridge.web` and open http://127.0.0.1:8765 (Chrome or Edge for voice input).
Run the MCP server: `python -m schoolbridge.server` (http://127.0.0.1:8000/mcp).

## Demo walkthrough

1. Switch to RU, say "Добавь ребёнка Айдар, 3 класс".
2. Forward a fictional school message, press Explain.
3. Ask "Какие у меня задачи?".
4. Say "Айдар заболел, напиши школе, что он не поедет": get an English draft plus a Russian check.
5. Mark a task done.

## Limits

Kazakh speech recognition depends on the browser. Gemini free-tier limits apply. The Kazakh help phrase was written by the author and may need native review.

## License

MIT