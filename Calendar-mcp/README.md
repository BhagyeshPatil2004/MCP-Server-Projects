# Google Calendar MCP Server [`Calendar-mcp`](./Calendar-mcp)
This MCP server integrates with Google Calendar to allow you to list, add, and delete events directly from Claude.

https://github.com/user-attachments/assets/fdcdcdd7-9ffe-4823-96be-0fd86696bf06

## Features

- **List Events**: View upcoming events from your primary calendar.
- **Add Event**: Create new events with a summary, start time, and end time.
- **Delete Event**: Remove events using their ID.

## Prerequisites

- Python 3.10 or higher
- A Google Cloud Project with the Google Calendar API enabled.
- `credentials.json` file from your Google Cloud Project (OAuth 2.0 Client ID).

## Installation

1.  **Clone the repository** (if you haven't already):
    ```bash
    git clone <repository_url>
    cd Calendar-mcp
    ```

2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## Configuration

1.  **Google Cloud Setup**:
    - Go to the [Google Cloud Console](https://console.cloud.google.com/).
    - Create a new project or select an existing one.
    - Enable the **Google Calendar API**.
    - Configure the **OAuth consent screen** (External user type is usually easiest for personal testing).
    - Go to **Credentials**, create **OAuth client ID** (Desktop app).
    - Download the JSON file and rename it to `credentials.json`.
    - Place `credentials.json` in the root of the `Calendar-mcp` directory.

2.  **First Run**:
    - When you run the server for the first time (or use it via Claude), a browser window will open asking you to log in to your Google account and authorize the application.
    - Click "Continue" (you might see a "Google hasn't verified this app" warning if you haven't published your app; click "Advanced" -> "Go to <Project Name> (unsafe)" to proceed).
    - After authorization, a `token.json` file will be created automatically to store your credentials.

## Usage with Claude Desktop

Add the following to your `claude_desktop_config.json` (usually found in `%APPDATA%\Claude\` on Windows or `~/Library/Application Support/Claude/` on macOS):

```json
{
  "mcpServers": {
    "google-calendar": {
      "command": "python",
      "args": [
        "C:\\Agent MCP\\Calendar-mcp\\server.py"
      ]
    }
  }
}
```
*Note: Adjust the path to `server.py` to match your actual file location.*

## Tools

- `list_events(max_results: int = 10)`
- `add_event(summary: str, start_time: str, end_time: str, timezone: str = "Asia/Kolkata")`
- `delete_event(event_id: str)`
