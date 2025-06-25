# 矿山储量核实报告信息提取器 🏔️

一个基于 AI 大模型的智能 PDF 文档信息提取工具，专门用于从矿山储量核实报告中提取结构化信息。支持 **Gemini** 和 **OpenAI** 两大 AI 服务商，其中 OpenAI 版本还具备多轮对话功能。

## 🌟 主要特性

- **🤖 双 AI 支持**：支持 Google Gemini 和 OpenAI 两大 AI 服务商
- **💬 智能对话**：OpenAI 版本支持基于报告内容的多轮问答对话
- **🎯 灵活模型选择**：提供预设模型列表，支持自定义模型名称
- **📄 智能 PDF 解析**：强大的文档理解和信息提取能力
- **🔧 统一 API 接口**：无论使用哪种 AI，调用方式完全一致
- **🗂️ 结构化输出**：使用 Pydantic 模型确保数据质量和一致性
- **🇨🇳 中文优化**：专门针对中文矿山报告进行优化
- **💎 多矿种支持**：支持主矿种和伴生矿种的资源量统计
- **📊 完整信息覆盖**：提取报告信息、矿权信息、资源信息、矿体分布等全面数据
- **🔒 安全配置**：使用 .env 文件统一管理 API 密钥

## 📋 提取信息类型

### 报告信息
- 报告名称
- 编制单位
- 编制日期

### 矿权信息
- 矿权名称、位置、编号
- 勘查程度（普查/详查/勘探）
- 矿权类型（探矿权/采矿权）
- 矿权起始/截止日期
- 生产规模、矿区面积、矿区海拔
- 以往勘查工作

### 资源信息
- 矿种（金矿、铜矿、银矿等）
- 资源量分类统计：
  - 推断资源量（333类别）
  - 控制资源量（332类别）
  - 探明资源量（331类别等）
  - 总计
- 每个类别包含：矿石量、金属量、品位

### 矿体分布信息
- 矿体编号、名称
- 矿体几何特征（长度、宽度、厚度、走向、倾角）
- 矿体规模（面积、体积）
- 矿体资源量（矿石量、金属量、品位）

## 🚀 快速开始

### 环境要求

- Python 3.8+
- Google Gemini API 密钥 或 OpenAI API 密钥（至少一个）

### 安装依赖

```bash
pip install -r requirements.txt
```

### 配置 API 密钥

创建 `.env` 文件并填入您的 API 密钥：

```bash
# API 密钥配置文件
# 请填入您的实际 API 密钥

# OpenAI API 密钥（支持对话功能）
OPENAI_API_KEY=your_openai_api_key_here

# Gemini API 密钥
GEMINI_API_KEY=your_gemini_api_key_here
```

### 交互式使用（推荐）

运行主程序：
```bash
python mining_report_extractor_with_conversation.py
```

程序流程：
1. 选择 AI 服务商（Gemini/OpenAI）
2. 选择提取模型
3. 输入 PDF 文件路径
4. 自动提取并显示结果
5. **（仅 OpenAI）** 选择是否进入对话模式
6. **（如进入对话）** 选择对话模型并开始问答

### 编程式使用

```python
from mining_report_extractor_with_conversation import create_extractor

# 方式1：交互式选择
extractor = create_extractor()
result = extractor.extract_from_file("your_report.pdf")

# 方式2：直接指定
extractor = create_extractor("gemini", "gemini-2.5-flash")
result = extractor.extract_from_file("your_report.pdf")

# 方式3：OpenAI 带对话功能
extractor = create_extractor("openai", "o4-mini")
result = extractor.extract_from_file("your_report.pdf")
# 启动对话（可选择不同模型）
extractor.start_conversation("o3-pro")
```

## 💬 对话功能特性

**仅 OpenAI 版本支持**

- **多轮对话**：基于已上传的报告内容进行连续问答
- **上下文记忆**：AI 会记住之前的问答历史
- **模型切换**：可为对话选择不同于提取的模型
- **专业回答**：基于地质和矿业领域专业知识回答问题

### 对话示例

```
🙋 您的问题: 这个矿山的金矿资源量有多少？

🤖 AI回答:
根据报告内容，该金矿的总资源量为：
- 矿石量：23.5万吨
- 金属量：965公斤
- 平均品位：4.11克/吨

🙋 您的问题: 这个品位在行业内算什么水平？

🤖 AI回答:
4.11克/吨的金品位在行业内属于中等偏上水平...
```

## 🔧 支持的模型

### Gemini 模型
- `gemini-2.5-flash`（默认，速度快）
- `gemini-2.5-pro`（质量高）
- 支持自定义模型名称

### OpenAI 模型
- `o4-mini`（默认，经济实用）
- `o3`（平衡性能）
- `o3-pro`（最高质量）
- 支持自定义模型名称

## 🏗️ 项目架构

### 文件结构
```
mining_file_recognize/
├── mining_report_extractor_with_conversation.py  # 🌟 主程序（含对话功能）
├── mining_report_extractor_unified.py            # 统一版本（无对话）
├── mining_report_extractor_gemini.py             # Gemini 专用版本
├── mining_report_extractor_openai.py             # OpenAI 专用版本
├── OpenAI_APIs_for_conversation_state.py         # OpenAI 对话 API 示例
├── .env                                           # API 密钥配置文件
├── requirements.txt                               # 依赖列表
├── README.md                                     # 项目说明
└── dataset/
    └── json_format.txt                           # 输出格式示例
```

