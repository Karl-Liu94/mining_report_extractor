import os
import json
import pathlib
from typing import Optional, List, Dict, Any, Tuple
from abc import ABC, abstractmethod
from pydantic import BaseModel


# ========== Pydantic 数据模型 ==========
class ReportInfo(BaseModel):
    """报告信息模型"""
    报告名称: Optional[str] = None
    编制单位: Optional[str] = None
    编制日期: Optional[str] = None


class MiningRightsInfo(BaseModel):
    """矿权信息模型"""
    矿权名称: Optional[str] = None
    矿权位置: Optional[str] = None
    勘查程度: Optional[str] = None  # 普查/详查/勘探
    矿权类型: Optional[str] = None  # 探矿权/采矿权
    矿权编号: Optional[str] = None
    矿权起始日期: Optional[str] = None
    矿权截止日期: Optional[str] = None
    生产规模: Optional[str] = None
    矿区面积: Optional[str] = None
    矿区海拔: Optional[str] = None
    以往勘查工作: Optional[str] = None


class ResourceQuantityDetail(BaseModel):
    """资源量详细信息模型"""
    矿石量: Optional[str] = None
    金属量: Optional[str] = None
    品位: Optional[str] = None


class ResourceCategory(BaseModel):
    """资源量类别模型"""
    推断资源量: Optional[ResourceQuantityDetail] = None
    控制资源量: Optional[ResourceQuantityDetail] = None
    探明资源量: Optional[ResourceQuantityDetail] = None
    总计: Optional[ResourceQuantityDetail] = None


class ResourceInfo(BaseModel):
    """资源信息模型"""
    矿种: Optional[str] = None
    资源量情况: Optional[ResourceCategory] = None


class OreBodyDistribution(BaseModel):
    """矿体分布情况信息模型"""
    矿体编号: Optional[str] = None
    矿体名称: Optional[str] = None
    矿体长度: Optional[str] = None
    矿体宽度: Optional[str] = None
    矿体厚度: Optional[str] = None
    矿体走向: Optional[str] = None
    矿体倾角: Optional[str] = None
    矿体面积: Optional[str] = None
    矿体体积: Optional[str] = None
    矿体金属量: Optional[str] = None
    矿体矿石量: Optional[str] = None
    矿体品位: Optional[str] = None


class MiningReport(BaseModel):
    """矿山储量核实报告完整模型"""
    报告信息: Optional[ReportInfo] = None
    矿权信息: Optional[MiningRightsInfo] = None
    资源信息: Optional[List[ResourceInfo]] = None
    矿体分布: Optional[List[OreBodyDistribution]] = None
    其它信息: Optional[str] = None


