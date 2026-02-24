# 🔧 腾讯OCR API设置指南

## 📋 前置准备

### 所需材料
- [ ] 腾讯云账号（免费注册）
- [ ] 手机号（用于验证）
- [ ] 身份信息（用于实名认证）

---

## 🚀 快速开始（5分钟）

### 步骤1: 注册腾讯云账号

1. 访问：https://cloud.tencent.com/
2. 点击右上角"免费注册"
3. 使用手机号注册
4. 完成实名认证（需要身份证）

### 步骤2: 开通OCR服务

1. 访问：https://cloud.tencent.com/product/ocr
2. 点击"立即使用"
3. 进入OCR控制台

### 步骤3: 获取API密钥

**方式A: 在OCR控制台获取**
1. 访问：https://console.cloud.tencent.com/ocr
2. 点击左侧"API密钥管理"
3. 查看或创建密钥
4. 记录 **SecretId** 和 **SecretKey**

**方式B: 在访问管理获取**
1. 访问：https://console.cloud.tencent.com/cam/capi
2. 查看现有密钥或创建新密钥
3. 记录 **SecretId** 和 **SecretKey**

⚠️ **重要**: SecretKey只在创建时显示一次，请立即保存！

### 步骤4: 配置本地环境

**方式A: 使用配置文件（推荐）**

1. 复制配置文件模板：
```bash
cd K12-Mistake-Notebook-POC
cp config.json.example config.json
```

2. 编辑 `config.json`，填入你的密钥：
```json
{
  "tencent_ocr": {
    "secret_id": "AKIDxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    "secret_key": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    "region": "ap-guangzhou"
  }
}
```

**方式B: 使用环境变量**

```bash
# Windows PowerShell
$env:TENCENT_SECRET_ID="你的SecretId"
$env:TENCENT_SECRET_KEY="你的SecretKey"

# Windows CMD
set TENCENT_SECRET_ID=你的SecretId
set TENCENT_SECRET_KEY=你的SecretKey

# Linux/Mac
export TENCENT_SECRET_ID="你的SecretId"
export TENCENT_SECRET_KEY="你的SecretKey"
```

### 步骤5: 启动服务

1. 停止当前OCR服务（如果正在运行）
2. 启动新的腾讯OCR版本：
```bash
cd ocr_service
python tencent_ocr_app.py
```

3. 访问 http://localhost:8001 查看状态
   - 应显示 `"mode": "tencent_ocr"`
   - 应显示 `"tencent_ocr": true`

---

## 🧪 测试OCR功能

### 测试1: API状态检查
```bash
curl http://localhost:8001/
```

**预期输出**（配置成功）：
```json
{
  "message": "K12错题本 OCR服务 - 腾讯OCR版",
  "version": "0.2.0",
  "mode": "tencent_ocr",
  "tencent_ocr": true
}
```

### 测试2: 图片识别测试

在浏览器中：
1. 访问 http://localhost:5173
2. 点击"录入错题"
3. 上传一张包含文字的图片
4. 点击"🔄 重新识别"

**预期结果**：
- 真实识别图片中的文字内容
- 准确率 > 95%
- 识别速度 < 3秒

---

## 💰 费用说明

### 免费额度
- ✅ 每月 **1000次** 免费调用
- ✅ 通用印刷体识别（GeneralBasicOCR）

### 计费标准（超出免费额度）
- 通用印刷体识别：¥0.0015/次
- 数学公式识别：¥0.002/次

### 预估费用
- 每天录入10道错题 × 30天 = 300次/月
- 免费额度1000次/月
- **个人使用完全免费**

---

## ⚠️ 常见问题

### Q1: 提示"未配置腾讯云API密钥"
**A**: 检查以下几点：
- [ ] config.json 文件是否存在
- [ ] SecretId 和 SecretKey 是否正确填入
- [ ] config.json 是否在项目根目录
- [ ] 服务是否重启

### Q2: 识别结果为空
**A**: 可能原因：
- 图片格式不支持（建议JPG/PNG）
- 图片太大（建议 < 5MB）
- 图片中无文字
- API密钥权限不足

### Q3: 识别速度慢
**A**: 正常情况：
- 首次调用：2-3秒
- 后续调用：< 1秒
- 如果持续超过3秒，检查网络连接

### Q4: 准确率低
**A**: 优化建议：
- 使用清晰图片（分辨率 > 300dpi）
- 避免反光和阴影
- 确保文字水平
- 手写体识别率较低（印刷体最佳）

### Q5: 数学公式识别不准确
**A**: 当前限制：
- 腾讯OCR通用版不支持公式识别
- 建议：
  - 先用通用OCR识别文字
  - 公式部分手动编辑
  - 未来可集成专业公式OCR

---

## 🔐 安全建议

### 保护API密钥
1. ✅ 不要将 config.json 提交到Git
2. ✅ 已添加到 .gitignore
3. ✅ 不要在公开代码中暴露密钥
4. ✅ 定期轮换密钥

### 权限管理
- 为OCR服务创建专用子账号
- 只授予必要权限
- 设置访问密钥IP白名单

---

## 📊 性能指标

| 指标 | 腾讯OCR | 模拟OCR |
|------|---------|---------|
| 准确率 | 95%+ | N/A |
| 速度 | 1-2秒 | < 1秒 |
| 费用 | 免费1000次/月 | 免费 |
| 公式支持 | ❌ | ❌ |
| 手写体 | ⚠️ 一般 | ❌ |

---

## 🎯 下一步

配置完成后：
1. ✅ 测试真实图片识别
2. ✅ 对比识别准确率
3. ✅ 收集测试反馈
4. ✅ 决定是否继续使用腾讯OCR

---

**需要帮助？**
- 腾讯云文档：https://cloud.tencent.com/document/product/866
- OCR技术支持：提交工单
- 或联系项目维护者

---

**祝使用愉快！** 🚀
