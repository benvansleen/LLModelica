from dotenv import load_dotenv
load_dotenv()

import functions as f
from openai_models import OpenAIResponse
from chain import Chain
from om import om


print(om('getVersion()'))


def prompt_user():
    print('> ', end='')
    return {
        'role': 'user',
        'content': input(),
        # 'content': wrap_prompt_in_context(input()),
    }


def handle_response(
        response: OpenAIResponse,
        messages: Chain,
) -> Chain:
    first_choice = response.choices[0]
    messages.add(first_choice.message)

    match first_choice.finish_reason:
        case 'function_call':
            result = f.dispatch_function(response)
        case _:
            result = prompt_user()

    messages.add(result)
    return messages


def prompt_step(messages: Chain = Chain()):
    if len(messages) <= 1:
        messages.add(prompt_user())

    response = f.llm(messages, model='gpt-4-0613')
    messages.print(clear=True)
    messages = handle_response(response, messages)
    messages.print(clear=True)
    return


while True:
    try:
        prompt_step()
    except KeyboardInterrupt:
        from sys import exit
        exit()
