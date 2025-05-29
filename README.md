# 矿山储量核实报告信息提取器

一个基于Google Gemini AI的智能PDF文档信息提取工具，专门用于从矿山储量核实报告中提取结构化信息。

## 🌟 主要特性

- **智能PDF解析**：基于Google Gemini 2.5 Flash模型的强大文档理解能力
- **自动文件大小检测**：根据文件大小自动选择最优上传方式（直接上传 vs File API）
- **结构化数据提取**：使用Pydantic模型确保输出数据的质量和一致性
- **中文友好**：专门针对中文矿山报告进行优化
- **多矿种支持**：支持主矿种和伴生矿种的资源量统计
- **完整信息覆盖**：提取报告信息、矿权信息、资源信息等全面数据

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

### 资源信息
- 矿种（金矿、铜矿、银矿等）
- 资源量分类统计：
  - 333类别（推断的资源量）
  - 332类别（控制的资源量）
  - 331类别（探明的资源量）
  - 高于331类别
  - 总计
- 每个类别包含：矿石量、金属量、品位

## 🚀 快速开始

### 环境要求

- Python 3.8+
- Google Gemini API密钥

### 安装依赖

```bash
pip install google-genai pydantic pathlib
```

### 设置API密钥

```bash
# 方法1：设置环境变量
export GEMINI_API_KEY="your_api_key_here"

# 方法2：在代码中直接传入
extractor = MiningReportExtractor(api_key="your_api_key_here")
```

### 基础使用

```python
from mining_report_extractor_v2 import MiningReportExtractor

# 创建提取器实例
extractor = MiningReportExtractor()

# 提取信息（自动选择上传方式）
result = extractor.extract_from_file("your_mining_report.pdf")

# 打印摘要
extractor.print_summary(result)

# 保存完整结果
extractor.extract_and_save("your_mining_report.pdf", result=result)
```

### 快速提取

```python
from mining_report_extractor_v2 import quick_extract

# 一行代码完成提取
data = quick_extract("your_mining_report.pdf")
print(data)
```

## 🔧 高级功能

### 手动指定上传方式

```python
# 强制使用File API（适用于大文件 > 20MB）
result = extractor.extract_from_file("large_file.pdf", use_file_api=True)

# 强制使用直接上传（适用于小文件 ≤ 20MB）
result = extractor.extract_from_file("small_file.pdf", use_file_api=False)
```

### 只保存已提取的结果

```python
# 避免重复调用AI，直接保存已有结果
extractor.save_result(result, "custom_output.json")
```

## 📁 项目结构

```
mining_report_extractor/
│
├── mining_report_extractor_v2.py  # 主程序文件
├── README.md                      # 项目说明
├── requirements.txt               # 依赖列表
└── examples/                      # 示例文件
    ├── sample_report.pdf          # 示例报告
    └── sample_output.json         # 示例输出
```

## 🔄 文件大小自动处理

程序会自动检测PDF文件大小：

- **≤ 20MB**：使用直接字节上传，速度更快
- **> 20MB**：自动切换到File API上传，符合Gemini官方建议

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
    "矿区面积": "1.06km²"
  },
  "资源信息": [
    {
      "矿种": "金矿",
      "资源量情况": {
        "类别_333": {
          "矿石量": "23.5万吨",
          "金属量": "965kg",
          "品位": "4.11g/t"
        },
        "类别_332": {
          "矿石量": "20.3万吨",
          "金属量": "1263kg",
          "品位": "6.22g/t"
        },
        "总计": {
          "矿石量": "43.8万吨",
          "金属量": "2228kg",
          "品位": "5.09g/t"
        }
      }
    }
  ]
}
```

## ⚡ 性能优化

- **单次AI调用**：避免重复调用大模型，提升处理效率
- **智能上传**：根据文件大小自动选择最优上传策略
- **数据一致性**：确保摘要和保存的JSON数据完全一致

## 🛠️ API参考

### MiningReportExtractor

主要的提取器类，提供完整的文档处理功能。

#### 方法

- `extract_from_file(file_path, use_file_api=None)` - 从PDF提取信息
- `extract_to_dict(file_path, use_file_api=None)` - 提取并返回字典格式
- `extract_and_save(file_path, output_path, result=None)` - 提取并保存到文件
- `save_result(result, output_path)` - 保存已提取的结果
- `print_summary(result)` - 打印美观的摘要信息

### 便捷函数

- `quick_extract(file_path, api_key=None)` - 快速提取，返回字典结果

## 🔒 注意事项

1. **API密钥安全**：请妥善保管您的Gemini API密钥，不要在代码中硬编码
2. **文件格式**：目前仅支持PDF格式的矿山报告
3. **网络要求**：需要稳定的网络连接访问Google Gemini API
4. **处理时间**：大文件处理时间较长，请耐心等待

## 🤝 贡献

欢迎提交Issue和Pull Request来改进这个项目！

## 📄 许可证

MIT License

## 🙏 致谢

- [Google Gemini](https://deepmind.google/technologies/gemini/) - 强大的AI模型支持
- [Pydantic](https://pydantic.dev/) - 数据验证和序列化
- 所有为矿业数字化转型贡献力量的开发者们

---

**作者**: Karl Liu  
**GitHub**: [Karl-Liu94](https://github.com/Karl-Liu94)  
**项目地址**: [mining_report_extractor](https://github.com/Karl-Liu94/mining_report_extractor.git) 