# ========== 提示词配置 ==========
EXTRACTION_PROMPT = """
你是一名地质和矿业领域的专家，请仔细分析这个矿山储量核实报告PDF文档，按照以下结构提取信息并以JSON格式返回：

## 报告信息
- 报告名称：报告的完整名称，通常在首页或标题中
- 编制单位：编制该报告的机构或公司名称（注意：不要与委托公司混淆，一般正文中会注明，A公司委托B公司/地质队/单位对xx开展勘探工作，编制了本报告，这个B公司/地质队/单位才是编制单位）
- 编制日期：报告的编制日期

## 矿权信息
- 矿权名称：该报告所调查的矿权主体名称
- 矿权位置：矿权的地理位置
- 勘查程度：本次储量核实的勘查程度，有且仅有以下三种类型（如果没有找到则返回null）：
  * 普查
  * 详查  
  * 勘探
- 矿权类型：有且仅有以下两种类型（如果没有找到则返回null）：
  * 探矿权
  * 采矿权
- 矿权编号：矿权的官方编号
- 矿权起始日期：矿权的开始日期
- 矿权截止日期：矿权的结束日期
- 生产规模：矿山的生产规模，如"100万吨/年"、"50万吨/年"等，仅采矿证才有，探矿证可返回null
- 矿区面积：矿区的总面积（包含数值和单位）
- 矿区海拔：矿区的海拔高度
- 以往勘查工作:过去地质工作的简要总结

## 资源信息
- 矿种：返回完整格式如"金矿"、"铜矿"、"银矿"，不要只返回"金"、"铜"、"银"
- 资源量情况：对于每个矿种（包括主矿种和伴生矿种），都要尝试按以下类别分别提取：
  * 推断资源量（如果报告中遇到333资源量，计入这该类别）
  * 控制资源量（如果报告中遇到332资源量，计入这该类别）
  * 探明资源量（如果报告中遇到331资源量、1、2开头的资源量，如122b、111等计入这该类别）
  * 总计（将上述资源量加总，表示该矿种的所有资源情况）

**重要说明：**
1. 对于每个矿种（无论是主矿种还是伴生矿种），都要尝试提取分类资源量数据
2. 如果报告中某个矿种只提供了总计数据而没有分类数据，那么分类字段也要保留，值为null即可，而不只填写总计字段
3. 如果报告中某个矿种有分类数据，请务必提取所有可用的分类信息
4. 上述资源量均返回保有资源量

对于每个资源量类别，请提取：
- 矿石量：返回数值和单位，如"1000千克"、"120万吨"（注意：伴生矿种可能与主矿种共享矿石量）
- 金属量：返回数值和单位，如"1000千克"、"120万吨"  
- 品位：返回如"6%"或"2.7克/吨"的格式

如果报告中出现多个矿种或伴生矿，请一并返回，每个矿种单独统计

## 矿体分布
- 矿体编号：矿体的编号
- 矿体名称：矿体的名称
- 矿体长度：矿体的长度
- 矿体宽度：矿体的宽度
- 矿体厚度：矿体的厚度
- 矿体走向：矿体的走向
- 矿体倾角：矿体的倾角
- 矿体面积：矿体的面积
- 矿体体积：矿体的体积
- 矿体金属量：矿体的金属量
- 矿体矿石量：矿体的矿石量
- 矿体品位：矿体的品位

**重要说明：**
以上信息报告中可能有描述，可能没有描述，如果没有找到描述则返回null，切不可没有根据地胡乱编造！

## 其它信息
提取任何上述未提到但你认为有价值的信息

如果某些信息在文档中未找到，请在对应字段填入null。
请仔细阅读文档内容，特别注意资源量统计表格，确保提取的信息准确完整。
"""

CONVERSATION_INSTRUCTIONS = """
你是一名地质和矿业领域的专家，请你仔细阅读报告内容，认真回答用户的问题，
注意答案需要条理清晰，如果遇到不知道或者报告中没有的问题可直言不知道，
切不可胡编乱造！优先保证答案的正确性
"""


# ========== 配置常量 ==========
GEMINI_MODELS = ["gemini-2.5-flash", "gemini-2.5-pro"]
OPENAI_MODELS = ["o4-mini", "o3", "gpt-4.1-nano"]
EXIT_COMMANDS = ['exit', 'quit', '退出', '结束']
CONFIRM_CHOICES = ['y', 'yes', '是', '好']
DENY_CHOICES = ['n', 'no', '否', '不']


