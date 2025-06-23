# 矿山储量核实报告信息提取器 🏔️

一个基于AI大模型的智能PDF文档信息提取工具，专门用于从矿山储量核实报告中提取结构化信息。支持**Gemini**和**OpenAI**两大AI服务商，用户可根据需要自由选择。

## 🌟 主要特性

- **🤖 双AI支持**：支持Google Gemini和OpenAI两大AI服务商
- **🎯 智能模型选择**：提供预设模型列表，支持自定义模型名称  
- **📄 智能PDF解析**：强大的文档理解和信息提取能力
- **🔧 统一API接口**：无论使用哪种AI，调用方式完全一致
- **🗂️ 结构化输出**：使用Pydantic模型确保数据质量和一致性
- **🇨🇳 中文优化**：专门针对中文矿山报告进行优化
- **💎 多矿种支持**：支持主矿种和伴生矿种的资源量统计
- **📊 完整信息覆盖**：提取报告信息、矿权信息、资源信息等全面数据
- **🔒 安全配置**：使用.env文件统一管理API密钥

## 📋 提取信息类型

### 报告信息
- 报告名称
- 编制单位  
- 编制日期

### 矿权信息
- 矿权名称
- 矿权位置
- 勘查程度（普查/详查/勘探）
- 矿权类型（探矿权/采矿权）
- 矿权编号
- 矿权起始/截止日期
- 生产规模
- 矿区面积
- 矿区海拔
- 以往勘查工作

### 资源信息
- 矿种（金矿、铜矿、银矿等）
- 资源量分类统计：
  - 推断资源量（333类别）
  - 控制资源量（332类别）
  - 探明资源量（331类别等）
  - 总计
- 每个类别包含：矿石量、金属量、品位

## 🚀 快速开始

### 环境要求

- Python 3.8+
- Google Gemini API密钥 或 OpenAI API密钥（至少一个）

### 安装依赖

```bash
pip install -r requirements.txt
```

或手动安装：

```bash
# 基础依赖
pip install pydantic python-dotenv

# 如果使用Gemini
pip install google-genai

# 如果使用OpenAI  
pip install openai
```

### 配置API密钥

1. **复制并编辑.env文件**：
```bash
cp .env.example .env  # 如果有示例文件
# 或直接编辑.env文件
```

2. **在.env文件中填入您的API密钥**：
```bash
# API密钥配置文件
# 请填入您的实际API密钥，去掉注释符号#

# OpenAI API密钥
OPENAI_API_KEY=your_openai_api_key_here

# Gemini API密钥  
GEMINI_API_KEY=your_gemini_api_key_here
```

### 交互式使用（推荐）

```bash
python mining_report_extractor_unified.py
```

程序会引导您：
1. 选择AI服务商（Gemini/OpenAI）
2. 选择具体模型
3. 输入PDF文件路径
4. 自动处理并显示结果

### 编程式使用

```python
from mining_report_extractor_unified import create_extractor

# 方式1：交互式选择
extractor = create_extractor()
result = extractor.extract_from_file("your_report.pdf")

# 方式2：直接指定
extractor = create_extractor("gemini", "gemini-2.5-flash")
result = extractor.extract_from_file("your_report.pdf")

# 方式3：快速提取
from mining_report_extractor_unified import quick_extract
data = quick_extract("your_report.pdf", "openai", "o3")
```

## 🔧 支持的模型

### Gemini 模型
- `gemini-2.5-flash`（默认，速度快）
- `gemini-2.5-pro`（质量高）
- 支持自定义模型名称

### OpenAI 模型  
- `o4-mini`（经济实用）
- `o3`（平衡性能）
- `o3-pro`（最高质量）
- 支持自定义模型名称

## 🏗️ 项目架构

