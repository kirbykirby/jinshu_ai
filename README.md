<div align="center">
<h1> 晋书AI </h1>

[**English**](README_EN.md) | **简体中文**
</div>

---

## 🤓 序
余以为晋氏之祚，钟灵毓秀。然天降祸乱，四海板荡，五胡扛鼎，六宗失序，七庙隳尊。

有感于斯，常思古人兴亡之迹。

时甲子之岁，天下多故，瘟疫盛行。余闭门不出，得王氏《魏晋南北朝史》一书，昼夜研读，辄有会心。

惜乎记性驽钝，览之既久，多所遗忘。遂发愤著述，立志传播华夏文明于四海。

余不揣固陋，创设西洋Youtube频道，以英语阐发我朝故事。每于撰文之际，常得《晋书》之助。

初不谙文言，乃潜心钻研，译为英文。盖以浅白之言解深奥之理，始知古人用意之所在。

然视频剪裁，殊为劳费。虽暂辍其事，而译述之志未改。

今春习得Python之术，颇究AI之理，然精力有限，此业遂搁。

近日公暇，忽念AI之用，正可助吾译事。《廿四史》洋洋四千万言，而余独钟情《晋书》百三卷，或亦天意使然。

古人云："善始者实繁，克终者盖寡。"今借AI之力，完此未竟之业，岂不美哉！故吾用二日之时，作此脚本。

吾虽不才，愿效玄龄之志，述晋氏盛衰，明得失之由。AI为助，古今相通，庶几不负此心耳。

## 🤔 介绍
用人话说，这就是一个用AI翻译md文件，把译文输出到docx并格式化的工具。
其实你翻译啥文档都行。

## 📑 使用教程
1. [点我注册](https://api.bltcy.ai/register?aff=q3ue)柏拉图中转站，获取密钥。
   - 可使用OpenAI、Anthropic、Google等公司之大模型
   - 价格比官方便宜60%以上。
2. 可选：使用OpenAI密钥（需要修改转发地址）
3. 根目录创建`.env`文件，输入汝之密钥于`BLT_KEY`。
4. 安装[`uv`库](https://github.com/astral-sh/uv)，[Windows使用者点我下载](https://github.com/astral-sh/uv/releases/download/0.5.8/uv-x86_64-pc-windows-msvc.zip)。
5. 按需修改`main.py`之参数，命令行运行`uv run main.py`进行翻译。

## 📚 获取数据
[《晋书》原始文本](https://ctext.org/wiki.pl?if=gb&res=788577&remap=gb)来自`中国哲学书电子化计划`。

该网站**严禁**自动爬取，需手动获取数据。
1. 打开一章节，Ctrl+A，Ctrl+C，Ctrl+V至md文件。
2. 运行`clean_md.py`清洗md文件。

## 💵 成本
以翻译《慕容暐载记》为例：

原文8665字，共花费2.66元，每千字的费用是0.307元（0.04美元）。

按照这个价格计算，翻译完整部《晋书》（1,158,126字）大约需要355.54元（48.7美元）。

## ⚠ 注意事项
### 1. 文言文常省略主语
填写`init_translator_and_translate`函数的`subject`参数可以避免错译主语。例子：
```
原文：
弱冠游于洛阳，坐事当诛，亡匿朝鲜，遇赦而归。（《刘曜载记》）

错误翻译：
At the age of twenty, [incorrect subject] traveled to Luoyang, where [incorrect subject] faced execution for an offense but fled to Joseon.

正确翻译：
At the age of twenty, Liu Yao traveled to Luoyang, where he faced execution for an offense but fled to Joseon.
```

### 2. 直译人名/地名用字偶尔造成错译
例子：
```
原文：
黄石屠各路松多起兵于新平、扶风，聚众数千，附于南阳王保。（《刘曜载记》）

错误翻译：
Huangshi slauthered Lusongduo, who raised an army in Xinping and Fufeng, gathering several thousand followers and allied with Prince of Nanyang Bao.
（错误直译“屠”字为"slaugher"。“屠各”为匈奴部落名，专有名词应音译。

正确翻译：
In Huangshi, Lu Songduo of the Tuge raised an army in Xinping and Fufeng, gathering several thousand followers and allied with Prince of Nanyang Bao.
```

### 3. 翻译专有名词时不一致
```
原文：
使持节

翻译：
Envoy with Imperial Insignia
Envoy with Imperial Credentials
Bearer with Imperial Insignia
...
```
可能的解决方案：告诉AI直接给出原词，然后用表格将其替换为英语翻译。


## 💬 项目结构
```
|- README.md  # 项目介绍
|- main.py  # 主脚本
|- translator  # 翻译模块
|  |- __init__.py  # 初始化文件
|  |- chatbot.py  # 聊天机器人模块
|  |- config.py  # 配置文件
|  |- formatter.py  # 格式化模块
|  |- prompts.py  # 指令模块
|  |- translator.py  # 翻译脚本
|  |- utils.py  # 工具模块
|
|- pyproject.toml  # 项目依赖文件
|- uv.lock  # uv依赖文件
```

## 🌏 未来展望
- [ ] 在上下文添加自定义知识库
- [ ] 保持名词翻译一致（如官职名）
- [ ] 自动建立人物索引
- [ ] 支持更多翻译引擎
- [ ] 支持原生Anthropic API
- [ ] 加入UI界面
