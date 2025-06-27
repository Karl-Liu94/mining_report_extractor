# 🏔️ 矿山储量核实报告信息提取工具

> 基于AI的智能矿山报告分析系统，支持自动信息提取和智能对话问询

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![OpenAI](https://img.shields.io/badge/OpenAI-API-green.svg)](https://openai.com/)
[![Gemini](https://img.shields.io/badge/Google-Gemini-orange.svg)](https://ai.google.dev/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 📋 项目简介

本项目是一个专业的矿山储量核实报告信息提取工具，利用先进的AI技术（OpenAI GPT和Google Gemini）自动分析PDF格式的矿山报告，提取关键信息并支持智能对话问询。

### ✨ 核心功能

- 🔍 **智能信息提取**：自动从PDF报告中提取结构化信息
- 💬 **流式对话问询**：支持实时对话，深度分析报告内容  
- 🤖 **多AI提供商**：支持OpenAI和Google Gemini双平台
- 📊 **结构化输出**：标准JSON格式，便于后续处理
- 🗂️ **完整数据模型**：覆盖报告信息、矿权信息、资源信息等

### 🎯 提取信息类别

- **报告信息**：报告名称、编制单位、编制日期
- **矿权信息**：矿权名称、位置、类型、编号、有效期等
- **资源信息**：矿种、各类资源量（推断/控制/探明）、品位等
- **矿体分布**：矿体编号、规模、走向、倾角等几何参数
- **其它信息**：报告中的补充价值信息

## 🚀 快速开始

### 环境要求

- Python 3.8+
- OpenAI API Key（可选）
- Google Gemini API Key（可选）

### 安装依赖

```bash
# 克隆项目
git clone https://github.com/yourusername/mining-report-extractor.git
cd mining-report-extractor

# 安装依赖
pip install -r requirements.txt
```

### 配置API密钥

创建 `.env` 文件：

```bash
# OpenAI配置（支持信息提取和流式对话）
OPENAI_API_KEY=your_openai_api_key_here

# Gemini配置（仅支持信息提取）
GEMINI_API_KEY=your_gemini_api_key_here
```

### 运行程序

```bash
# 标准版本（非流式对话）
python mining_report_extractor_with_conversation.py

# 流式输出版本（推荐）
python mining_report_extractor_stream.py
```

## 📖 使用指南

### 基本操作流程

1. **选择AI提供商**
   ```
   🤖 请选择AI提供商:
   1. Gemini (Google) - 仅支持信息提取
   2. OpenAI - 支持信息提取和对话功能
   ```

2. **选择模型**
   - **Gemini**: `gemini-2.5-flash`, `gemini-2.5-pro`
   - **OpenAI**: `o4-mini`, `o3`, `gpt-4.1-nano`

3. **输入PDF文件路径**
   ```bash
   📁 请输入PDF文件路径: /path/to/your/report.pdf
   ```

4. **查看提取结果**
   - 终端显示结构化摘要
   - 自动保存JSON格式结果文件

5. **进入对话模式**（仅OpenAI）
   - 支持关于报告内容的任意问询
   - 实时流式输出，响应迅速
   - 输入 `exit` 或 `退出` 结束对话

### 示例对话

```
🙋 您的问题: 这个矿山的主要矿种是什么？

🤖 AI回答:
根据报告内容，该矿山的主要矿种是铜矿。报告显示这是一个铜矿详查项目，
主要开采铜矿资源，同时还包含一些伴生矿物...
```

## 📁 项目结构

```
mining-report-extractor/
├── 📁 dataset/                          # 示例数据集
│   ├── json_format.txt                  # JSON格式说明
│   ├── 泽华长石矿核实报告2022.7.22.pdf    # 示例报告1
│   ├── 云南省洱源县丕坪铜矿详查报告.pdf     # 示例报告2
│   └── 2016年储量年报.pdf               # 示例报告3
├── 📄 mining_report_extractor_with_conversation.py  # 标准版本
├── 📄 mining_report_extractor_stream.py             # 流式输出版本
├── 📄 requirements.txt                  # 项目依赖
├── 📄 README.md                        # 项目说明
├── 📄 .gitignore                       # Git忽略文件
└── 📄 .env                            # 环境变量配置（需自建）
```

## 🔧 技术架构

### 数据模型设计

使用 Pydantic 构建的完整数据模型：

```python
class MiningReport(BaseModel):
    """矿山储量核实报告完整模型"""
    报告信息: Optional[ReportInfo] = None
    矿权信息: Optional[MiningRightsInfo] = None  
    资源信息: Optional[List[ResourceInfo]] = None
    矿体分布: Optional[List[OreBodyDistribution]] = None
    其它信息: Optional[str] = None
```

### AI服务商支持

| 功能 | OpenAI | Gemini |
|------|--------|--------|
| 信息提取 | ✅ | ✅ |
| 流式对话 | ✅ | ❌ |
| 大文件支持 | ✅ | ✅ |
| 结构化输出 | ✅ | ✅ |

### 核心特性

- **抽象基类设计**：易于扩展新的AI提供商
- **流式输出**：实时响应，改善用户体验
- **错误处理**：完善的异常处理和用户提示
- **资源管理**：自动清理临时文件
- **类型安全**：完整的类型注解和验证

## 📊 输出示例

### JSON结构示例

```json
{
  "报告信息": {
    "报告名称": "云南省洱源县丕坪铜矿详查报告",
    "编制单位": "云南地质工程勘察院",
    "编制日期": "2023年8月"
  },
  "矿权信息": {
    "矿权名称": "洱源县丕坪铜矿",
    "矿权位置": "云南省大理州洱源县",
    "勘查程度": "详查",
    "矿权类型": "探矿权",
    "矿区面积": "2.85平方千米"
  },
  "资源信息": [
    {
      "矿种": "铜矿",
      "资源量情况": {
        "推断资源量": {
          "矿石量": "128.5万吨",
          "金属量": "3250吨",
          "品位": "0.68%"
        },
        "总计": {
          "矿石量": "128.5万吨", 
          "金属量": "3250吨",
          "品位": "0.68%"
        }
      }
    }
  ]
}
```

## 🛠️ 开发指南

### 添加新的AI提供商

1. 继承 `BaseMiningReportExtractor` 基类
2. 实现 `extract_from_file` 方法
3. 在 `create_extractor` 工厂函数中注册
4. 添加相应的模型列表和配置

### 自定义数据模型

可以根据需要扩展或修改 Pydantic 数据模型，支持更多字段或不同的报告格式。

## 🤝 贡献指南

欢迎提交 Issue 和 Pull Request！

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`) 
5. 开启 Pull Request

## 📝 更新日志

### v2.0.0 (2024-12-19)
- ✨ 新增流式输出对话功能
- 🔧 简化用户交互流程
- 📊 优化数据模型结构
- 🐛 修复多项已知问题

### v1.0.0 (2024-12-01)
- 🎉 项目首次发布
- ✅ 支持基础信息提取功能
- ✅ 支持OpenAI和Gemini双平台

## 📄 许可证

本项目基于 MIT 许可证开源 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 🆘 技术支持

如遇到问题，请：

1. 查看 [Issues](https://github.com/yourusername/mining-report-extractor/issues) 页面
2. 提交新的 Issue 描述问题
3. 参考项目文档和示例代码

## 🙏 致谢

感谢以下技术和平台的支持：

- [OpenAI](https://openai.com/) - 提供强大的GPT模型
- [Google AI](https://ai.google.dev/) - Gemini模型支持
- [Pydantic](https://pydantic.dev/) - 数据验证框架
- 所有贡献者和用户的支持

---

⭐ 如果这个项目对您有帮助，请给我们一个星标！
**项目地址**: [mining_file_recognize](https://github.com/Karl-Liu94/mining_file_recognize.git) 