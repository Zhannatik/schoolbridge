# Friction Log

Project: School Bridge (Alexa+ track). Environment: Windows, Python 3.11, MCP Python SDK v1, Gemini API free tier.

## 1. Registering an MCP server as an Alexa+ add-on
- **Task:** Find out how to register my MCP server as an Alexa+ add-on so a real Alexa+ client could call it.
- **Expected:** A self-serve path (for example, `alexa-ai deploy`) open to hackathon participants.
- **Actual:** The Alexa+ developer docs home states that Category SDK and MCP Toolkit are available to select partners only. I could not tell from the docs how a hackathon participant gets access.
- **Workaround:** Simulated the Alexa+ experience with a local web page. The MCP server stays a separate surface.
- **Suggestion:** State on the hackathon page whether simulation is the expected path, or how participants can request access.

## 2. Choosing the MCP protocol version
- **Task:** Decide which MCP protocol version my server must support.
- **Expected:** One version across the hackathon rules and the Alexa+ docs.
- **Actual:** The track asks for spec 2025-11-25 or later, while the Alexa+ MCP client lifecycle page shows an initialize request with protocol version 2025-03-26.
- **Workaround:** Sent initialize requests with both versions to my server; it answered with the version requested each time.

## 3. `mcp dev` on Windows
- **Task:** Open the MCP server in MCP Inspector with `mcp dev` inside a virtualenv.
- **Expected:** Inspector opens.
- **Actual:** `npx` is not found (PATH issue inside the virtualenv).
- **Workaround:** Run `npx @modelcontextprotocol/inspector` directly and add the server by its Streamable HTTP URL.

## 4. FastMCP rename in SDK v2
- **Task:** Use `FastMCP` from v1-era tutorials with the latest SDK.
- **Expected:** The import works.
- **Actual:** v2 renamed FastMCP, so tutorial code fails.
- **Workaround:** Pinned `mcp[cli]<2`.

## 5. Gemini model availability
- **Task:** Call `gemini-2.5-flash` with a newly created free API key.
- **Expected:** A normal response.
- **Actual:** The model is unavailable to new users.
- **Workaround:** Switched to `gemini-flash-lite-latest` (configurable through `GEMINI_MODEL`).

## 6. Local web server port on Windows
- **Task:** Start the demo web page on port 8080.
- **Expected:** The server starts.
- **Actual:** `PermissionError: [WinWinError 10013]` when binding the port.
- **Workaround:** Made the port configurable (`SCHOOLBRIDGE_WEB_PORT`), default 8765.

## 7. Kazakh output with mixed alphabets
- **Task:** Get a natural Kazakh summary of a school notice from the LLM.
- **Expected:** Clean Cyrillic text.
- **Actual:** Grammar and terminology were correct, but one name came back with a Latin letter inside a Cyrillic word.
- **Workaround:** Used a Cyrillic spelling of the name in the demo.

## Not covered
I did not run the Alexa AI CLI and did not test the server with a real Alexa+ client. Items 3 to 5 were first hit in my other hackathon project and reproduced here through the shared SDK and API key.