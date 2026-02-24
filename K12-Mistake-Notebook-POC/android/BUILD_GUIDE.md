# 📱 Android构建指南

## 🔧 Android Studio构建步骤

### 1. 打开项目
1. 启动Android Studio
2. 选择 `File -> Open`
3. 浏览到: `D:\mine\me\Personal_AI_Infrastructure\K12-Mistake-Notebook-POC\android`
4. 点击"OK"

### 2. 等待Gradle同步
- Android Studio会自动开始Gradle同步
- 等待底部状态栏显示"Gradle sync finished"
- 如果同步失败，点击"Try Again"

### 3. 检查项目配置
- 确保`build.gradle`文件没有红色错误提示
- 确保SDK已安装（Android Studio会自动提示）

### 4. 运行应用
- 连接Android设备（USB调试已开启）
- 或启动Android模拟器（AVD Manager）
- 点击工具栏的绿色播放按钮 ▶️
- 选择目标设备
- 等待应用安装和启动

---

## ❓ 常见构建问题

### 问题1: Gradle同步失败
**解决方案**:
1. 检查网络连接
2. 在`build.gradle`中添加阿里云镜像：
```kotlin
maven { url = uri("https://maven.aliyun.com/repository/google") }
maven { url = uri("https://maven.aliyun.com/repository/public") }
```

### 问题2: SDK未安装
**解决方案**:
1. 打开SDK Manager（Tools -> SDK Manager）
2. 勾选"Android 14.0 (API 34)"
3. 点击"Apply"下载

### 问题3: 设备未识别
**解决方案**:
1. 确保USB调试已开启（设置 -> 开发者选项）
2. 安装手机驱动程序
3. 使用`adb devices`命令检查连接

### 问题4: 构建错误"Could not resolve"
**解决方案**:
1. 清理项目：`Build -> Clean Project`
2. 重新构建：`Build -> Rebuild Project`
3. 删除.gradle文件夹，重新同步

---

## 🔍 检查构建状态

### Android Studio提示位置
- **底部状态栏**: 显示Gradle同步状态
- **Build窗口**: View -> Tool Windows -> Build
- **Problems窗口**: View -> Tool Windows -> Problems

### 预期状态
- ✅ Gradle sync finished
- ✅ Build successful
- ✅ No errors

---

## 📱 设备要求

### 最低要求
- Android 7.0 (API 24) 或更高
- 2GB RAM
- 100MB可用存储

### 推荐配置
- Android 10 (API 29) 或更高
- 4GB RAM
- 500MB可用存储

---

## 🚀 快速验证

### 验证步骤
1. 打开Android Studio
2. 打开项目文件夹
3. 等待Gradle同步
4. 查看是否有红色错误提示
5. 尝试构建：Build -> Make Project

### 成功标志
- ✅ 左侧项目树显示正常
- ✅ 顶部工具栏显示运行按钮
- ✅ 底部状态栏显示"Ready"
- ✅ Build窗口显示"BUILD SUCCESSFUL"

---

## 💡 提示

**首次构建可能需要较长时间**（下载依赖）
- 耐心等待
- 保持网络连接
- 如果中断，重新同步即可

**构建完成后**:
- 可以在模拟器或真机上运行
- 查看UI和功能
- 测试拍照→选题→保存→组题流程

---

## 🎯 下一步

构建成功后：
1. 在手机上安装应用
2. 测试拍照功能
3. 测试AI选题（需要后端服务运行）
4. 测试保存和组题功能

**注意**: Android应用需要访问局域网的后端服务，确保手机和电脑在同一WiFi。

---

现在可以在Android Studio中打开项目了！
