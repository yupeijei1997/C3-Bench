# C^3-Bench: The Things Real Disturbing LLM based Agent in Multi-Tasking


<p align="center">
    📖 <a href="README.md">English</a> •
    <a>中文</a>
    <br>
    🤗 <a href="https://huggingface.co/datasets/jpy/C3-Bench">数据集</a> •
    📚 <a href="https://arxiv.org/abs/2505.18746">预印版论文</a>
</p>


![Example](./picture/first.png)


## 📖 Overview

基于大型语言模型的智能体借助工具来改造环境，这一方式彻底革新了人工智能与物理世界的交互模式。不同于仅依赖历史对话来生成回答的传统自然语言处理任务，这些智能体在做出选择时，必须考虑更为复杂的因素，例如工具间的相互关系、环境反馈以及过往决策等。

当前的研究通常通过多轮对话来评估智能体，但却忽略了上述关键因素对智能体行为的影响。

为了填补这一空白，我们推出了一个开源且高质量的基准测试—C^3-Bench。该基准测试融入了攻击概念，并运用单变量分析来精准定位影响智能体鲁棒性的关键要素。

具体而言，我们设计了三项挑战：复杂工具关系导航、关键隐藏信息处理以及动态决策路径管理。除了这些挑战，我们还引入了细粒度指标、创新数据收集算法以及可复现的评估方法。

我们在49个主流智能体上进行了广泛实验，这些智能体涵盖了通用型快思维模型、慢思维模型以及特定领域模型。实验发现，智能体在处理工具依赖关系、长上下文信息依赖以及频繁的策略类型切换方面存在显著缺陷。

从本质上讲，C^3-Bench旨在通过这些挑战揭示模型的弱点，并推动智能体性能可解释性方面的研究。


## 😊 Key Materials

- 测试数据地址：c3_bench/data/C3-Bench.jsonl 或 🤗 <a href="https://huggingface.co/datasets/jpy/C3-Bench">数据集</a>
- 论文中汇报的49个模型的预测结果地址：c3_bench/bench_test/result
- 更多关于 C3-Bench 的详细信息可以在下文中获取

## ⚡️ Quickstart

### Basic Installation
```bash
# Create a new Conda environment with Python 3.10
conda create -n C3-Bench python=3.10
conda activate C3-Bench

# Clone the C3-Bench repository
git clone https://github.com/yupeijei1997/C3-Bench.git

# Change directory to the `c3_bench`
cd c3_bench/

# Install the package
pip install -r requirements.txt
```

## ⏳ Inference

### 💾 Test Data

![overall](./picture/example_zh.png)

地址：c3_bench/data/C3-Bench.jsonl

说明：我们的测试数据经过了了五名从业NLP、CV、LLM方向多年的高级算法研究员五轮的人工查验与修正，总耗时约1个月。具有极高的质量和准确率，多轮任务之间具有紧密的联系，难度依次递增，不存在不可用的无效数据，并且与人类分布完全一致，其评测结果与结论对后续Agent方向的优化有着极高地参考价值。

具体来说，经过了如下几个阶段的数据质量优化工作：

1、初始数据是使用我们提出的Multi Agent Data Generation框架生成的，并且覆盖了所有可能的动作空间。

2、之后将测试数据按照我们的定义的四种不同类型的动作进行划分，并交由不同的四名算法研究员进行人工查验与修正。具体地，由于LLM生成的任务总是过于正式，不够口语化，特别是到了第二个任务之后，难以生成真多轮问题。因此，我们基于口语化、必须为真多轮任务两个准则对数据进行第一轮修正。特别的，在设计第三轮和第四轮任务时，我们会增加长期记忆这一真多轮类型的任务，来增加测试集的难度。

注：特别的，在实际构建过程中，四名算法研究员均采用了一层一层的方式构建，先由模型生成一层的数据，之后交由人工查验与修正，之后再进行下一层的数据生成与修正。这样做的好处是，避免了在一次性生成所有层的数据之后，当某一层的数据存在问题需要修正时，往往需要对其前一层和后几层的任务均修改，才能保证整体正确性，这会使得数据构建困难，并难以保证数据整体的连贯性。因此，我们采用逐层构建的方式，使得我们的数据层与层之间的任务逻辑性强，关系紧密，不存在不合理的轨迹。

