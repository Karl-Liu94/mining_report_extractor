# 矿山储量核实报告信息提取工具 🏔️

一个基于大语言模型的智能PDF文档信息提取工具，专门用于从矿山储量核实报告中提取结构化信息。支持 **Google Gemini** 和 **OpenAI** 两大AI服务商，其中OpenAI版本还具备流式对话功能。

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🌟 核心特性

### 🤖 双AI支持
- **Google Gemini**: 高效的文档分析和信息提取
- **OpenAI**: 支持信息提取 + 流式对话问答功能

### 💬 智能对话（OpenAI专属）
- 基于已提取报告内容进行多轮问答
- 流式输出，实时显示AI回答
- 支持地质和矿业领域专业问题

### 📄 强大的文档处理
- 智能PDF解析和内容理解
- 针对中文矿山报告优化
- 支持大文件处理（自动选择最优上传方式）

### 🎯 结构化输出
- 使用Pydantic模型确保数据质量
- 标准化JSON格式输出
- 支持多矿种和伴生矿种统计

## 📋 提取信息类型

### 1. 报告基本信息
```
📋 报告信息
├── 报告名称      # 报告的完整标题
├── 编制单位      # 编制机构名称（非委托单位）
└── 编制日期      # 报告编制时间
```

### 2. 矿权详细信息
```
⛏️ 矿权信息
├── 矿权名称      # 矿权主体名称
├── 矿权位置      # 地理位置
├── 勘查程度      # 普查/详查/勘探
├── 矿权类型      # 探矿权/采矿权
├── 矿权编号      # 官方编号
├── 矿权起始日期   # 开始日期
├── 矿权截止日期   # 结束日期
├── 生产规模      # 年产量（仅采矿权）
├── 矿区面积      # 总面积（含单位）
├── 矿区海拔      # 海拔高度
└── 以往勘查工作   # 历史工作概述
```

### 3. 资源量统计信息
```
💎 资源信息（支持多矿种）
├── 矿种          # 如"金矿"、"铜矿"、"银矿"
└── 资源量情况
    ├── 推断资源量 (333)    ├── 矿石量
    ├── 控制资源量 (332)    ├── 金属量
    ├── 探明资源量 (331等)  └── 品位
    └── 总计
```

### 4. 矿体分布信息
```
🗺️ 矿体分布（支持多矿体）
├── 矿体编号      # 矿体标识
├── 矿体名称      # 矿体名称
├── 几何特征      # 长度/宽度/厚度/走向/倾角
├── 规模信息      # 面积/体积
└── 资源量       # 矿石量/金属量/品位
```

## 🚀 快速开始

### 1. 环境准备

**系统要求:**
- Python 3.8 或更高版本
- 至少一个AI服务商的API密钥

**安装依赖:**
```bash
pip install -r requirements.txt
```

### 2. 配置API密钥

复制环境变量模板并填入您的API密钥：

```bash
# 复制模板文件
cp env_template.txt .env

# 编辑 .env 文件，填入实际的API密钥
```

`.env` 文件内容示例：
```bash
# OpenAI API 密钥（支持对话功能）
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxx

# Gemini API 密钥
GEMINI_API_KEY=xxxxxxxxxxxxxxxxxxxxx
```

### 3. 运行程序

**交互式使用（推荐）:**
```bash
python mining_report_extractor_stream.py
```

**程序操作流程:**
1. **选择AI提供商** → Gemini（仅提取）或 OpenAI（提取+对话）
2. **选择模型** → 从预设列表选择或输入自定义模型名
3. **输入PDF路径** → 支持拖拽文件或手动输入路径
4. **自动处理** → 上传、分析、提取信息
5. **查看结果** → 控制台显示摘要 + JSON文件保存
6. **（OpenAI专属）对话模式** → 可选进入问答环节

## 💬 对话功能详解

### 特性说明
- **仅OpenAI版本支持**
- 基于已上传的报告内容进行智能问答
- 支持多轮连续对话，具有上下文记忆
- 流式输出，实时显示AI回答过程

### 使用示例

