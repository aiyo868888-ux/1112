"""
腾讯OCR集成服务
支持: 通用印刷体识别、数学公式识别
"""
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import io
import base64
import hmac
import hashlib
import time
import requests
from typing import Optional
import json

app = FastAPI(title="K12错题本 OCR服务 - 腾讯OCR版")

# 允许跨域
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 腾讯云API配置
TENCENT_OCR_CONFIG = {
    "secret_id": "",  # 从环境变量或配置文件读取
    "secret_key": "",
    "endpoint": "ocr.tencentcloudapi.com",
    "region": "ap-guangzhou",
    "version": "2018-11-19"
}

class TencentOCRClient:
    """腾讯OCR客户端"""

    def __init__(self, secret_id: str, secret_key: str):
        self.secret_id = secret_id
        self.secret_key = secret_key
        self.endpoint = "ocr.tencentcloudapi.com"
        self.region = "ap-guangzhou"
        self.version = "2018-11-19"

    def _sign(self, secret_id, secret_key, payload):
        """腾讯云API签名算法"""
        service = "ocr"
        host = self.endpoint
        algorithm = "TC3-HMAC-SHA256"
        timestamp = int(time.time())
        date = time.strftime("%Y-%m-%d", time.gmtime(timestamp))

        # 步骤1：拼接规范请求串
        http_request_method = "POST"
        canonical_uri = "/"
        canonical_querystring = ""
        ct = "application/json; charset=utf-8"
        canonical_headers = f"content-type:{ct}\nhost:{host}\n"
        signed_headers = "content-type;host"

        hashed_request_payload = hashlib.sha256(payload.encode("utf-8")).hexdigest()
        canonical_request = (
            http_request_method + "\n" +
            canonical_uri + "\n" +
            canonical_querystring + "\n" +
            canonical_headers + "\n" +
            signed_headers + "\n" +
            hashed_request_payload
        )

        # 步骤2：拼接待签名字符串
        credential_scope = date + "/" + service + "/" + "tc3_request"
        hashed_canonical_request = hashlib.sha256(canonical_request.encode("utf-8")).hexdigest()
        string_to_sign = (
            algorithm + "\n" +
            str(timestamp) + "\n" +
            credential_scope + "\n" +
            hashed_canonical_request
        )

        # 步骤3：计算签名
        def _hmac_sha256(key, msg):
            return hmac.new(key, msg.encode("utf-8"), hashlib.sha256).digest()

        secret_date = _hmac_sha256(("TC3" + secret_key).encode("utf-8"), date)
        secret_key = _hmac_sha256(secret_date, service)
        secret_signing = _hmac_sha256(secret_key, "tc3_request")
        signature = hmac.new(secret_signing, string_to_sign.encode("utf-8"), hashlib.sha256).hexdigest()

        # 步骤4：拼接Authorization
        authorization = (
            algorithm + " " +
            "Credential=" + secret_id + "/" + credential_scope + ", " +
            "SignedHeaders=" + signed_headers + ", " +
            "Signature=" + signature
        )

        return {
            "Authorization": authorization,
            "Host": host,
            "Content-Type": ct,
            "X-TC-Action": "GeneralBasicOCR",
            "X-TC-Timestamp": str(timestamp),
            "X-TC-Version": self.version,
            "X-TC-Region": self.region
        }

    async def general_ocr(self, image_base64: str) -> dict:
        """
        通用印刷体识别（GeneralBasicOCR）

        Args:
            image_base64: base64编码的图片

        Returns:
            识别结果
        """
        if not self.secret_id or not self.secret_key:
            return {
                "success": False,
                "error": "未配置腾讯云API密钥",
                "text": "",
                "mock": True,
                "mock_data": "请配置腾讯云API密钥或在config.json中设置"
            }

        try:
            # 构造请求
            payload = {
                "ImageBase64": image_base64
            }

            # 生成签名
            headers = self._sign(
                self.secret_id,
                self.secret_key,
                json.dumps(payload)
            )

            # 发送请求
            url = f"https://{self.endpoint}/"
            response = requests.post(url, headers=headers, json=payload, timeout=10)

            if response.status_code == 200:
                result = response.json()

                if "Response" in result:
                    response_data = result["Response"]

                    # 提取识别的文本
                    text_lines = []
                    details = []

                    if "TextDetections" in response_data:
                        for item in response_data["TextDetections"]:
                            text_lines.append(item["DetectedText"])
                            details.append({
                                "text": item["DetectedText"],
                                "confidence": item.get("Confidence", 0),
                                "polygon": item.get("Polygon", {})
                            })

                    return {
                        "success": True,
                        "text": "\n".join(text_lines),
                        "details": details,
                        "request_id": response_data.get("RequestId", ""),
                        "mock": False
                    }
                else:
                    return {
                        "success": False,
                        "error": "API响应格式错误",
                        "text": "",
                        "mock": False
                    }
            else:
                return {
                    "success": False,
                    "error": f"HTTP {response.status_code}: {response.text}",
                    "text": "",
                    "mock": False
                }

        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "text": "",
                "mock": False
            }

