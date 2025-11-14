import base64

import openai
from openai import OpenAI

import set


user_model_name = "YOUR_MODEL_NAME"

client2 = OpenAI(
    api_key = "YOUR_API_KEY",
    base_url = "YOUR_BASE_URL",
)


settings = set.Set()


chooser_sys_prompt = {"role": "system", "content": settings.chooser_system_prompt}


ban = []

def choose_chemical(requirement: str="无") -> str:
    """
    内置一个大模型，调用此函数时可以按照要求选择一个化学物质并返回这个化学物质的化学式
    形参：
    requirement:对于选择化学式的要求
    """
    flag = True
    result = "1"
    while flag:
        flag = False
        try:
            completion = client2.chat.completions.create(
                model=user_model_name,
                messages=[
                    chooser_sys_prompt,
                    {"role": "user", "content": f"随机选取一个化学物质，要求如下：{requirement}，不能生成以下物质：{ban}"},
                ],
                temperature=settings.chooser_temperature,
                max_tokens=settings.chooser_max_token,
            )
            result = completion.choices[0].message.content
            ban.append(result)
            if len(ban) >= 8:
                ban.pop(0)
            #if settings.debug:
            #    print("工具调用成功！")
        except openai.RateLimitError:
            flag = True
            return "error"
    #print("Debug:"+result)
    return result


tools = [
    {
        "type": "function",
        "function": {
            "name": "choose_chemical",
            "description": "调用此函数时可以按照要求选择一个化学物质并返回这个化学物质的化学式",
            "parameters": {
                "type": "object",
                "properties": {
                    "requirement": {
                        "type": "string",
                        "description": "对于选择化学式的要求",
                    },
                },
            },
        },
    },
]

tool_map = {
    "choose_chemical": choose_chemical,
}