### 核心架构设计

```python
# 抽象基类
class BaseMiningReportExtractor(ABC):
    @abstractmethod
    def extract_from_file(self, file_path: str) -> MiningReport:
        pass

# 具体实现
class GeminiMiningReportExtractor(BaseMiningReportExtractor):
    # Gemini API 实现

class OpenAIMiningReportExtractorWithConversation(BaseMiningReportExtractor):
    # OpenAI API 实现 + 对话功能
    def start_conversation(self, conversation_model: Optional[str] = None):
        # 多轮对话实现
```

## 📊 输出格式示例

```json
{
  "报告信息": {
    "报告名称": "四川省石棉县薛家崖金矿详查报告",
    "编制单位": "四川省地质矿产勘查开发局区域地质调查队",
    "编制日期": "二〇一八年六月"
  },
  "矿权信息": {
    "矿权名称": "薛家崖金矿",
    "矿权位置": "四川省石棉县",
    "勘查程度": "详查",
    "矿权类型": "探矿权",
    "矿权编号": "T51120100102038390",
    "矿权起始日期": "2018年2月15日",
    "矿权截止日期": "2020年2月15日",
    "生产规模": null,
    "矿区面积": "1.06km²",
    "矿区海拔": "2800-3200m",
    "以往勘查工作": "区域地质调查、化探、物探等前期工作"
  },
  "资源信息": [
    {
      "矿种": "金矿",
      "资源量情况": {
        "推断资源量": {
          "矿石量": "23.5万吨",
          "金属量": "965kg",
          "品位": "4.11g/t"
        },
        "控制资源量": {
          "矿石量": "15.2万吨",
          "金属量": "624kg",
          "品位": "4.11g/t"
        },
        "总计": {
          "矿石量": "38.7万吨",
          "金属量": "1589kg",
          "品位": "4.11g/t"
        }
      }
    }
  ],
  "矿体分布": [
    {
      "矿体编号": "Ⅰ号矿体",
      "矿体名称": "主矿体",
      "矿体长度": "800m",
      "矿体宽度": "200m",
      "矿体厚度": "3.5m",
      "矿体走向": "NE45°",
      "矿体倾角": "60°",
      "矿体面积": "0.16km²",
      "矿体品位": "4.2g/t"
    }
  ],
  "其它信息": "矿床类型为石英脉型金矿，成矿地质条件良好..."
}
```

## 🛠️ 开发指南

### 扩展新的 AI 服务商

1. 继承 `BaseMiningReportExtractor` 类
2. 实现 `extract_from_file` 方法
3. 在 `create_extractor` 工厂函数中添加新的分支

### 自定义数据模型

修改 Pydantic 模型以适应特定需求：
```python
class CustomReportInfo(BaseModel):
    # 添加自定义字段
    custom_field: Optional[str] = None
```

## ❓ 常见问题

### Q: 如何获取 API 密钥？
**A**: 
- **OpenAI**: 访问 [OpenAI Platform](https://platform.openai.com/) 注册并获取 API 密钥
- **Gemini**: 访问 [Google AI Studio](https://makersuite.google.com/) 获取 API 密钥

### Q: 哪个 AI 服务商效果更好？
**A**: 
- **Gemini**: 处理中文文档效果好，速度快，成本低
- **OpenAI**: 信息理解能力强，支持对话功能，适合复杂查询

### Q: 对话功能支持哪些问题？
**A**: 
- 报告内容查询（资源量、矿权信息等）
- 数据解释和分析
- 专业术语解释
- 矿山评估建议
- 任何基于已上传报告的问题

### Q: 文件大小有限制吗？
**A**: 
- **Gemini**: 自动处理大文件（>20MB 使用 File API）
- **OpenAI**: 支持大文件上传

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

1. Fork 本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 📞 联系方式

如有问题或建议，请通过以下方式联系：

- 提交 [GitHub Issue](https://github.com/your-username/mining_file_recognize/issues)
- 发送邮件至：your-email@example.com

## 🔄 更新日志

### v2.0.0 (最新)
- ✨ 新增 OpenAI 多轮对话功能
- 🎯 支持对话前选择不同模型
- 🔧 优化代码结构和错误处理
- 📝 完善文档和示例

### v1.0.0
- 🚀 初始版本发布
- 🤖 支持 Gemini 和 OpenAI 双 AI 服务商
- 📊 完整的矿山报告信息提取功能
- 🗂️ 结构化数据输出

---

**⭐ 如果这个项目对您有帮助，请给我们一个 Star！**

**作者**: Karl Liu  
**联系**: [GitHub Issues](https://github.com/Karl-Liu94/mining_file_recognize/issues)  
**项目地址**: [mining_file_recognize](https://github.com/Karl-Liu94/mining_file_recognize.git) 
**项目地址**: [mining_file_recognize](https://github.com/Karl-Liu94/mining_file_recognize.git) 