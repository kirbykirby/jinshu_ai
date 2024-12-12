from .chatbot import Chatbot


def init_chatbot(
    api_key,
    model="gpt-4o-mini",
    base_url="https://api.bltcy.ai/v1",
    system_prompt=None,
    initial_assistant_message=None,
    max_tokens=1024,
    temperature=0.7,
    max_history_length=10,
) -> Chatbot:
    return Chatbot(
        api_key,
        model,
        base_url,
        system_prompt,
        initial_assistant_message,
        max_tokens,
        temperature,
        max_history_length,
    )


def get_chatbot_response(
    user_prompt, bot, stream=True, print_response=True, debug=True
):
    return bot.get_response(user_prompt, stream, print_response, debug)
