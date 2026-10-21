# Friction Log

Project: School Bridge (Alexa+ track). Environment: Windows, Python 3.11, MCP Python SDK v1, Gemini API free tier.
Severity scale: High = blocks the intended path; Medium = costs significant time or needs a code change; Low = small annoyance with an easy workaround.

## 1. Registering an MCP server as an Alexa+ add-on
- **Task:** Register my MCP server as an Alexa+ add-on so a real Alexa+ client could call it.
- **Steps taken:** Read the Alexa+ developer docs home, the MCP client lifecycle page and the MCP design guide.
- **Expected:** A self-serve path (for example `alexa-ai deploy`) open to hackathon participants.
- **Actual:** The docs home says Category SDK and MCP Toolkit are available to select partners only. I could not tell how a participant gets access.
- **Severity:** High
- **Workaround:** Simulated the Alexa+ experience with a local web page, as the track allows. The MCP server stays a separate surface.
- **Suggestion:** State on the hackathon page whether simulation is the expected path, or how participants can request toolkit access.

## 2. Choosing the MCP protocol version
- **Task:** Decide which MCP protocol version my server must support.
- **Steps taken:** Compared the track description with the Alexa+ client lifecycle page.
- **Expected:** One version across the hackathon rules and the Alexa+ docs.
- **Actual:** The track asks for spec 2025-11-25 or later. The lifecycle page shows an initialize request with protocol version 2025-03-26.
- **Severity:** Medium
- **Workaround:** Sent initialize requests with both versions to my server. It answered with the version requested each time. I could not test with a real Alexa+ client.
- **Suggestion:** Align the version across the docs and the track, or say which one the Alexa+ client actually negotiates.

## 3. `mcp dev` on Windows (first hit in my other hackathon project)
- **Task:** Open the MCP server in MCP Inspector with `mcp dev` inside a virtualenv.
- **Steps taken:** Ran `mcp dev` from the activated virtualenv.
- **Expected:** Inspector opens.
- **Actual:** `npx` is not found (PATH issue inside the virtualenv).
- **Severity:** Low
- **Workaround:** Run `npx @modelcontextprotocol/inspector` directly and add the server by its Streamable HTTP URL.
- **Suggestion:** Document the Windows virtualenv case, or print a clearer error when `npx` is missing.

## 4. FastMCP rename in SDK v2 (first hit in my other project)
- **Task:** Use `FastMCP` from v1-era tutorials with the latest SDK.
- **Steps taken:** Installed the SDK without a version pin and ran tutorial code.
- **Expected:** The import works.
- **Actual:** v2 renamed FastMCP, so tutorial code fails.
- **Severity:** Low
- **Workaround:** Pinned `mcp[cli]>=1.30,<2` in requirements.txt.
- **Suggestion:** Add a migration note at the top of the v1 quickstart pages.

## 5. Gemini model availability (first hit in my other project)
- **Task:** Call `gemini-2.5-flash` with a newly created free API key.
- **Steps taken:** Created a key in Google AI Studio and sent a generateContent request.
- **Expected:** A normal response.
- **Actual:** The model is unavailable to new users.
- **Severity:** Low
- **Workaround:** Switched to `gemini-flash-lite-latest`, configurable through `GEMINI_MODEL`.
- **Suggestion:** Show in AI Studio which models a new free key can use.

## 6. Local web server port on Windows
- **Task:** Start the demo web page on port 8080.
- **Steps taken:** Ran `python -m schoolbridge.web`.
- **Expected:** The server starts.
- **Actual:** `PermissionError: [WinError 10013]` when binding the port.
- **Severity:** Low
- **Workaround:** Made the port configurable (`SCHOOLBRIDGE_WEB_PORT`), default 8765.
- **Suggestion:** Not an Alexa+ issue. Worth knowing that common dev ports can be reserved on Windows.

## 7. Kazakh output with mixed alphabets
- **Task:** Get a natural Kazakh summary of a school notice from the LLM.
- **Steps taken:** Sent a notice with the parent language set to Kazakh.
- **Expected:** Clean Cyrillic text.
- **Actual:** Grammar and terminology were correct, but one name came back with a Latin letter inside a Cyrillic word.
- **Severity:** Low
- **Workaround:** Used a Cyrillic spelling of the name in the demo.
- **Suggestion:** Validate script consistency in code for Kazakh output. A native speaker should review the Kazakh phrases before real use.

## 8. Gemini free tier timeouts
- **Task:** Route a parent's request to a tool through Gemini.
- **Steps taken:** Sent requests from the demo page during recording.
- **Expected:** A response within the 30 s timeout.
- **Actual:** "Gemini did not answer within 30s", and again within 45s.
- **Severity:** Medium
- **Workaround:** Raised the timeout to 45 s and added one retry. Failed calls show a plain error in the chat instead of crashing.
- **Suggestion:** Publish expected latency and free-tier limits for flash-lite models.

## Not covered
I did not run the Alexa AI CLI and did not test the server with a real Alexa+ client.

Items 3 to 5 were first hit while building my other hackathon project. I carried the workarounds over to School Bridge (the `mcp[cli]<2` pin, `gemini-flash-lite-latest` as the default model, and Inspector launched through `npx`) rather than hitting each problem again from scratch.