3、在四名算法研究员进行了第一轮修正之后，会由一名Agent领域的高级专家对每条数据进行点评，说明其是否符合要求以及存在的问题，之后由这四名算法研究员进行二次修正。

4、在第二轮修正之后，我们引入了交叉验证，四名算法工程分别去查验其他人的数据并进行点评，然后四名算法研究员和一位Agent领域的高级专家进行讨论，对存疑的数据进行第三轮的修正。

5、在第三轮修正之后，会由一名Agent领域的高级专家分别对全部数据进行第四轮查验与修正，确保数据的绝对准确。

6、最后，由于人类修正可能存在误操作，我们会使用代码对可能误操作产生的参数类型错误、不合理依赖关系进行检查，并由一位高级专家进行最终第五轮的修正。

经过上述五个阶段的数据质量优化工作，每一条数据均由多个算法专家人工修正与构建，使得我们的测试数据从最初的准确率不到60%，最终达到了100%的正确性，并且模型生成结合多人修正的方式，也让我们的数据具备极佳的多样性和质量。

同时，相比其他BenchMark，如BFCL、T-EVAL等，我们的数据覆盖了所有可能的动作空间，并且在第二至四轮全部是真多轮任务，覆盖率达到了2个100%，这也让我们的数据分布十分均衡，能够无死角的测试出模型的短板所在。

![compare](./picture/compare.png)

最终，我们构建的这份高质量数据，为我们后续的实验奠定了基础，让我们的结论具有绝对的可信度。

此外，我们为测试数据提供了双语支持，包括英文和中文两个版本，并全部经过上述人工查验过程。后续LeadBoard结果主要汇报的是英文版本的结果。

## 🛠️ Framework

我们的评估框架采用推理和结果分析分离的方式构建，具备下述多项优点：

- 可复现性高：我们的测试数据里所有正确答案对应的工具执行结果都进行了持久化保存，不需要任何网站的KEY，不存在工具调用不稳定的情况，确保了结果的可复现性
- 评估效率高：我们的评估采用动态评估的方式进行，第一阶段使用EvalByToolCallGraph进行，根据动作(预测工具名)是否与标准答案一致，决定是否继续调用。同时，过程中采用了决策树剪枝的方式，极大地减少了维护的路径数量，加快了评估速度
- 代码可复用性高：我们所有的请求均采用标准的ToolCalls协议，这使得我们的评估代码具有极高的可复用性。同时，我们为多个未支持ToolCalls协议的开源通用模型和开源专用模型封装了ToolCalls协议，使代码逻辑更加清晰，解决了其他评估框架Prompt和ToolCalls两种调用方式混用，逻辑混乱的问题
- 评估分析维度多：在获取第一阶段的预测和动作级的评估结果后，我们使用AnalysisResult模块对其结果进行细致评估，包含六种维度的分析。据我们所知，在所有Agent评估框架中，我们提供的分析维度最多，结果最为详细。同时，我们的结果均保存在了CSV文件中，方便开发者进行badcase分析
- 可扩展性强：由于我们采用了标准的ToolCalls协议，对于API模型，可使用GPTHandle快速接入；对于新的开源模型，我们会持续更新该仓库，进行接入；对于开发者自己训练的模型，可以参考我们的Handle代码，将Prompt的调用方式封装为ToolCalls协议，即可快速接入验证

整体框架图如下所示：

![Framework](./picture/framework.png)


### 🤖 API Models
本项目支持多种API模型，包括：GPT-4o、GPT-4.1、GPT-o1、Gemini-2.5、Gemini-2.0-flash-thinking、Gemini-1.5、Claude-3.7-Sonnet、Claude-3.5-Sonnet、Mistral-Large等。

以GPT-4o为例，在环境变量中设置以下key