# ========== 抽象基类 ==========
class BaseMiningReportExtractor(ABC):
    """矿山报告提取器抽象基类"""
    
    def __init__(self, api_key: Optional[str] = None, model: str = None):
        self.api_key = api_key
        self.model = model
        self.prompt = EXTRACTION_PROMPT
    
    def _get_file_size_mb(self, file_path: str) -> float:
        """获取文件大小（MB）"""
        file_size_bytes = pathlib.Path(file_path).stat().st_size
        return file_size_bytes / (1024 * 1024)
    
    @abstractmethod
    def extract_from_file(self, file_path: str) -> MiningReport:
        """从PDF文件提取信息"""
        pass
    
    def save_result(self, result: MiningReport, output_path: str) -> bool:
        """保存结果到文件"""
        try:
            result_dict = result.model_dump(exclude_none=True)
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(result_dict, f, ensure_ascii=False, indent=2)
            print(f"✅ 结果已保存到: {output_path}")
            return True
        except Exception as e:
            print(f"❌ 保存文件时出错: {e}")
            return False
    
    def print_summary(self, result: MiningReport) -> None:
        """打印提取结果摘要"""
        print("\n" + "="*50)
        print("📊 矿山储量核实报告信息摘要")
        print("="*50)
        
        # 报告信息
        if result.报告信息:
            print(f"\n📋 报告信息:")
            for field, value in result.报告信息.model_dump().items():
                print(f"  • {field}: {value or 'N/A'}")
        
        # 矿权信息
        if result.矿权信息:
            print(f"\n⛏️  矿权信息:")
            for field, value in result.矿权信息.model_dump().items():
                print(f"  • {field}: {value or 'N/A'}")
        
        # 资源信息（简化显示）
        if result.资源信息:
            print(f"\n💎 资源信息:")
            for idx, resource in enumerate(result.资源信息, 1):
                if len(result.资源信息) > 1:
                    print(f"\n  【矿种 {idx}】")
                print(f"  • 矿种: {resource.矿种 or 'N/A'}")
                
                if resource.资源量情况 and resource.资源量情况.总计:
                    total = resource.资源量情况.总计
                    print(f"  • 资源量总计:")
                    print(f"    - 矿石量: {total.矿石量 or 'N/A'}")
                    print(f"    - 金属量: {total.金属量 or 'N/A'}")
                    print(f"    - 品位: {total.品位 or 'N/A'}")
        
        # 其它信息
        if result.其它信息:
            print(f"\n📝 其它信息:")
            print(f"  {result.其它信息}")
        
        print("\n" + "="*50)


# ========== Gemini 实现 ==========
class GeminiMiningReportExtractor(BaseMiningReportExtractor):
    """基于Gemini的矿山报告提取器"""
    
    FILE_SIZE_THRESHOLD = 20 * 1024 * 1024  # 20MB
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gemini-2.5-flash", env_file: str = ".env"):
        super().__init__(api_key, model)
        
        try:
            from google import genai
            from google.genai import types
            from dotenv import load_dotenv
            self.genai = genai
            self.types = types
            load_dotenv(env_file)
        except ImportError:
            raise ImportError("请安装必需包: pip install google-genai python-dotenv")
        
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            raise ValueError("请提供GEMINI_API_KEY环境变量或直接传入api_key参数")
        
        self.client = genai.Client(api_key=self.api_key)
    
    def extract_from_file(self, file_path: str, use_file_api: Optional[bool] = None) -> MiningReport:
        """从PDF文件提取信息"""
        filepath = pathlib.Path(file_path)
        if not filepath.exists():
            raise FileNotFoundError(f"文件不存在: {file_path}")
        
        file_size_mb = self._get_file_size_mb(file_path)
        
        # 自动判断是否使用File API
        if use_file_api is None:
            use_file_api = filepath.stat().st_size > self.FILE_SIZE_THRESHOLD
        
        print(f"📁 文件大小: {file_size_mb:.2f} MB")
        
        if use_file_api:
            print(f"📤 使用File API上传（文件大小超过{self.FILE_SIZE_THRESHOLD/(1024*1024):.0f}MB阈值）")
            print("⏳ 正在上传文件到Gemini服务器...")
            uploaded_file = self.client.files.upload(file=filepath)
            file_content = uploaded_file
            print("✅ 文件上传完成")
        else:
            print(f"📤 使用直接字节上传")
            file_content = self.types.Part.from_bytes(
                data=filepath.read_bytes(),
                mime_type='application/pdf',
            )
        
        print("🔍 正在分析文档内容...")
        response = self.client.models.generate_content(
            model=self.model,
            contents=[file_content, self.prompt],
            config={
                "response_mime_type": "application/json",
                "response_schema": MiningReport,
            }
        )
        
        result = MiningReport.model_validate_json(response.text)
        print("✅ 文档分析完成")
        return result