# 全局OCR客户端
ocr_client: Optional[TencentOCRClient] = None

def init_ocr_client():
    """初始化OCR客户端"""
    global ocr_client

    # 尝试从环境变量读取
    import os
    secret_id = os.environ.get("TENCENT_SECRET_ID", "")
    secret_key = os.environ.get("TENCENT_SECRET_KEY", "")

    # 尝试从配置文件读取
    if not secret_id or not secret_key:
        try:
            with open("config.json", "r", encoding="utf-8") as f:
                config = json.load(f)
                secret_id = config.get("tencent_ocr", {}).get("secret_id", "")
                secret_key = config.get("tencent_ocr", {}).get("secret_key", "")
        except:
            pass

    if secret_id and secret_key:
        ocr_client = TencentOCRClient(secret_id, secret_key)
        print("Tencent OCR client initialized")
        return True
    else:
        print("Warning: Tencent OCR credentials not found, using mock mode")
        ocr_client = None
        return False

@app.on_event("startup")
async def startup_event():
    """服务启动时初始化"""
    init_ocr_client()

@app.get("/")
async def root():
    status = "tencent_ocr" if ocr_client else "mock"
    return {
        "message": f"K12错题本 OCR服务 - 腾讯OCR版",
        "version": "0.2.0",
        "mode": status,
        "tencent_ocr": ocr_client is not None
    }

@app.post("/ocr/text")
async def recognize_text(file: UploadFile = File(...)):
    """
    识别图片中的文字内容

    使用腾讯OCR通用印刷体识别
    """
    try:
        # 读取图片
        contents = await file.read()

        # 转换为base64
        image_base64 = base64.b64encode(contents).decode("utf-8")

        # 如果有真实OCR客户端，使用真实OCR
        if ocr_client:
            result = await ocr_client.general_ocr(image_base64)

            if result["success"]:
                return {
                    "success": True,
                    "text": result["text"],
                    "details": result["details"],
                    "char_count": len(result["text"]),
                    "mode": "tencent_ocr",
                    "request_id": result.get("request_id", "")
                }
            else:
                return {
                    "success": False,
                    "error": result["error"],
                    "text": ""
                }
        else:
            # 使用模拟数据
            mock_text = """解方程 x² + 2x + 1 = 0

已知一元二次方程：x² + 2x + 1 = 0
求：方程的解

注意：当前使用模拟数据，请配置腾讯云API密钥启用真实OCR识别"""

            return {
                "success": True,
                "text": mock_text,
                "details": [
                    {"text": "解方程 x² + 2x + 1 = 0", "confidence": 0.95},
                    {"text": "已知一元二次方程：x² + 2x + 1 = 0", "confidence": 0.92},
                    {"text": "求：方程的解", "confidence": 0.98}
                ],
                "char_count": len(mock_text),
                "mode": "mock",
                "note": "未配置腾讯云API密钥，使用模拟数据"
            }

    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "text": ""
        }

@app.post("/ocr/formula")
async def recognize_formula(file: UploadFile = File(...)):
    """
    识别数学公式（占位符）

    腾讯OCR暂不支持公式识别，返回通用文字识别结果
    """
    result = await recognize_text(file)
    return {
        "success": result["success"],
        "latex": result.get("text", ""),
        "mode": result.get("mode", "unknown"),
        "note": "公式识别功能待开发，当前使用通用OCR"
    }

if __name__ == "__main__":
    import uvicorn
    print("OCR Service starting with Tencent OCR...")
    print("Address: http://localhost:8001")
    print("\nTo enable Tencent OCR:")
    print("1. Create config.json with your credentials")
    print("2. Or set environment variables: TENCENT_SECRET_ID, TENCENT_SECRET_KEY")
    uvicorn.run(app, host="0.0.0.0", port=8001)
