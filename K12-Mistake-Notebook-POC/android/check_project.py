"""
Android项目完整性检查
"""
import os
import sys

# 设置控制台编码为UTF-8
if sys.platform == "win32":
    import codecs
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter("utf-8")(sys.stderr.buffer, 'strict')

def check_android_project():
    print("=" * 70)
    print("Android项目完整性检查")
    print("=" * 70)

    project_path = "/d/mine/me/Personal_AI_Infrastructure/K12-Mistake-Notebook-POC/android"

    # 必需文件列表
    required_files = {
        "根目录配置": [
            "settings.gradle.kts",
            "build.gradle.kts",
            "gradle.properties",
        ],
        "App模块": [
            "app/build.gradle.kts",
            "app/src/main/AndroidManifest.xml",
        ],
        "资源文件": [
            "app/src/main/res/values/strings.xml",
            "app/src/main/res/values/themes.xml",
        ],
        "源代码": [
            "app/src/main/java/com/k12/mistake/notebook/MainActivity.kt",
            "app/src/main/java/com/k12/mistake/notebook/MistakeNotebookApp.kt",
        ],
        "UI组件": [
            "app/src/main/java/com/k12/mistake/notebook/ui/navigation/MistakeNavigation.kt",
            "app/src/main/java/com/k12/mistake/notebook/ui/home/HomeScreen.kt",
            "app/src/main/java/com/k12/mistake/notebook/ui/camera/CameraScreen.kt",
            "app/src/main/java/com/k12/mistake/notebook/ui/selection/SelectionScreen.kt",
            "app/src/main/java/com/k12/mistake/notebook/ui/save/SaveScreen.kt",
            "app/src/main/java/com/k12/mistake/notebook/ui/organize/OrganizeScreen.kt",
        ],
        "主题": [
            "app/src/main/java/com/k12/mistake/notebook/ui/theme/Color.kt",
            "app/src/main/java/com/k12/mistake/notebook/ui/theme/Theme.kt",
            "app/src/main/java/com/k12/mistake/notebook/ui/theme/Type.kt",
        ]
    }

    total_files = 0
    existing_files = 0
    missing_files = []

    for category, files in required_files.items():
        print(f"\n[{category}]")
        for file_path in files:
            total_files += 1
            full_path = os.path.join(project_path, file_path)

            if os.path.exists(full_path):
                print(f"  [OK] {file_path}")
                existing_files += 1
            else:
                print(f"  [MISSING] {file_path}")
                missing_files.append(file_path)

    print("\n" + "=" * 70)
    print("检查总结")
    print("=" * 70)
    print(f"\n总文件数: {total_files}")
    print(f"已存在: {existing_files}")
    print(f"缺失: {total_files - existing_files}")

    if missing_files:
        print(f"\n缺失的文件:")
        for file in missing_files:
            print(f"  - {file}")
    else:
        print("\n[OK] 所有必需文件都已创建！")
        print("\n下一步:")
        print("  1. 打开Android Studio")
        print("  2. File -> Open -> 选择android文件夹")
        print("  3. 等待Gradle同步完成")
        print("  4. 连接Android设备或启动模拟器")
        print("  5. 点击运行按钮 ▶️")

    print("\n" + "=" * 70)

    return len(missing_files) == 0

if __name__ == "__main__":
    success = check_android_project()
    sys.exit(0 if success else 1)
