# 🎯 K12智能错题本 - POC项目

> 用开源OCR + 小模型验证技术可行性，两周内决定Go/No-Go

---

## 📊 项目状态

```
✅ Week 1 基础设施搭建完成 (2025-02-21)
🔄 Week 2 并行执行中
🎯 Week 4 决策点: Go/No-Go
```

**当前进度**: 60% | **目标**: 验证技术可行性

---

## 🎯 项目目标

### 核心假设验证
| 假设 | 验证方法 | 成功标准 | 当前状态 |
|------|---------|---------|---------|
| 开源OCR能识别数学公式 | PaddleOCR测试 | 准确率>85% | 🟡 待测试 |
| 小模型能进行错因分类 | Qwen2.5-7B微调 | F1>75% | 🟡 待测试 |
| 端到端流程可行 | 整合测试 | 延迟<5秒 | 🟡 待测试 |

### 差异化机会
- 🔴 **AI深度错因诊断** (知识/思维/习惯三维)
- 🔴 **智能复习提醒** (艾宾浩斯曲线)
- 🔴 **知识图谱可视化**
- 🔴 **家校轻量协同**

---

## 🛠️ 技术栈

```
前端: React + Vite + TailwindCSS
OCR:  PaddleOCR (文字) + LaTeX-OCR (公式)
AI:   Qwen2.5-7B (Ollama本地运行)
API:  FastAPI
存储: LocalStorage (POC阶段)
```

---

## 📁 项目结构

```
K12-Mistake-Notebook-POC/
├── frontend/              # React Web界面
│   ├── src/
│   │   ├── components/   # 录入页、列表页等
│   │   ├── services/     # API封装
│   │   └── App.jsx       # 主应用
│   ├── package.json
│   └── vite.config.js
├── ocr_service/           # OCR识别服务 (端口8001)
│   └── app.py
├── ai_service/            # AI分析服务 (端口8002)
│   └── app.py
├── data/                  # 测试数据
│   ├── raw/              # 原始错题图片
│   ├── processed/        # 处理后数据
│   └── test_mistakes.md  # 测试题集
├── docs/                  # 文档
│   ├── 竞品测试计划.md
│   └── 原型设计规范.md
├── README.md              # 本文件
├── requirements.txt       # Python依赖
├── quickstart.bat         # Windows启动脚本
└── EXECUTION_GUIDE.md     # 执行指南 ⭐
```

---

## 🚀 快速开始

### 1. 环境要求
- Python 3.10+
- Node.js 18+
- Ollama (可选，用于AI功能)

### 2. 安装依赖

```bash
# Python依赖
pip install -r requirements.txt

# 前端依赖
cd frontend
npm install
cd ..
```

### 3. 启动服务

**方式1: 使用启动脚本**
```bash
# Windows
quickstart.bat

# Mac/Linux
./quickstart.sh
```

**方式2: 手动启动** (3个终端窗口)
```bash
# 终端1: OCR服务
python ocr_service/app.py

# 终端2: AI服务
python ai_service/app.py

# 终端3: 前端
cd frontend && npm run dev
```

### 4. 访问应用

打开浏览器访问: http://localhost:5173

---

## 📱 核心功能

### 1. 错题录入
- 📸 拍照/上传错题图片
- 🔍 OCR自动识别题目
- ✏️ 手动编辑识别结果
- 📝 填写错误答案

### 2. AI错因分析
- 🧠 三维分析 (知识点/思维/习惯)
- 🎯 定位根本原因
- 💡 提供改进建议
- 🔗 推荐关联概念

### 3. 错题管理
- 📚 错题列表查看
- 🏷️ 按科目/年级筛选
- 📊 学习数据统计
- 🔄 复习进度追踪

---

## 🧪 测试指南

### POC功能测试

**测试场景**: 录入一道数学错题

1. 打开 http://localhost:5173
2. 点击"录入错题"
3. 上传错题图片
4. 确认OCR识别结果
5. 填写错误答案
6. 点击"AI智能分析"
7. 查看分析结果
8. 保存到错题本