### 文件结构
```
mining_file_recognize/
├── mining_report_extractor_unified.py    # 🌟 统一入口（推荐使用）
├── mining_report_extractor_gemini.py     # Gemini专用版本
├── mining_report_extractor_openai.py     # OpenAI专用版本
├── .env                                   # API密钥配置文件
├── requirements.txt                       # 依赖列表
├── README.md                             # 项目说明
└── dataset/
    └── json_format.txt                   # 输出格式示例
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
    # Gemini API实现
    
class OpenAIMiningReportExtractor(BaseMiningReportExtractor):  
    # OpenAI API实现

# 工厂函数
def create_extractor(provider: str, model: str) -> BaseMiningReportExtractor:
    # 根据参数创建对应的提取器实例
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
          "矿石量": "20.3万吨",
          "金属量": "1263kg",
          "品位": "6.22g/t"
        },
        "探明资源量": null,
        "总计": {
          "矿石量": "43.8万吨", 
          "金属量": "2228kg",
          "品位": "5.09g/t"
        }
      }
    }
  ],
  "其它信息": "该矿床具有良好的开发前景..."
}
```

## 🛠️ API参考

### 核心类

#### `BaseMiningReportExtractor`（抽象基类）
所有提取器的统一接口。

#### `GeminiMiningReportExtractor`
基于Google Gemini的实现。
- 自动文件大小检测（>20MB使用File API）
- 支持多种Gemini模型

#### `OpenAIMiningReportExtractor`  
基于OpenAI的实现。
- 文件自动上传和清理
- 支持结构化输出

### 主要方法

```python
# 基础提取
result = extractor.extract_from_file("file.pdf")

# 提取为字典格式
data = extractor.extract_to_dict("file.pdf") 

# 提取并保存
success = extractor.extract_and_save("file.pdf", "output.json")

# 保存已有结果
extractor.save_result(result, "output.json")

# 打印美观摘要
extractor.print_summary(result)
```

### 工厂函数

```python
# 交互式创建
extractor = create_extractor()

# 直接指定
extractor = create_extractor("gemini", "gemini-2.5-flash")
extractor = create_extractor("openai", "o3")

# 便捷函数
data = quick_extract("file.pdf", "gemini", "gemini-2.5-pro")
```

## ⚡ 性能优化

### Gemini优化
- **智能文件上传**：小文件(<20MB)直接上传，大文件使用File API
- **模型选择**：Flash版本速度更快，Pro版本质量更高

### OpenAI优化  
- **自动文件管理**：处理完成后自动清理临时文件
- **结构化输出**：使用最新的结构化输出API确保格式正确

### 通用优化
- **单次AI调用**：避免重复调用大模型
- **统一数据模型**：确保不同AI的输出格式完全一致

## 🔒 安全注意事项

1. **API密钥安全**：
   - 将`.env`添加到`.gitignore`
   - 不要在代码中硬编码API密钥
   - 妥善保管您的API密钥

2. **文件处理**：
   - 仅支持PDF格式
   - 确保文件完整性
   - 注意文件大小限制

3. **网络要求**：
   - 需要稳定的网络连接
   - 确保能访问对应的AI服务

## 🚩 故障排除

### 常见问题

**Q: 提示"请安装必需包"错误**
```bash
# 安装Gemini依赖
pip install google-genai python-dotenv

# 安装OpenAI依赖  
pip install openai python-dotenv
```

**Q: API密钥错误**
- 检查`.env`文件中的密钥是否正确
- 确认已去掉注释符号`#`
- 验证密钥是否有效且有足够额度

**Q: 文件上传失败**
- 检查PDF文件是否损坏
- 确认网络连接稳定
- 尝试使用较小的文件测试

**Q: 输出格式不正确**  
- 确保使用的是最新版本的代码
- 检查模型是否支持结构化输出
- 尝试更换模型

## 🤝 贡献指南

欢迎贡献代码！请遵循以下步骤：

1. Fork项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建Pull Request

## 📄 许可证

MIT License - 详见[LICENSE](LICENSE)文件

## 🙏 致谢

- [Google Gemini](https://deepmind.google/technologies/gemini/) - 强大的AI模型支持
- [OpenAI](https://openai.com/) - 先进的语言模型API
- [Pydantic](https://pydantic.dev/) - 数据验证和序列化
- 所有为矿业数字化转型贡献力量的开发者们

---

**如果这个项目对您有帮助，请给个⭐星标支持！**

**作者**: Karl Liu  
**联系**: [GitHub Issues](https://github.com/Karl-Liu94/mining_file_recognize/issues)  
**项目地址**: [mining_file_recognize](https://github.com/Karl-Liu94/mining_file_recognize.git) 