from mcp.server.fastmcp import FastMCP
import httpx
import html
import random

# Create an MCP server
mcp = FastMCP("Trivia Game Server")

# Global state to track the game
game_state = {
    "score": 0,
    "current_question": None,
    "current_answer": None,
    "incorrect_answers": [],
    "hints_used": 0
}

@mcp.tool()
async def get_question(category: str = "any", difficulty: str = "medium") -> str:
    """
    Get a new trivia question to answer.
    Args:
        category: The category of the question (default: any).
        difficulty: The difficulty level (easy, medium, hard).
    """
    url = "https://opentdb.com/api.php?amount=1&type=multiple"
    
    if difficulty:
        url += f"&difficulty={difficulty}"
    
    # Simple mapping for common categories could be added here if needed
    # For now, "any" just omits the category param
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url)
            data = response.json()
            
            if data["response_code"] != 0:
                return "Failed to fetch question. Please try again."
                
            question_data = data["results"][0]
            
            # Decode HTML entities
            question = html.unescape(question_data["question"])
            correct_answer = html.unescape(question_data["correct_answer"])
            incorrect_answers = [html.unescape(ans) for ans in question_data["incorrect_answers"]]
            
            # Store state
            game_state["current_question"] = question
            game_state["current_answer"] = correct_answer
            game_state["incorrect_answers"] = incorrect_answers
            game_state["hints_used"] = 0 # Reset hints for new question
            
            # Shuffle answers for display? Or just show the question?
            # Typically trivia just asks the question.
            
            return f"Question: {question}\n(Difficulty: {question_data['difficulty']}, Category: {question_data['category']})"
            
        except Exception as e:
            return f"Error fetching question: {str(e)}"

@mcp.tool()
def get_hint() -> str:
    """
    Get a hint for the current question. Deducts 0.5 points from potential score? 
    (Score logic is simple here, so we just track usage).
    """
    current_answer = game_state["current_answer"]
    if not current_answer:
        return "No active question! Please use `get_question` to start."
    
    game_state["hints_used"] += 1
    
    # Hint 1: First letter and length
    if game_state["hints_used"] == 1:
        return f"Hint: The answer starts with '{current_answer[0]}' and has {len(current_answer)} characters."
    
    # Hint 2: Scrambled word (if single word) or more letters?
    # Let's keep it simple.
    return "No more hints available!"

@mcp.tool()
def answer_question(user_answer: str) -> str:
    """
    Submit an answer to the current trivia question.
    Args:
        user_answer: Your answer to the question.
    """
    current_answer = game_state["current_answer"]
    
    if not current_answer:
        return "No active question! Please use `get_question` to start."

    # Simple normalization for comparison (case-insensitive)
    is_correct = user_answer.strip().lower() == current_answer.lower()
    
    if is_correct:
        points = 1
        if game_state["hints_used"] > 0:
            points = 0.5
            
        game_state["score"] += points
        result = f"✅ Correct! The answer is {current_answer}.\nPoints earned: {points}\nCurrent Score: {game_state['score']}"
    else:
        result = f"❌ Incorrect. The correct answer was {current_answer}.\nCurrent Score: {game_state['score']}"
    
    # Reset current question
    game_state["current_question"] = None
    game_state["current_answer"] = None
    game_state["incorrect_answers"] = []
    
    return result

@mcp.tool()
def get_score() -> str:
    """Check your current score."""
    return f"Current Score: {game_state['score']}"

if __name__ == "__main__":
    mcp.run()
