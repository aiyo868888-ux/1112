"""
K12错题本 - 百度OCR服务
使用百度通用文字识别API
"""
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import json
import os
import base64
import requests
from typing import Optional
import sys

# 设置控制台编码为UTF-8
if sys.platform == "win32":
    import codecs
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter("utf-8")(sys.stderr.buffer, 'strict')

app = FastAPI(title="K12错题本 OCR服务 - 百度OCR版")

# 添加CORS支持
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 配置信息
class BaiduOCRConfig:
    def __init__(self):
        # 从环境变量或配置文件读取
        self.api_key = os.getenv("BAIDU_API_KEY", "")
        self.secret_key = os.getenv("BAIDU_SECRET_KEY", "")

        # 如果环境变量为空，尝试从config.json读取
        if not self.api_key or not self.secret_key:
            try:
                # 尝试多个可能的config.json路径
                script_dir = os.path.dirname(os.path.abspath(__file__))
                config_paths = [
                    os.path.join(script_dir, "config.json"),  # ocr_service目录
                    os.path.join(script_dir, "..", "config.json"),  # 项目根目录
                ]

                for config_path in config_paths:
                    try:
                        if os.path.exists(config_path):
                            with open(config_path, "r", encoding="utf-8") as f:
                                config = json.load(f)
                                self.api_key = config.get("baidu_ocr", {}).get("api_key", "")
                                self.secret_key = config.get("baidu_ocr", {}).get("secret_key", "")
                                if self.api_key and self.secret_key:
                                    break
                    except Exception as e:
                        continue
            except:
                pass

    def is_configured(self) -> bool:
        """检查是否已配置"""
        return bool(self.api_key and self.secret_key)

# 百度OCR客户端
class BaiduOCRClient:
    def __init__(self, api_key: str, secret_key: str):
        self.api_key = api_key
        self.secret_key = secret_key
        self.access_token = None
        self.token_expire_time = 0

    def get_access_token(self) -> str:
        """获取access_token"""
        import time

        # 检查token是否过期
        if self.access_token and time.time() < self.token_expire_time:
            return self.access_token

        # 获取新的token
        url = "https://aip.baidubce.com/oauth/2.0/token"
        params = {
            "grant_type": "client_credentials",
            "client_id": self.api_key,
            "client_secret": self.secret_key
        }

        try:
            response = requests.post(url, params=params, timeout=10)
            response.raise_for_status()
            result = response.json()

            if "access_token" in result:
                self.access_token = result["access_token"]
                # 提前5分钟过期
                self.token_expire_time = time.time() + result.get("expires_in", 2592000) - 300
                return self.access_token
            else:
                raise Exception(f"获取access_token失败: {result}")
        except Exception as e:
            raise Exception(f"获取access_token异常: {str(e)}")

    def recognize_text(self, image_data: bytes) -> dict:
        """调用百度通用文字识别API"""
        try:
            # 获取access_token
            access_token = self.get_access_token()

            # 编码图片
            image_base64 = base64.b64encode(image_data).decode('utf-8')

            # 调用API
            url = "https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic"
            headers = {"Content-Type": "application/x-www-form-urlencoded"}
            data = {"image": image_base64}

            response = requests.post(
                url,
                headers=headers,
                data=data,
                params={"access_token": access_token},
                timeout=10
            )
            response.raise_for_status()
            result = response.json()

            # 检查API错误
            if "error_code" in result:
                error_msg = result.get("error_msg", "未知错误")
                if result["error_code"] == 17:  # 每日流量限制
                    return {
                        "success": False,
                        "error": "每日流量超限",
                        "error_code": result["error_code"],
                        "error_msg": error_msg,
                        "note": "建议升级到更高版本或等待明天重置"
                    }
                elif result["error_code"] == 18:  # QPS超限
                    return {
                        "success": False,
                        "error": "QPS超限",
                        "error_code": result["error_code"],
                        "error_msg": error_msg,
                        "note": "请求过于频繁，请稍后重试"
                    }
                else:
                    return {
                        "success": False,
                        "error": error_msg,
                        "error_code": result["error_code"]
                    }

            # 解析识别结果
            if "words_result" in result:
                text_lines = [item["words"] for item in result["words_result"]]
                full_text = "\n".join(text_lines)

                return {
                    "success": True,
                    "text": full_text,
                    "words_result": result["words_result"],
                    "lines_count": len(text_lines)
                }
            else:
                return {
                    "success": False,
                    "error": "未识别到文字",
                    "result": result
                }

        except requests.exceptions.Timeout:
            return {
                "success": False,
                "error": "请求超时",
                "note": "网络连接超时，请检查网络"
            }
        except requests.exceptions.RequestException as e:
            return {
                "success": False,
                "error": f"网络请求失败: {str(e)}",
                "note": "请检查网络连接"
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"识别异常: {str(e)}"
            }

