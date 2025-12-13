import os

import openai

try:
    import base64
    import json

    from openai import OpenAI, RateLimitError

    import set
    import tools

    settings = set.Set()


    user_model_name = "YOUR_MODEL_NAME"

    client = OpenAI(
        api_key = "YOUR_API_KEY",
        base_url = "YOUR_BASE_URL",
    )


    chemical = "暂时没有化学物质，请先调用工具choose_chemical"

    sys_prompt = {"role": "system", "content": settings.prompt + f"当前谜底：{chemical}，请按照此回答用户的问题，不要自己瞎编一个！！！（在用户未明确提出揭晓谜底的情况下严禁将此告诉用户，这将影响游戏的平衡）"}

    choice = None


    past_message = []


    def chat(query):
        try:
            global chemical, choice, past_message
            finish_reason = None
            past_message.append({"role": "user", "content": query + f"\n开发者提醒：本次谜底为{chemical}，请严格按照此谜底回答用户问题，当用户提出重新开始时，请调用工具choose_chemical，另外，注意要确保回答正确。本段提醒为开发者附加，非用户输入"})
            messages = [
                sys_prompt,
                {"role": "assistant", "content": "非常抱歉，我确实应该按照您设定的规则和谜底来回答。如果本次游戏中出现了错误，那是因为我没有正确调用或理解您设置的谜底。再次为这个失误向您道歉，并且在接下来的游戏里我会更加注意遵守规则，不会继续告诉您谜底，并且只在您提出开始游戏时会使用工具choose_chemical进行随机抽取谜底，并且不会一直连续调用多次工具"},
            ]
            messages.extend(past_message)
            completion = client.chat.completions.create(
                model = user_model_name,
                messages = messages,
                tools = tools.tools,
                tool_choice = "auto",
                temperature = settings.temperature,
                max_tokens = settings.max_token,
            )
            choice = completion.choices[0]
            finish_reason = choice.finish_reason
            if finish_reason == "tool_calls":
                messages.append(choice.message)
                tool_call = choice.message.tool_calls[0]
                print(tool_call)
                tool_call_name = tool_call.function.name
                tool_call_arguments = json.loads(tool_call.function.arguments)
                tool_function = tools.tool_map[tool_call_name]
                tool_result = tool_function(tool_call_arguments)
                chemical = json.dumps(tool_result)
                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "name": tool_call_name,
                        "content": json.dumps(tool_result)
                    }
                )
                completion = client.chat.completions.create(
                    model=user_model_name,
                    messages=messages,
                    tools=tools.tools,
                    tool_choice="auto",
                    temperature=settings.temperature,
                    max_tokens=settings.max_token,
                    extra_body={
                        "enable_thinking": False
                    },
                )
                choice = completion.choices[0]
                finish_reason = choice.finish_reason
            flag = True
            cnt = 0
            while flag:
                cnt += 1
                if cnt >= 100:
                    return "请求过多，请稍后再试"
                flag = False
                try:
                    completion = client.chat.completions.create(
                        model = user_model_name,
                        messages = messages,
                        tool_choice = "none",
                        temperature = settings.temperature,
                        max_tokens = settings.max_token,
                        extra_body={
                            "enable_thinking": False
                        },
                    )
                except RateLimitError:
                    flag = True
            choice = completion.choices[0]
            result = choice.message.content
            #print(choice.message.reasoning_content)
            past_message.append({"role": "assistant", "content": result})
            if len(past_message) > settings.past_message_number:
                past_message = past_message[-settings.past_message_number:]
            return result
        except openai.APIConnectionError:
            return "连接不到API"
        except openai.PermissionDeniedError:
            return "联系不到API"
        except:
            return "未知错误"



    def main():
        ipt = None
        print("试着说：“开始”")
        while ipt != "esc":
            ipt = input("键入语句并回车以给AI发送信息（键入esc退出）：")
            if ipt == "esc":
                break
            ans = "API调用失败"
            flag = True
            while flag:
                flag = False
                try:
                    ans = chat(ipt)
                    print("AI：" + ans)
                    if settings.debug:
                        print("debug:" + chemical)
                except RateLimitError:
                    flag = True
                    print("服务器繁忙，正在重试中……")


    if __name__ == "__main__":
        if not os.path.exists("chemistTemp"):
            os.makedirs("chemistTemp")
        main()
except openai.APIConnectionError:
    print("无法连接，请检查网络后再试")
except openai.PermissionDeniedError:
    print("联系不到API")
except:
    print("未知错误")