```
💬 进入对话模式
🤖 使用模型: o4-mini
==================================================
您现在可以询问关于这份矿山报告的任何问题。
输入 'exit' 或 '退出' 结束对话。
==================================================

🙋 您的问题: 这个矿山的主要矿种是什么？

🤖 AI回答:
--------------------------------------------------
根据报告内容，该矿山的主要矿种是金矿，同时还有银作为伴生矿种。

具体资源量情况：
- 金矿总资源量：23.5万吨矿石，965公斤金属，平均品位4.11克/吨
- 银矿伴生资源量：965公斤金属，平均品位41.1克/吨
--------------------------------------------------

🙋 您的问题: 这个品位在行业内算什么水平？

🤖 AI回答:
--------------------------------------------------
金品位4.11克/吨在行业内属于中等偏上水平：

1. **国际标准对比**：
   - 低品位金矿：< 2克/吨
   - 中等品位：2-5克/吨  ← 当前矿山
   - 高品位金矿：> 5克/吨

2. **开采可行性**：
   - 该品位已达到经济开采标准
   - 具备较好的商业开发价值

3. **技术建议**：
   - 建议采用常规选矿工艺
   - 可考虑规模化开采
--------------------------------------------------

🙋 您的问题: exit

👋 结束对话，感谢使用！
```

## 🔧 支持的AI模型

### Google Gemini
| 模型名称 | 特点 | 适用场景 |
|---------|------|----------|
| `gemini-2.5-flash` | 速度快，成本低 | 日常文档提取 |
| `gemini-2.5-pro` | 质量高，理解深 | 复杂报告分析 |

### OpenAI
| 模型名称 | 特点 | 适用场景 |
|---------|------|----------|
| `o4-mini` | 经济实用 | 标准提取需求 |
| `o3` | 平衡性能 | 高质量提取 |
| `gpt-4.1-nano` | 快速响应 | 简单文档处理 |

**注意**: 所有模型都支持自定义名称输入，以适应API更新。

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
    "矿权起始日期": "2010年12月13日",
    "矿权截止日期": "2018年12月13日",
    "生产规模": null,
    "矿区面积": "2.88平方千米",
    "矿区海拔": "1800-2800米",
    "以往勘查工作": "历经多轮地质普查和详查工作"
  },
  "资源信息": [
    {
      "矿种": "金矿",
      "资源量情况": {
        "推断资源量": {
          "矿石量": "23.5万吨",
          "金属量": "965公斤",
          "品位": "4.11克/吨"
        },
        "控制资源量": null,
        "探明资源量": null,
        "总计": {
          "矿石量": "23.5万吨",
          "金属量": "965公斤",
          "品位": "4.11克/吨"
        }
      }
    },
    {
      "矿种": "银矿",
      "资源量情况": {
        "推断资源量": {
          "矿石量": "23.5万吨",
          "金属量": "965公斤",
          "品位": "41.1克/吨"
        },
        "控制资源量": null,
        "探明资源量": null,
        "总计": {
          "矿石量": "23.5万吨",
          "金属量": "965公斤", 
          "品位": "41.1克/吨"
        }
      }
    }
  ],
  "矿体分布": [
    {
      "矿体编号": "I号矿体",
      "矿体名称": "主矿体",
      "矿体长度": "800米",
      "矿体宽度": "300米",
      "矿体厚度": "平均1.2米",
      "矿体走向": "北东45°",
      "矿体倾角": "60°",
      "矿体面积": "24万平方米",
      "矿体体积": "28.8万立方米",
      "矿体金属量": "965公斤",
      "矿体矿石量": "23.5万吨",
      "矿体品位": "4.11克/吨"
    }
  ],
  "其它信息": "矿山位于构造活跃带，建议加强地质风险评估"
}
```

## 🏗️ 项目架构

### 文件结构
```
mining_file_recognize/
├── 📄 mining_report_extractor_stream.py    # 🌟 主程序（统一版本）
├── 📄 requirements.txt                     # 依赖清单
├── 📄 env_template.txt                     # 环境变量模板
├── 📄 README.md                           # 项目说明文档
└── 📁 dataset/
    └── 📄 json_format.txt                  # 输出格式说明
```

### 核心架构设计

```python
# 抽象基类设计
class BaseMiningReportExtractor(ABC):
    """矿山报告提取器抽象基类"""
    
    @abstractmethod
    def extract_from_file(self, file_path: str) -> MiningReport:
        """从PDF文件提取信息"""
        pass
    
    def save_result(self, result: MiningReport, output_path: str) -> bool:
        """保存结果到文件"""
        pass
    
    def print_summary(self, result: MiningReport) -> None:
        """打印提取结果摘要"""
        pass

# Gemini实现
class GeminiMiningReportExtractor(BaseMiningReportExtractor):
    """基于Gemini的矿山报告提取器"""
    
    def extract_from_file(self, file_path: str) -> MiningReport:
        # Gemini API实现
        pass

