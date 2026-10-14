import json
import ollama

from app.agent.tools import get_order_details, get_ticket_details,search_support_knowledge
from app.core.database import SessionLocal


tools = [
    {
        "type": "function",
        "function": {
            "name": "get_order_details",
            "description": "Retrieve real order details from PostgreSQL using an order ID.",
            "parameters": {
                "type": "object",
                "properties": {
                    "order_id": {
                        "type": "integer",
                        "description": "The ID of the order to retrieve"
                    }
                },
                "required": ["order_id"]
            }
        }
    }, 
    {
    "type": "function",
    "function": {
        "name": "get_ticket_details",
        "description": "Retrieve a support ticket's subject, message, status, and related order using its ticket ID.",
        "parameters": {
            "type": "object",
            "properties": {
                "ticket_id": {
                    "type": "integer",
                    "description": "The ID of the support ticket to retrieve"
                }
            },
            "required": ["ticket_id"]
        }
    }
},
{
    "type": "function",
    "function": {
        "name": "search_support_knowledge",
        "description": (
            "Search support policy and troubleshooting documents "
            "for questions about refunds, shipping, returns, "
            "or damaged products."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The support question to search for"
                }
            },
            "required": ["query"]
        }
    }
}

]

def ask_agent(question: str) -> str:
    db = SessionLocal()

    try:
        messages = [
            {
                "role": "system",
                "content": (
                    "You are a support assistant connected to PostgreSQL "
                    "and support policy documents.\n"
                    "For order questions, use get_order_details.\n"
                    "For ticket questions, use get_ticket_details.\n"
                    "For policy or troubleshooting questions, use "
                    "search_support_knowledge.\n"
                    "Never invent order, ticket, or policy information. "
                    "Use tool results as evidence. If the information "
                    "is unavailable, say so clearly."
                )
            },
            {"role": "user", "content": question}
        ]

        for _ in range(5):
            response = ollama.chat(
                model="llama3.2:3b",
                messages=messages,
                tools=tools
            )

            messages.append(response.message)

            tool_calls = response.message.tool_calls or []

            if not tool_calls:
                return response.message.content or ""

            for tool_call in tool_calls:
                tool_name = tool_call.function.name
                arguments = tool_call.function.arguments

                try:
                    if tool_name == "get_order_details":
                        order_id = int(arguments["order_id"])
                        if order_id <= 0:
                            raise ValueError
                        result = get_order_details(order_id, db)

                    elif tool_name == "get_ticket_details":
                        ticket_id = int(arguments["ticket_id"])
                        if ticket_id <= 0:
                            raise ValueError
                        result = get_ticket_details(ticket_id, db)

                    elif tool_name == "search_support_knowledge":
                        query = arguments["query"]
                        if not isinstance(query, str) or not query.strip():
                            raise ValueError
                        result = search_support_knowledge(query)

                    else:
                        result = {"error": "Unknown tool"}

                except (ValueError, TypeError, KeyError):
                    result = {"error": "Invalid tool arguments"}

                messages.append({
                    "role": "tool",
                    "tool_name": tool_name,
                    "content": json.dumps(result)
                })

        return "I couldn't complete the request within the tool-call limit."

    finally:
        db.close()
