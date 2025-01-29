from openai import OpenAI



def get_chat_messages(prompt_text,rule,client:OpenAI):
    

    completion = client.chat.completions.create(
    model='deepseek-chat',
    messages=[
        {"role": "system", "content": rule},
        {"role": "user", "content": prompt_text}
    ]
    )
    return completion

