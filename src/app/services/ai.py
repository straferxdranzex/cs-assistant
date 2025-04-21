from typing import AsyncGenerator
import groq
from app.core.config import settings


class AIService:
    def __init__(self):
        self.client = groq.Groq(api_key=settings.GROQ_API_KEY)
        self.model = settings.GROQ_MODEL

    async def generate_response(
        self, ticket_description: str, message_history: str, latest_message: str
    ) -> AsyncGenerator[str, None]:
        prompt = f"""You are a helpful customer support assistant. 
The customer has the following issue: {ticket_description}

Previous messages:
{message_history}

Customer's latest message: {latest_message}

Provide a helpful response that addresses their concern:
"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            stream=True,
        )

        for chunk in response:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content
