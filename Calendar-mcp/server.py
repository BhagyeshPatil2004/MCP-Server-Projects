# /// script
# dependencies = [
#   "mcp",
#   "google-auth-oauthlib",
#   "google-auth",
#   "google-api-python-client"
# ]
# ///

from mcp.server.fastmcp import FastMCP
from google_calendar import get_service
import datetime

# Initialize FastMCP server
mcp = FastMCP("Google Calendar")

# To List number of events
@mcp.tool()
def list_events(max_results: int = 10) -> str:
    """
    Lists upcoming events from the user's primary calendar.
    Args:
        max_results: The maximum number of events to return (default 10).
    """
    try:
        service = get_service()
        now = datetime.datetime.utcnow().isoformat() + "Z"  # 'Z' indicates UTC time
        
        events_result = (
            service.events()
            .list(
                calendarId="primary",
                timeMin=now,
                maxResults=max_results,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
        events = events_result.get("items", [])

        if not events:
            return "No upcoming events found."

        result = "Upcoming events:\n"
        for event in events:
            start = event["start"].get("dateTime", event["start"].get("date"))
            result += f"- {start}: {event['summary']}\n"
        
        return result

    except Exception as e:
        return f"Error listing events: {str(e)}"

# To add an event
@mcp.tool()
def add_event(summary: str, start_time: str, end_time: str, timezone: str = "Asia/Kolkata") -> str:
    """
    Adds a new event to the user's primary calendar.
    Args:
        summary: The title of the event.
        start_time: The start time in ISO format (e.g., '2023-10-27T10:00:00') or partial format like '2023-10-27 10:00'.
        end_time: The end time in ISO format (e.g., '2023-10-27T14:00:00') or partial format like '2023-10-27 14:00'.
        timezone: The timezone for the event (default: Asia/Kolkata for India).
    """
    try:
        service = get_service()
        
        # Normalize datetime strings - add seconds if missing
        if len(start_time) == 16:  # Format: "2023-10-27 10:00"
            start_time = start_time.replace(" ", "T") + ":00"
        if len(end_time) == 16:
            end_time = end_time.replace(" ", "T") + ":00"
        
        event = {
            "summary": summary,
            "start": {
                "dateTime": start_time,
                "timeZone": timezone,
            },
            "end": {
                "dateTime": end_time,
                "timeZone": timezone,
            },
        }

        event = service.events().insert(calendarId="primary", body=event).execute()
        return f"Event created: {event.get('htmlLink')}"

    except Exception as e:
        return f"Error adding event: {str(e)}"

# To delete an event
@mcp.tool()
def delete_event(event_id: str) -> str:
    """
    Deletes an event from the user's primary calendar.
    Args:
        event_id: The ID of the event to delete.
    """
    try:
        service = get_service()
        service.events().delete(calendarId="primary", eventId=event_id).execute()
        return f"Event {event_id} deleted."
    except Exception as e:
        return f"Error deleting event: {str(e)}"

if __name__ == "__main__":
    mcp.run()