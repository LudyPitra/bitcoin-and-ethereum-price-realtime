import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from functions import coin_price_consult

tools = [
    {
        "type": "function",
        "function":{
            "name": "coin_price_consult",
            "description": "Consults the current price of the coin in USD",
            "parameters": {
                "type": "object",
                "properties":{
                    "coin_name":{
                        "type": "string",
                        "description": "The name or ticker of the coin."
                    }
                },
                "required": ["coin_name"]
            }
        }
    }
]


load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def create_response(user_message: str):
    messages = [
        {"role": "user", "content": user_message}
    ]

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        tools=tools,
        tool_choice="auto"
    )

    message= response.choices[0].message

    if message.tool_calls:
        call = message.tool_calls[0]
        function_name = call.function.name
        arguments = json.loads(call.function.arguments)

        if function_name == "coin_price_consult":
            result = coin_price_consult(**arguments)

            messages.append({
                "role": "function",
                "name": function_name,
                "content": result
            })

            second_response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages
            )

            return second_response.choices[0].message.content
        
    return message.content