```bash
export OPENAI_MODEL=xxxxxxxxx
export OPENAI_API_KEY=xxxxxxxxx
export OPENAI_BASE_URL=xxxxxxxxx
```

若使用AZURE，则设置以下key

```bash
export AZURE_OPENAI_DEPLOYMENT=xxxxxxxxx
export AZURE_OPENAI_ENDPOINT=xxxxxxxxx
export AZURE_OPENAI_API_KEY=xxxxxxxxx
export AZURE_OPENAI_API_VERSION=xxxxxxxxx
```

之后，使用以下代码请求模型结果，将model设为gpt4o，若测试中途意外停止，可以修改continue_file继续进行测试，这将使得已预测的结果不会重复预测。

upta format
```bash
cd c3_bench/bench_test

python3 request_pipeline_upta.py \
    --model=gpt4o \
    --data_path=./data/C3-Bench.jsonl \
    --output_path=./result \
    --language=en \
    --continue_file=empty.jsonl \
    --remove_role=True \
    --contain_context=True
```

ua format
```bash
cd c3_bench/bench_test

python3 request_pipeline.py \
    --model=gpt4o \
    --data_path=./data/C3-Bench.jsonl \
    --output_path=./result \
    --language=en \
    --continue_file=empty.jsonl \
    --remove_role=True \
    --contain_context=True
```

### 🤗 HuggingFace Models
本项目还支持多种开源专用模型和开源通用模型，具体如下：

开源专用模型包括：xLAM2系列、watt-tool系列、ToolACE2-8B、ToolACE-8B、Hammer2.1系列、xLAM-7b-fc-r-7b、gorilla-openfunctions-v2

开源通用模型包括：Qwen3系列、Qwen2.5系列、Llama-3.3系列、DeepSeek-R1、DeepSeek-V3、GLM-4-9B-Chat

