from groq import Groq
from app.config import GROQ_API_KEY, GROQ_MODEL

# Initialize Groq client
client = Groq(api_key=GROQ_API_KEY)


def call_llm(prompt: str, system_prompt: str, max_tokens: int = 1000) -> str:
    """
    Send a prompt to Groq LLM and get a response.
    
    Args:
        prompt       : The user message / instruction
        system_prompt: The system role / behavior instruction
        max_tokens   : Maximum tokens in the response
    
    Returns:
        str: The LLM response text
    """
    try:
        response = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user",   "content": prompt}
            ],
            max_tokens=max_tokens,
            temperature=0.8,  # Higher = more creative
        )
        return response.choices[0].message.content

    except Exception as e:
        print(f"❌ LLM call failed: {e}")
        raise e


def call_llm_json(prompt: str, system_prompt: str, max_tokens: int = 500) -> str:
    """
    Send a prompt to Groq LLM and get a JSON response.
    Used for structured outputs like choices.

    Args:
        prompt       : The user message / instruction
        system_prompt: The system role / behavior instruction
        max_tokens   : Maximum tokens in the response

    Returns:
        str: The LLM response text in JSON format
    """
    try:
        response = client.chat.completions.create(
            model=GROQ_MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user",   "content": prompt}
            ],
            max_tokens=max_tokens,
            temperature=0.5,  # Lower = more consistent JSON
            response_format={"type": "json_object"}
        )
        return response.choices[0].message.content

    except Exception as e:
        print(f"❌ LLM JSON call failed: {e}")
        raise e