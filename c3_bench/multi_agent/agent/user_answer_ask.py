import json
import os

from utils import get_all_tool_info, logger


user_system_prompt_template_zh = '''请你扮演一个用户，你正在和一个超级智能体进行交互。
这个超级智能体拥有一个Planner、Agent助手，并具备一系列外部工具，可以使用外部工具解决你提出的任务，具体见[工具列表]。
根据上下文对话信息，你已经提出了你的任务，但是根据Planner的反馈，你提供的任务信息不足。
因此，接下来，请你根据最新一轮超级智能体的Agent助手询问的信息进行回复，给出Agent助手要求的必填参数，从而帮助超级智能体解决你的任务。
输出格式参考[用户输出格式]。

{{{all_tool_required_info}}}

[环境信息]="""
{{{env_info}}}
"""

[用户输出格式]="""
用户：根据[要求]，回复上下文对话信息中最近一轮以 "Agent助手：" 开头的内容（不要重复这句话）
"""

[要求]="""
1、回复必须以 "用户：" 开头。
2、根据上下文对话信息，回复最近一轮以 "Agent助手：" 开头的用户任务。
3、你的回复里必须包含Agent助手所询问的所有必填参数的信息，使用自然语言描述，可以看情况伪造出一个，例如Base64编码字符串。（不要重复这句话）。
4、你的回复需要使用不同种类的句子结构：祈使句、陈述句、疑问句等。
5、你的回复应该使用不同的语气：口语化、正式、礼貌、直接等。
6、你的回复应该使用不同的长度：有短到长，长度逐渐递增。
"""

[工具列表]="""
{{{tools}}}
"""'''


user_system_prompt_template_en = '''Please play the role of a user who is interacting with a super intelligent agent.
This super intelligent agent has a Planner, an Agent Assistant, and a series of external tools that can be used to solve the tasks you propose, as detailed in the [Tool List].
Based on the context of the conversation, you have already proposed your task, but according to the Planner's feedback, the information you provided is insufficient.
Therefore, next, please respond according to the latest round of inquiries from the super intelligent agent's Agent Assistant, providing the required parameters requested by the Agent Assistant to help the super intelligent agent solve your task.
Refer to the [User Output Format] for the output format.

{{{all_tool_required_info}}}

[Environment Information]="""
{{{env_info}}}
"""

[User Output Format]="""
User: According to the [Requirements], respond to the most recent round of context conversation information that starts with "Agent Assistant:" (do not repeat this sentence).
"""

[Requirements]="""
1. The response must start with "User:".
2. Based on the context of the conversation, respond to the most recent user task that starts with "Agent Assistant:".
3. Your response must include all the required parameter information requested by the Agent Assistant, described in natural language. You may fabricate one if necessary, such as a Base64 encoded string. (Do not repeat this sentence).
4. Your response should use different types of sentence structures: imperative, declarative, interrogative, etc.
5. Your response should use different tones: colloquial, formal, polite, direct,etc.
6. Your response should vary in length: from short to long, gradually increasing in length.
"""

[Tool List]="""
{{{tools}}}
"""'''

def user_answer_ask(messages, tools, env_info, request_func):
    all_tool_name, all_tool_required_info = get_all_tool_info(tools)
    language = os.getenv("LANGUAGE")
    if language == "zh":
        user_system_prompt_template = user_system_prompt_template_zh
    else:
        user_system_prompt_template = user_system_prompt_template_en
    user_system_prompt = user_system_prompt_template.replace("{{{tools}}}", json.dumps(tools, ensure_ascii=False, indent=4)) \
                                                    .replace("{{{env_info}}}", env_info) \
                                                    .replace("{{{all_tool_required_info}}}", all_tool_required_info)
    # print(user_system_prompt)
    messages_new = [
        {
            "role": "system",
            "content": user_system_prompt
        }
    ]
    messages_new.extend(messages)
    res = request_func(messages_new)
    logger.info(f"user_answer_ask:\n{res}\n")
    fetch_data = {"task": "user_answer_ask", "tools": tools, "env_info": env_info, "messages": messages_new, "answer": res}
    return res, fetch_data


def main():
    pass


if __name__ == "__main__":
    main()