# 全局配置和客户端
config = BaiduOCRConfig()
ocr_client = None

if config.is_configured():
    try:
        ocr_client = BaiduOCRClient(config.api_key, config.secret_key)
    except Exception as e:
        print(f"警告: 初始化百度OCR客户端失败: {e}")
        ocr_client = None

# API模型
class OCRResponse(BaseModel):
    success: bool
    text: Optional[str] = None
    error: Optional[str] = None
    words_result: Optional[list] = None
    lines_count: Optional[int] = None
    note: Optional[str] = None

# 健康检查
@app.get("/")
async def root():
    """API状态检查"""
    is_configured = config.is_configured()
    has_client = ocr_client is not None

    return {
        "message": "K12错题本 OCR服务 - 百度OCR版",
        "version": "0.3.0",
        "mode": "baidu_ocr",
        "baidu_ocr_configured": is_configured,
        "baidu_ocr_client": has_client,
        "api_key_prefix": config.api_key[:8] + "..." if config.api_key else "",
        "free_quota_info": {
            "personal": "1000次/月 (个人认证)",
            "enterprise": "2000次/月 (企业认证)",
            "reset": "每月1日重置"
        } if is_configured else None
    }

# OCR识别接口
@app.post("/ocr/text", response_model=OCRResponse)
async def recognize_text(file: UploadFile = File(...)):
    """识别图片中的文字"""

    # 检查配置
    if not config.is_configured():
        return OCRResponse(
            success=False,
            error="未配置百度云API密钥",
            note="请在config.json中配置api_key和secret_key"
        )

    # 检查客户端
    if not ocr_client:
        return OCRResponse(
            success=False,
            error="百度OCR客户端未初始化",
            note="请检查API密钥是否正确"
        )

    try:
        # 读取图片
        image_data = await file.read()

        # 检查文件大小
        if len(image_data) > 10 * 1024 * 1024:  # 10MB
            return OCRResponse(
                success=False,
                error="图片文件过大",
                note="百度OCR限制最大10MB，建议压缩后重试"
            )

        # 调用百度OCR
        result = ocr_client.recognize_text(image_data)

        return OCRResponse(**result)

    except Exception as e:
        return OCRResponse(
            success=False,
            error=f"处理失败: {str(e)}"
        )

# 测试接口
@app.post("/ocr/test")
async def test_ocr():
    """测试OCR功能（使用模拟数据）"""
    if not config.is_configured():
        return {
            "success": False,
            "error": "未配置百度云API密钥",
            "config_status": {
                "api_key": bool(config.api_key),
                "secret_key": bool(config.secret_key)
            }
        }

    return {
        "success": True,
        "message": "百度OCR配置正常",
        "api_key_prefix": config.api_key[:8] + "...",
        "note": "请通过前端上传图片测试实际识别功能"
    }

if __name__ == "__main__":
    import uvicorn

    print("=" * 60)
    print("K12错题本 - 百度OCR服务")
    print("=" * 60)

    if config.is_configured():
        print("状态: 百度OCR已配置")
        print(f"API Key: {config.api_key[:8]}...{config.api_key[-4:]}")
        print(f"Secret Key: {config.secret_key[:4]}...{config.secret_key[-4:]}")
        print("\n免费额度:")
        print("  - 个人认证: 1000次/月")
        print("  - 企业认证: 2000次/月")
        print("  - 重置时间: 每月1日")
        print("\n服务启动中...")
    else:
        print("状态: 未配置百度OCR密钥")
        print("提示: 请在config.json中配置api_key和secret_key")
        print("\n将在模拟模式下运行...")

    print("=" * 60)

    uvicorn.run(app, host="0.0.0.0", port=8001)