# ========== OpenAI 实现（带流式对话功能） ==========
class OpenAIMiningReportExtractorWithStreamConversation(BaseMiningReportExtractor):
    """基于OpenAI的矿山报告提取器（带流式对话功能）"""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "o4-mini", env_file: str = ".env"):
        super().__init__(api_key, model)
        
        try:
            from openai import OpenAI
            from dotenv import load_dotenv
            self.OpenAI = OpenAI
            load_dotenv(env_file)
        except ImportError:
            raise ImportError("请安装必需包: pip install openai python-dotenv")
        
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("请提供OPENAI_API_KEY环境变量或直接传入api_key参数")
        
        self.client = OpenAI(api_key=self.api_key)
        self.file_id = None  # 保存上传的文件ID
        self.initial_response_id = None  # 保存初始提取响应的ID
    
    def _upload_file(self, file_path: str) -> str:
        """上传文件到OpenAI"""
        print("📤 正在上传文件到OpenAI服务器...")
        with open(file_path, "rb") as f:
            file = self.client.files.create(file=f, purpose="user_data")
        print("✅ 文件上传完成")
        return file.id
    
    def extract_from_file(self, file_path: str) -> MiningReport:
        """从PDF文件提取信息"""
        filepath = pathlib.Path(file_path)
        if not filepath.exists():
            raise FileNotFoundError(f"文件不存在: {file_path}")
        
        file_size_mb = self._get_file_size_mb(file_path)
        print(f"📁 文件大小: {file_size_mb:.2f} MB")
        
        self.file_id = self._upload_file(file_path)
        
        print("🔍 正在分析文档内容...")
        response = self.client.responses.parse(
            model=self.model,
            input=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "input_file",
                            "file_id": self.file_id,
                        },
                        {
                            "type": "input_text",
                            "text": self.prompt,
                        },
                    ]
                }
            ],
            text_format=MiningReport,
        )
        
        # 保存初始响应ID，用于后续对话
        self.initial_response_id = response.id
        
        result = response.output_parsed
        print("✅ 文档分析完成")
        return result
    
    def start_conversation(self):
        """开始对话模式"""
        if not self.initial_response_id:
            print("❌ 请先提取报告信息后再进入对话模式")
            return
        
        print("\n" + "="*50)
        print("💬 进入对话模式")
        print(f"🤖 使用模型: {self.model}")
        print("="*50)
        print("您现在可以询问关于这份矿山报告的任何问题。")
        print("输入 'exit' 或 '退出' 结束对话。")
        print("="*50)
        
        previous_response_id = self.initial_response_id
        
        while True:
            try:
                # 获取用户输入
                user_input = input("\n🙋 您的问题: ").strip()
                
                # 检查是否退出
                if user_input.lower() in EXIT_COMMANDS:
                    print("\n👋 结束对话，感谢使用！")
                    break
                
                if not user_input:
                    print("❌ 请输入有效的问题")
                    continue
                
                # 发送问题并获取流式回答
                print("\n🤖 AI回答:")
                print("-" * 50)
                
                # 使用流式输出
                stream = self.client.responses.create(
                    model=self.model,
                    instructions=CONVERSATION_INSTRUCTIONS,
                    previous_response_id=previous_response_id,
                    input=user_input,
                    stream=True,
                )
                
                # 收集完整响应以获取response_id
                full_response = ""
                response_id = None
                
                for event in stream:
                    if event.type == 'response.output_text.delta':
                        print(event.delta, end='', flush=True)
                        full_response += event.delta
                    elif event.type == 'response.done':
                        # 获取response_id用于下一轮对话
                        response_id = event.response.id
                
                print("\n" + "-" * 50)
                
                # 更新对话ID
                if response_id:
                    previous_response_id = response_id
                
            except KeyboardInterrupt:
                print("\n\n👋 用户中断对话")
                break
            except Exception as e:
                print(f"\n❌ 对话过程中出现错误: {e}")
                print("您可以尝试重新提问或退出对话。")
    
    def cleanup(self):
        """清理上传的文件"""
        if self.file_id:
            try:
                self.client.files.delete(self.file_id)
                print("🗑️ 临时文件已清理")
            except Exception as e:
                print(f"⚠️ 清理临时文件时出现警告: {e}")