以 [Qwen2.5-7B-Instruct](https://qwen.readthedocs.io/en/latest/framework/function_call.html) 为例：

首先，你需要下载模型到某个地址，之后将该地址替换到c3_bench/tool_calls/tool_model_map.py中的tool_model_path_map变量中。

之后，你可以使用如下代码部署模型。

```bash
python3 web_server.py qwen7b
```

之后，使用以下代码请求模型结果，将model设为qwen7b，将model_url设为您部署机器的ip和端口号，例如：http://111.111.111.111:12345 若测试中途意外停止，可以修改continue_file继续进行测试。

upta格式
```bash
python3 request_pipeline_upta.py \
    --model=qwen7b \
    --data_path=./data/C3-Bench.jsonl \
    --output_path=./result \
    --language=en \
    --model_url=MODEL_URL \
    --continue_file=empty.jsonl \
    --remove_role=True \
    --contain_context=True
```

ua格式
```bash
python3 request_pipeline.py \
    --model=qwen7b \
    --data_path=./data/C3-Bench.jsonl \
    --output_path=./result \
    --language=en \
    --model_url=MODEL_URL \
    --continue_file=empty.jsonl \
    --remove_role=True \
    --contain_context=True
```

最后，在c3_bench/bench_test/handle/handles.py中列举了我们实现的10+种的Handle，想测试其他模型的话，可以查阅该文件，获取model参数的设置信息。另外，想加入自己实现的Handle，也可以在该文件中添加。

## 💫 Evaluation
使用以下代码对模型预测结果进行评估，将PREDICT_DATA_FILE填写为上一步./result目录中对应的预测文件，评估结果包括：动作类型与层的矩阵准确率、动作类型与层各自的准确率、多工具调用结果分析、错误类型分析、真伪多轮准确率、真多轮子类型准确率、参数错误类型分析。

详细结果会输出到data_with_details.csv中。

```bash
cd c3_bench/bench_test

python3 analysis_result.py \
    --data_file PREDICT_DATA_FILE \
    --output_csv_flag=True \
    --output_csv_path=./data_with_details.csv
```

特别的，我们将论文中汇报的所有模型的结果都持久化的保存在了c3_bench/bench_test/result目录下，方便每个人直接复现论文中的结果，便利相关的Agent模型研发同学分析badcase，以及为想快速学习评估代码的同学提供了便利的方式，而不用重新进行推理。

如下为一个复现 gpt-4o 结果的示例

```bash
python3 analysis_result.py \
    --data_file ./result/2025-04-28-18:03:45_89a6a1_gpt4o_en_remove_role_contain_context_history_with_planner_tool.jsonl \
    --output_csv_flag=True \
    --output_csv_path=./data_with_details.csv
```

此外，我们还支持了同时对多个模型的预测结果进行评估，这进一步增加了易用性。

如下为一个同时复现 gpt-4o 和 gpt-o1 结果的示例，多个文件使用,拼接

```bash
python3 analysis_result.py \
    --data_file ./result/2025-04-28-18:03:45_89a6a1_gpt4o_en_remove_role_contain_context_history_with_planner_tool.jsonl,./result/2025-04-29-17:29:50_01f8b7_gpt4o1_en_remove_role_contain_context_history_with_planner_tool.jsonl \
    --output_csv_flag=True \
    --output_csv_path=./data_with_details.csv
```

## 🧠 Controllable Multi Agent Data Generation Framework

![MultiAgent](./picture/multi_agent2.png)

本论文设计的是一个可控的多智能体数据生成框架，相比其他框架，有如下八大独特的优势：

- **可控任务生成**：在生成每一轮任务时，能够可控地指定当前需要生成的任务类型，包括单工具调用、多工具调用、澄清后调用工具、闲聊四个类型。也正是该优势，让我们的框架能够遍历所有可能的动作空间，构建出无偏的数据，这一点在大模型领域十分重要，无论是训练还是测试，数据的无偏性直接决定了模型的效果是否优秀、评估是否可靠
- **指定数量任务生成**：我们的框架能够生成任务数量的任务，搭配第一点优势可控任务生成，生成的数据能够覆盖任意数量任务的所有可能的动作空间
- **多样化任务生成**：在第一轮任务生成时，我们的框架能够生成多个具有不同语气、长度、主题/实例、场景、角色身份的任务，并从中随机挑选一个继续进行生成，具有极高的多样性，贴近人类真实分布
- **真多轮任务生成**：在后续轮次任务生成时，我们的框架是目前唯一能够可控的生成真多轮任务的框架，我们能够生成包括指代理解、省略成分、长期记忆这三种核心的真多轮任务，并且我们提供了几十种few-shot来指导模型生成真多轮任务，每次生成时随机选择其中一个示例，大大提高了数据多样性和生成有效率
- **丰富的智能体**：我们设计了五大类型的智能体，包括User智能体、AI智能体、Planner智能体、Tool智能体、Checker智能体，二级类型共有15种，多样化的智能体保证了我们的框架生成数据的多样性和高质量
- **强力的Planner**：我们设计的Planner Agent是目前所有智能体框架中唯一能够决策复杂串并行多工具调用任务的智能体，我们通过编写 4000 字以上的Prompt，让其按照我们设定的指导意见进行决策，具备极高的决策准确率
- **可靠的Checker**：我们设计的Checker Agent是目前唯一会对并行调用逻辑进行检查的智能体，同时我们编写了几十种规则，以检查Planner可能犯的低级错误，并提供评论意见，让其能够进行反思。最终我们的Planner Agent 和 Checker Agent搭配使用，在没有人工干预的情况下，决策准确率在90%以上，据我们所知，这是目前所有多智能体数据生成框架中最高的。
- **任意模型指定**：我们的框架能够使用任意LLM来作为智能体的基座模型，研究者可以使用任意一个他们觉得更强的模型，来获得更好的效果
- **双语支持**：我们的框架支持英文和中文两种语言，能够生成中英两种语言的数据，据我们所知，这同样也是目前唯一一个支持双语数据生成的框架

![AgentFamily](./picture/agent_family.png)

### ⚡️ Quickstart

以所有智能体均使用AZURE GPT-4o作为基座模型，并且生成中文的数据为例。首先，在环境变量中设置以下key

```bash
export AZURE_OPENAI_DEPLOYMENT=xxxxxxxxx
export AZURE_OPENAI_ENDPOINT=xxxxxxxxx
export AZURE_OPENAI_API_KEY=xxxxxxxxx
export AZURE_OPENAI_API_VERSION=xxxxxxxxx
export LANGUAGE=zh
```

本论文的核心创新点在于，我们提出的 C3-Bench 能够覆盖任意数量任务的所有可能的动作空间，并且除第一轮以外全部为真多轮任务，因此我们的框架能够支持生成任意数量任务的数据，此处我们以生成四个任务为例，参考如下代码：
```bash
cd multi_agent

python3 generate.py \
    --layer_num_total 4 \
    --user_model ["gpt4o"] \
    --planner_model "gpt4o" \
    --tool_model "gpt4o" \
    --agent_model "gpt4o" \
    --checker_model "gpt4o"
```
特别的，我们保存了三种格式的数据，包括：原始生成数据、精简后的数据(删除checker message和角色切换 message)、各个智能体的抓取数据，以供需要的研究人员使用。

最后，展示一下我们生成的一个实际case的部分结果，可以发现，Continue Question User Agent 生成了一个指代理解类型的真多轮任务 "第三张壁纸的上传者是谁？"，这意味着在解决该任务时，需要模型参考上文内容，才能获取第三张壁纸的ID 778899，从而继续调用获取壁纸详细信息的工具getWaifuDetails。

```
用户: 我需要最新的5张动漫壁纸。

Planner：getWaifuImages(limit=5, tags=["动漫壁纸"])

Tool：...

Planner：prepare_to_answer(answer_type=tool)

Agent助手:

以下是最新的5张动漫壁纸:
1. 壁纸ID: 112233
 - [查看壁纸](https://wallhaven.cc/w/112233)
 - ![缩略图](https://wallhaven.cc/thumb/small/112233.jpg)
 - 分辨率: 1920x1080
2. 壁纸ID: 445566
 - [查看壁纸](https://wallhaven.cc/w/445566)
 - ![缩略图](https://wallhaven.cc/thumb/small/445566.jpg)
 - 分辨率: 2560x1440
3. 壁纸ID: 778899
 - [查看壁纸](https://wallhaven.cc/w/778899)
 - ![缩略图](https://wallhaven.cc/thumb/small/778899.jpg)
 - 分辨率: 3840x2160
4. 壁纸ID: 101112
 - [查看壁纸](https://wallhaven.cc/w/101112)
 - ![缩略图](https://wallhaven.cc/thumb/small/101112.jpg)
 - 分辨率: 1920x1080
5. 壁纸ID: 131415
 - [查看壁纸](https://wallhaven.cc/w/131415)
 - ![缩略图](https://wallhaven.cc/thumb/small/131415.jpg)
 - 分辨率: 2560x1440

你可以点击链接查看完整壁纸。希望你喜欢这些壁纸！如果需要更多帮助，请告诉我。

Continue Question User Agent Generate:
用户: 第三张壁纸的上传者是谁? 

Planner：getWaifuDetails(image_id=778899)
```

需要说明的是，即便我们的框架能够生成这样优秀的真多轮任务，但是真多轮任务生成对LLM来说仍十分困难，因此我们前面提到的通过多位专家人工标注，才将准确率从不足60%提升到100%，这也包括将LLM生成的伪多轮任务修改为真多轮任务。

## 🔎 Citation

```
@misc{yu2025c3bench,
      title={C^3-Bench: The Things Real Disturbing LLM based Agent in Multi-Tasking}, 
      author={Peijie Yu and Yifan Yang and Jinjian Li and Zelong Zhang and Haorui Wang and Xiao Feng and Feng Zhang},
      year={2025},
      eprint={2505.18746},
      archivePrefix={arXiv},
      primaryClass={cs.AI},
      url={https://arxiv.org/abs/2505.18746}, 
}
```