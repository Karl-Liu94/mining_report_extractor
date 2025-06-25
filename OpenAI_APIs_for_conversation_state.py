from openai import OpenAI
client = OpenAI()

response = client.responses.create(
    model="o4-mini",
    # instructions 参数设定了对话的基本要求
    instructions="你是一名地质和矿业领域的专家，请你仔细阅读报告内容，认真回答用户的问题，注意答案需要条理清晰，如果遇到不知道或者报告中没有的问题可直言不知道，切不可胡编乱造！优先保证答案的正确性",
    # input 参数传入用户真实问题
    input="报告中是否提到了矿体的分布信息？",
)
print(response.output_text)

second_response = client.responses.create(
    model="o4-mini",
    instructions="你是一名地质和矿业领域的专家，请你仔细阅读报告内容，认真回答用户的问题，注意答案需要条理清晰，如果遇到不知道或者报告中没有的问题可直言不知道，切不可胡编乱造！优先保证答案的正确性",
    previous_response_id=response.id,
    input="你认为这个矿山有无考察价值",
)
print(second_response.output_text)