# ========== 用户交互函数 ==========
def select_model(models: List[str], prompt: str) -> str:
    """通用的模型选择函数"""
    print(f"\n{prompt}")
    for i, model in enumerate(models, 1):
        print(f"{i}. {model}")
    print(f"{len(models)+1}. 自定义模型名称")
    
    while True:
        choice = input(f"\n请选择模型 (1-{len(models)+1}): ").strip()
        try:
            choice_num = int(choice)
            if 1 <= choice_num <= len(models):
                return models[choice_num - 1]
            elif choice_num == len(models) + 1:
                custom_model = input("请输入自定义模型名称: ").strip()
                if custom_model:
                    return custom_model
            else:
                print(f"❌ 无效选择，请输入 1-{len(models)+1}")
        except ValueError:
            print(f"❌ 请输入有效数字 1-{len(models)+1}")


def get_user_choice() -> Tuple[str, str]:
    """获取用户选择的API提供商和模型"""
    print("\n🤖 请选择AI提供商:")
    print("1. Gemini (Google) - 仅支持信息提取")
    print("2. OpenAI - 支持信息提取和流式对话功能")
    
    while True:
        choice = input("\n请输入选择 (1-2): ").strip()
        if choice == "1":
            provider = "gemini"
            model = select_model(GEMINI_MODELS, "📋 Gemini 可用模型:")
            break
        elif choice == "2":
            provider = "openai"
            model = select_model(OPENAI_MODELS, "📋 OpenAI 可用模型:")
            break
        else:
            print("❌ 无效选择，请输入 1 或 2")
    
    return provider, model


def create_extractor(provider: str = None, model: str = None, **kwargs) -> BaseMiningReportExtractor:
    """工厂函数：创建提取器实例"""
    if provider is None or model is None:
        provider, model = get_user_choice()
    
    print(f"\n🔧 创建提取器: {provider} - {model}")
    
    if provider == "gemini":
        return GeminiMiningReportExtractor(model=model, **kwargs)
    elif provider == "openai":
        return OpenAIMiningReportExtractorWithStreamConversation(model=model, **kwargs)
    else:
        raise ValueError(f"不支持的提供商: {provider}")


def get_pdf_file() -> str:
    """获取PDF文件路径"""
    while True:
        file_path = input("\n📁 请输入PDF文件路径: ").strip()
        # 去除可能的引号
        if file_path.startswith('"') and file_path.endswith('"'):
            file_path = file_path[1:-1]
        
        if pathlib.Path(file_path).exists():
            return file_path
        else:
            print("❌ 文件不存在，请重新输入")


def ask_yes_no(prompt: str) -> bool:
    """通用的是/否询问函数"""
    while True:
        choice = input(f"\n{prompt} (y/n): ").strip().lower()
        if choice in CONFIRM_CHOICES:
            return True
        elif choice in DENY_CHOICES:
            return False
        else:
            print("❌ 无效输入，请输入 y 或 n")


# ========== 主函数 ==========
def main():
    """主函数 - 交互式使用"""
    print("🏔️  矿山储量核实报告信息提取工具")
    print("="*50)
    
    extractor = None
    try:
        # 获取用户选择
        provider, model = get_user_choice()
        extractor = create_extractor(provider, model)
        
        # 获取文件路径
        pdf_file = get_pdf_file()
        
        # 处理文件
        print(f"\n🚀 开始处理矿山报告: {pathlib.Path(pdf_file).name}")
        result = extractor.extract_from_file(pdf_file)
        
        # 显示结果
        extractor.print_summary(result)
        
        # 保存结果
        output_path = pathlib.Path(pdf_file).stem + "_result.json"
        extractor.save_result(result, output_path)
        
        print("\n🎉 信息提取完成！")
        
        # 如果是OpenAI，询问是否进入对话模式
        if provider == "openai" and isinstance(extractor, OpenAIMiningReportExtractorWithStreamConversation):
            if ask_yes_no("💬 是否进入提问环节？"):
                extractor.start_conversation()
        
    except KeyboardInterrupt:
        print("\n\n👋 用户取消操作")
    except Exception as e:
        print(f"\n❌ 处理失败: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # 清理资源
        if extractor and isinstance(extractor, OpenAIMiningReportExtractorWithStreamConversation):
            extractor.cleanup()


if __name__ == "__main__":
    main() 