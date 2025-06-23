import os
import json
import pathlib
from typing import Optional, List, Dict, Any
from openai import OpenAI
from dotenv import load_dotenv
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


class MiningReport(BaseModel):
    """矿山储量核实报告完整模型"""
    报告信息: Optional[ReportInfo] = None
    矿权信息: Optional[MiningRightsInfo] = None
    资源信息: Optional[List[ResourceInfo]] = None
    其它信息: Optional[str] = None


# ========== 主提取器类 ==========
class MiningReportExtractorOpenAI:
    """基于OpenAI的矿山储量核实报告信息提取器"""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "o4-mini", env_file: str = "openai.env"):
        """初始化提取器
        
        Args:
            api_key: OpenAI API密钥，如果不提供则从环境变量获取
            model: 使用的模型名称
            env_file: 环境变量文件路径
        """
        # 加载环境变量
        load_dotenv(env_file)
        
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("请提供OPENAI_API_KEY环境变量或直接传入api_key参数")
        
        self.client = OpenAI(api_key=self.api_key)
        self.model = model
        self.prompt = self._build_prompt()
    
    def _get_file_size_mb(self, file_path: str) -> float:
        """获取文件大小（MB）
        
        Args:
            file_path: 文件路径
            
        Returns:
            文件大小（MB）
        """
        file_size_bytes = pathlib.Path(file_path).stat().st_size
        return file_size_bytes / (1024 * 1024)
    
    def _build_prompt(self) -> str:
        """构建提示词"""
        return """
请仔细分析这个矿山储量核实报告PDF文档，按照以下结构提取信息并以JSON格式返回：

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

## 其它信息
提取任何上述未提到但你认为有价值的信息

如果某些信息在文档中未找到，请在对应字段填入null。
请仔细阅读文档内容，特别注意资源量统计表格，确保提取的信息准确完整。
"""

    def _upload_file(self, file_path: str) -> str:
        """上传文件到OpenAI
        
        Args:
            file_path: 文件路径
            
        Returns:
            文件ID
        """
        try:
            print("📤 正在上传文件到OpenAI服务器...")
            with open(file_path, "rb") as f:
                file = self.client.files.create(
                    file=f,
                    purpose="user_data"
                )
            print("✅ 文件上传完成")
            return file.id
        except Exception as e:
            print(f"❌ 文件上传失败: {e}")
            raise

    def extract_from_file(self, file_path: str) -> MiningReport:
        """从PDF文件提取信息
        
        Args:
            file_path: PDF文件路径
            
        Returns:
            MiningReport对象
        """
        try:
            filepath = pathlib.Path(file_path)
            if not filepath.exists():
                raise FileNotFoundError(f"文件不存在: {file_path}")
            
            # 获取文件大小信息
            file_size_mb = self._get_file_size_mb(file_path)
            print(f"📁 文件大小: {file_size_mb:.2f} MB")
            
            # 上传文件
            file_id = self._upload_file(file_path)
            
            # 调用OpenAI API提取信息
            print("🔍 正在分析文档内容...")
            try:
                response = self.client.responses.parse(
                    model=self.model,
                    input=[
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "input_file",
                                    "file_id": file_id,
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
                
                result = response.output_parsed
                print("✅ 文档分析完成")
                return result
                
            finally:
                # 清理上传的文件
                try:
                    self.client.files.delete(file_id)
                    print("🗑️ 临时文件已清理")
                except Exception as e:
                    print(f"⚠️ 清理临时文件时出现警告: {e}")
            
        except FileNotFoundError as e:
            print(f"❌ 文件错误: {e}")
            raise
        except Exception as e:
            print(f"❌ 提取过程中出现错误: {e}")
            raise
    
    def extract_to_dict(self, file_path: str) -> Dict[str, Any]:
        """提取信息并返回字典格式
        
        Args:
            file_path: PDF文件路径
            
        Returns:
            提取的信息字典
        """
        result = self.extract_from_file(file_path)
        return result.model_dump(exclude_none=True)
    
    def save_result(self, result: MiningReport, output_path: str) -> bool:
        """保存已提取的结果到文件
        
        Args:
            result: 已提取的MiningReport对象
            output_path: 输出JSON文件路径
            
        Returns:
            是否成功保存
        """
        try:
            result_dict = result.model_dump(exclude_none=True)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(result_dict, f, ensure_ascii=False, indent=2)
            
            print(f"✅ 结果已保存到: {output_path}")
            return True
            
        except Exception as e:
            print(f"❌ 保存文件时出错: {e}")
            return False
    
    def extract_and_save(self, file_path: str = None, output_path: Optional[str] = None, 
                        result: Optional[MiningReport] = None) -> bool:
        """提取信息并保存到文件（支持从已有结果保存）
        
        Args:
            file_path: PDF文件路径（如果提供result则可为None）
            output_path: 输出JSON文件路径，默认为原文件名+_result.json
            result: 已提取的MiningReport对象（如果提供则不会重新提取）
            
        Returns:
            是否成功保存
        """
        try:
            # 如果提供了已有结果，直接使用；否则重新提取
            if result is not None:
                result_to_save = result
                # 如果没有提供file_path但有result，尝试从output_path推断
                if file_path is None and output_path is None:
                    output_path = "mining_report_result.json"
                elif output_path is None:
                    output_path = pathlib.Path(file_path).stem + "_result.json"
            else:
                if file_path is None:
                    raise ValueError("必须提供file_path或result参数")
                result_to_save = self.extract_from_file(file_path)
                if output_path is None:
                    output_path = pathlib.Path(file_path).stem + "_result.json"
            
            return self.save_result(result_to_save, output_path)
            
        except Exception as e:
            print(f"❌ 保存过程中出现错误: {e}")
            return False
    
    def print_summary(self, result: MiningReport) -> None:
        """打印提取结果摘要
        
        Args:
            result: MiningReport对象
        """
        print("\n" + "="*50)
        print("📊 矿山储量核实报告信息摘要")
        print("="*50)
        
        # 报告信息
        if result.报告信息:
            print(f"\n📋 报告信息:")
            print(f"  • 报告名称: {result.报告信息.报告名称 or 'N/A'}")
            print(f"  • 编制单位: {result.报告信息.编制单位 or 'N/A'}")
            print(f"  • 编制日期: {result.报告信息.编制日期 or 'N/A'}")
        
        # 矿权信息 - 显示所有完整字段
        if result.矿权信息:
            print(f"\n⛏️  矿权信息:")
            print(f"  • 矿权名称: {result.矿权信息.矿权名称 or 'N/A'}")
            print(f"  • 矿权位置: {result.矿权信息.矿权位置 or 'N/A'}")
            print(f"  • 勘查程度: {result.矿权信息.勘查程度 or 'N/A'}")
            print(f"  • 矿权类型: {result.矿权信息.矿权类型 or 'N/A'}")
            print(f"  • 矿权编号: {result.矿权信息.矿权编号 or 'N/A'}")
            print(f"  • 矿权起始日期: {result.矿权信息.矿权起始日期 or 'N/A'}")
            print(f"  • 矿权截止日期: {result.矿权信息.矿权截止日期 or 'N/A'}")
            print(f"  • 生产规模: {result.矿权信息.生产规模 or 'N/A'}")
            print(f"  • 矿区面积: {result.矿权信息.矿区面积 or 'N/A'}")
            print(f"  • 矿区海拔: {result.矿权信息.矿区海拔 or 'N/A'}")
        
        # 资源信息
        if result.资源信息:
            print(f"\n💎 资源信息:")
            for idx, resource in enumerate(result.资源信息, 1):
                if len(result.资源信息) > 1:
                    print(f"\n  【矿种 {idx}】")
                print(f"  • 矿种: {resource.矿种 or 'N/A'}")
                
                if resource.资源量情况:
                    print(f"  • 资源量情况:")
                    # 显示总计
                    if resource.资源量情况.总计:
                        total = resource.资源量情况.总计
                        print(f"    📊 总计:")
                        print(f"       - 矿石量: {total.矿石量 or 'N/A'}")
                        print(f"       - 金属量: {total.金属量 or 'N/A'}")
                        print(f"       - 品位: {total.品位 or 'N/A'}")
        
        # 其它信息
        if result.其它信息:
            print(f"\n📝 其它信息:")
            print(f"  {result.其它信息}")
        
        print("\n" + "="*50)


# ========== 便捷函数 ==========
def quick_extract(file_path: str, api_key: Optional[str] = None, env_file: str = "openai.env") -> Dict[str, Any]:
    """快速提取函数，直接返回字典结果
    
    Args:
        file_path: PDF文件路径
        api_key: API密钥（可选）
        env_file: 环境变量文件路径
        
    Returns:
        提取的信息字典
    """
    extractor = MiningReportExtractorOpenAI(api_key=api_key, env_file=env_file)
    return extractor.extract_to_dict(file_path)


# ========== 主函数 ==========
def main():
    MODEL = "o3"
    """主函数 - 使用示例"""
    # 创建提取器实例
    extractor = MiningReportExtractorOpenAI(model=MODEL)
    
    # 设置PDF文件路径
    pdf_file = "储量核实20150410.pdf"
    
    try:
        # 提取信息
        print("🚀 开始处理矿山报告...")
        result = extractor.extract_from_file(pdf_file)
        
        # 打印摘要
        extractor.print_summary(result)
        
        # 保存完整结果（使用已提取的结果，避免重复调用）
        extractor.extract_and_save(file_path=pdf_file, result=result)
        
        print("\n🎉 处理完成！")
        
    except Exception as e:
        print(f"\n❌ 处理失败: {e}")


if __name__ == "__main__":
    main()
    # print(quick_extract("file.pdf")) 