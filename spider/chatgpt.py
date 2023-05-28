import os
os.environ["OPENAI_API_KEY"] = "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" # from 阿飞

# from 克拉
# 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 # 已用完
# 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
# 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
# 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
# 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

from langchain.llms import OpenAI
import time

def callChatGPTApi(items, path):
    promptSuffix = '''
    你是一个中文新闻编辑师，请用一句话总结上面新闻，30字左右。总结时请参考以下例子。

    例子：
    1.微软的一个华人研究团队发布了一项新型基准测试 AGIEval，专门用于对基础模型的类人能力做准确考察（涵盖高考、法学入学考试、数学竞赛和律师资格考试等）。

    2.北京发布《促进通用人工智能创新发展措施》，提出21项措施推动大模型发展，助力各行业效率革命和体验升级。

    3.中国人民大学和华为联合发布可解释推荐数据集REASONER。REASONER数据集推动可解释推荐领域发展，提供多模态、多方面的解释真值，促进算法评估和推荐系统研究。

    4.2023年NeRF技术取得显著进步，结合抗混叠和快速训练，错误率降低76%、训练速度提高22倍，有望应用于VR等领域。

    5.欧洲议会正就全球首部人工智能（AI）法案展开大规模协商，光修正案就有一千多项，创下了欧洲议会史上之最。

    6.OpenAl联合创始人山姆·阿尔特曼的加密货币项目“世界币（WorldCoin）”推出新产品——加密钱包World App，希望成为AI时代的“身份证”。

    7.毕马威与微软合作，全面应用生成式AI，提升工作效率和客户体验。

    8.SAP与微软合作推出生成式AI服务加速人力资源流程，应用于招聘和员工学习。
    '''

    llm = OpenAI(model_name="text-davinci-003", max_tokens=512)
    results = []

    for i in range(len(items)):
        print("[" + str(i+1) + "] >>>>>>>>>> " + '%s' % time.strftime("%H:%M:%S", time.localtime()))
        result = llm(items[i][:1024] + promptSuffix)
        print(result)
        results.append(result)

    writeToFile(results, path)

def writeToFile(results, path):
    with open(path, 'a+') as f:
        for i in range(len(results)):
            f.write("[" + str(i) + "]\n")
            f.write(results[i] + "\n")