# OpenAI实现（含对话功能）
class OpenAIMiningReportExtractorWithStreamConversation(BaseMiningReportExtractor):
    """基于OpenAI的矿山报告提取器（带流式对话功能）"""
    
    def extract_from_file(self, file_path: str) -> MiningReport:
        # OpenAI API实现
        pass
    
    def start_conversation(self):
        """开始流式对话模式"""
        pass
```

### 数据模型设计

使用 Pydantic 确保数据质量和类型安全：

```python
class MiningReport(BaseModel):
    """矿山储量核实报告完整模型"""
    报告信息: Optional[ReportInfo] = None
    矿权信息: Optional[MiningRightsInfo] = None  
    资源信息: Optional[List[ResourceInfo]] = None
    矿体分布: Optional[List[OreBodyDistribution]] = None
    其它信息: Optional[str] = None
```

## 🔍 使用指南

### 编程式调用

```python
from mining_report_extractor_stream import create_extractor

# 方式1: 交互式选择（推荐新手）
extractor = create_extractor()
result = extractor.extract_from_file("report.pdf")

# 方式2: 直接指定提供商和模型
extractor = create_extractor("gemini", "gemini-2.5-flash")
result = extractor.extract_from_file("report.pdf")

# 方式3: OpenAI + 对话功能
extractor = create_extractor("openai", "o4-mini")
result = extractor.extract_from_file("report.pdf")

# 进入对话模式
if hasattr(extractor, 'start_conversation'):
    extractor.start_conversation()

# 保存结果
extractor.save_result(result, "output.json")

# 清理资源（OpenAI）
if hasattr(extractor, 'cleanup'):
    extractor.cleanup()
```

### 批量处理示例

```python
import os
from pathlib import Path

def batch_process_reports(pdf_dir: str, output_dir: str):
    """批量处理PDF报告"""
    extractor = create_extractor("gemini", "gemini-2.5-flash")
    
    pdf_files = Path(pdf_dir).glob("*.pdf")
    for pdf_file in pdf_files:
        try:
            print(f"Processing: {pdf_file.name}")
            result = extractor.extract_from_file(str(pdf_file))
            
            output_path = Path(output_dir) / f"{pdf_file.stem}_result.json"
            extractor.save_result(result, str(output_path))
            
        except Exception as e:
            print(f"Error processing {pdf_file.name}: {e}")
```

## ⚠️ 注意事项

### API配置
- **API密钥安全**: 请妥善保管您的API密钥，不要将 `.env` 文件提交到公共仓库
- **网络环境**: 确保网络能正常访问相应的AI服务商API
- **费用控制**: 大文件处理可能产生较高的API调用费用，建议先用小文件测试

### 文件处理
- **文件大小**: Gemini支持大于20MB文件自动使用File API上传
- **文件格式**: 目前仅支持PDF格式的矿山报告
- **中文优化**: 工具专门针对中文矿山报告进行了优化

### 提取质量
- **报告标准化**: 结构化程度较高的报告提取效果更好
- **信息完整性**: 如报告中缺失某些信息，对应字段将返回 `null`
- **多矿种支持**: 自动识别并提取主矿种和伴生矿种信息

## 🐛 故障排除

### 常见问题

**Q: 提示"API密钥错误"怎么办？**
A: 检查 `.env` 文件中的API密钥是否正确，确保没有多余的空格或换行符。

**Q: 上传大文件失败？**
A: Gemini会自动选择File API处理大文件，OpenAI需要确保文件大小在支持范围内。

**Q: 提取结果不准确？**
A: 可以尝试：
- 使用更高质量的模型（如gemini-2.5-pro或o3）
- 确保PDF文件质量良好，文字清晰
- 检查报告是否为标准的矿山储量核实报告格式

**Q: 对话功能无响应？**
A: 确保：
- 使用的是OpenAI版本的提取器
- 已成功提取报告信息
- 网络连接正常

### 错误日志
程序会输出详细的执行日志，包括：
- 📁 文件大小信息
- 📤 上传方式选择
- 🔍 分析进度提示
- ✅ 成功状态确认
- ❌ 错误信息详情

## 📞 技术支持

### 获取帮助
- **Issues**: 在GitHub仓库提交问题
- **文档**: 查看本README和代码注释
- **示例**: 参考 `dataset/json_format.txt` 输出格式

### 贡献指南
欢迎提交PR改进项目：
1. Fork项目仓库
2. 创建特性分支
3. 提交代码改进
4. 发起Pull Request

---

**开发者**: Mining Report AI Team  
**许可证**: MIT License  
**最后更新**: 2024年12月

🏔️ **让AI助力地质勘探，让数据驱动决策！**