**测试数据**: 参考 `data/test_mistakes.md`

### API测试

```bash
# OCR测试
curl -X POST http://localhost:8001/ocr/text \
  -F "file=@data/raw/test.jpg"

# AI分析测试
curl -X POST http://localhost:8002/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "question": "解方程 x² + 2x + 1 = 0",
    "wrong_answer": "x = -1",
    "correct_answer": "x₁=x₂=-1",
    "subject": "数学",
    "grade": "初二"
  }'
```

---

## 📊 验证指标

| 指标 | 目标 | 测试方法 | 状态 |
|------|------|---------|------|
| OCR准确率 | ≥85% | 100道题测试 | 🟡 待测 |
| AI分类F1 | ≥75% | 50道题测试 | 🟡 待测 |
| 端到端延迟 | ≤5秒 | 10次测量 | 🟡 待测 |
| 用户满意度 | ≥4/5 | 用户测试 | 🟡 待测 |

---

## 📅 时间线

### Week 1 (2025-02-21 ~ 02-27)
- ✅ 基础设施搭建
- 🔄 POC功能开发
- 🔄 竞品深度测试
- 🔄 原型线框图

### Week 2 (2025-02-28 ~ 03-06)
- 📋 Ollama模型部署
- 📋 AI功能集成
- 📋 端到端测试
- 📋 竞品报告整理

### Week 3 (2025-03-07 ~ 03-13)
- 📋 数据收集优化
- 📋 性能调优
- 📋 用户测试
- 📋 原型迭代

### Week 4 (2025-03-14 ~ 03-20)
- 📋 结果汇总
- 🎯 **Go/No-Go决策**
- 📋 下一阶段规划

---

## 💰 预算

**总预算**: ¥5,000

| 项目 | 预算 | 说明 |
|------|------|------|
| 开源工具 | ¥0 | PaddleOCR, Ollama |
| API调用 | ¥200 | OpenAI Embeddings |
| 云服务器 | ¥300 | 阿里云/腾讯云 |
| 数据标注 | ¥500 | 众包标注 |
| 竞品会员 | ¥50 | 作业帮1周 |
| **总计** | **¥1,050** | |

---

## 🎯 Go/No-Go 决策标准

### ✅ Go条件 (全部满足)
- [ ] OCR准确率 ≥ 85%
- [ ] AI分类F1 ≥ 75%
- [ ] 端到端延迟 ≤ 5秒
- [ ] 发现3个以上差异化机会
- [ ] 原型用户满意度 ≥ 4/5

### 📋 Go后行动
- 启动React Native全栈开发
- 组建开发团队
- 制定详细产品路线图

### 🛑 No-Go行动
- 调整技术方案 (商用API)
- 寻找新切入点
- 或暂停项目重新评估

---

## 📖 相关文档

- [执行指南](EXECUTION_GUIDE.md) - ⭐ 立即行动指南
- [项目看板](PROJECT_DASHBOARD.md) - 进度跟踪
- [竞品测试计划](docs/竞品测试计划.md)
- [原型设计规范](docs/原型设计规范.md)
- [测试数据集](data/test_mistakes.md)

---

## 🆘 常见问题

### Q: OCR识别不准确怎么办？
A: POC阶段使用开源PaddleOCR，如果不达标可切换到百度/腾讯OCR API

### Q: AI模型效果不好？
A: 可以调整Prompt，或升级到Qwen-14B，或使用API版本

### Q: 本地运行太慢？
A: 建议配置: GPU或至少16GB内存，或使用云端服务器

### Q: 如何参与测试？
A: 参考 [EXECUTION_GUIDE.md](EXECUTION_GUIDE.md)

---

## 📞 联系方式

- 项目负责人: [你的名字]
- 技术支持: Claude/PAI AI Assistant
- 问题反馈: 直接在项目中提Issue

---

## 📄 许可证

MIT License - 自由使用和修改

---

**让我们一起用技术改变K12教育！🚀**

最后更新: 2025-02-21 18:05
