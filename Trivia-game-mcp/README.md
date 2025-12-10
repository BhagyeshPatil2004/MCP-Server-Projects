# Trivia Game MCP Server

This MCP server provides an interactive trivia game using the [Open Trivia DB](https://opentdb.com/) API. It allows you to play trivia games directly within Claude.

## Features

- **Infinite Questions**: Fetches real-time questions from the Open Trivia Database.
- **Hint System**: Get hints for difficult questions (costs 0.5 points).
- **Scoring**: Tracks your score across the session.

## Prerequisites

- Python 3.11 or higher
- `uv` (optional, for dependency management) or `pip`.

## Installation

1.  **Clone the repository**:
    ```bash
    git clone <repository_url>
    cd Trivia-game-mcp
    ```

2.  **Install dependencies**:
    Using `uv`:
    ```bash
    uv sync
    ```
    
    Or using `pip`:
    ```bash
    pip install "mcp[cli]>=1.23.1" httpx
    ```

## Configuration

Add the following to your `claude_desktop_config.json` (usually found in `%APPDATA%\Claude\` on Windows or `~/Library/Application Support/Claude/` on macOS):

```json
{
  "mcpServers": {
    "trivia-game": {
      "command": "python",
      "args": [
        "C:\\Agent MCP\\Trivia-game-mcp\\main.py"
      ]
    }
  }
}
```
*Note: Adjust the path to `main.py` if your location differs.*

## Tools

### `get_question(category: str = "any", difficulty: str = "medium")`
Fetches a new trivia question.
- **category**: Question category (currently "any" for all categories).
- **difficulty**: "easy", "medium", or "hard".

### `answer_question(user_answer: str)`
Submit your answer.
- Returns "Correct" or "Incorrect" and updates your score.
- **Scoring**: 1 point for correct answer, 0.5 points if a hint was used.

### `get_hint()`
Get a hint for the current question.
- Reveals the first letter and the length of the answer.
- **Cost**: 0.5 points.

### `get_score()`
Check your current score.
