"""
K12错题本 - 服务状态检查脚本
检查所有服务的运行状态
"""
import requests
import sys

# 设置控制台编码为UTF-8
if sys.platform == "win32":
    import codecs
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter("utf-8")(sys.stderr.buffer, 'strict')

def check_service(name, url, expected_keys=None):
    """检查单个服务状态"""
    try:
        response = requests.get(url, timeout=3)
        data = response.json()

        print(f"\n{name}:")
        print(f"  URL: {url}")
        print(f"  状态: [OK] 运行中")

        # 显示关键信息
        if expected_keys:
            for key in expected_keys:
                if key in data:
                    value = data[key]
                    if isinstance(value, dict):
                        print(f"  {key}:")
                        for k, v in value.items():
                            print(f"    - {k}: {v}")
                    else:
                        print(f"  {key}: {value}")

        return True

    except requests.exceptions.ConnectionError:
        print(f"\n{name}:")
        print(f"  URL: {url}")
        print(f"  状态: [ERROR] 无法连接")
        return False
    except Exception as e:
        # 前端返回HTML，不是JSON，这是正常的
        if "5173" in url:
            print(f"\n{name}:")
            print(f"  URL: {url}")
            print(f"  状态: [OK] 运行中 (HTML)")
            return True
        print(f"\n{name}:")
        print(f"  URL: {url}")
        print(f"  状态: [ERROR] {str(e)}")
        return False

def main():
    print("=" * 70)
    print("K12错题本 - 服务状态检查")
    print("=" * 70)

    services = [
        {
            "name": "OCR服务 (百度OCR)",
            "url": "http://localhost:8001/",
            "keys": ["mode", "baidu_ocr_configured", "baidu_ocr_client", "api_key_prefix", "free_quota_info"]
        },
        {
            "name": "AI分析服务",
            "url": "http://localhost:8002/",
            "keys": ["mode", "ai_ready"]
        },
        {
            "name": "题目检测服务",
            "url": "http://localhost:8003/",
            "keys": ["methods", "note"]
        },
        {
            "name": "前端应用",
            "url": "http://localhost:5173/",
            "keys": None  # 前端返回HTML，不检查keys
        }
    ]

    results = []
    for service in services:
        result = check_service(service["name"], service["url"], service["keys"])
        results.append(result)

    print("\n" + "=" * 70)
    print("检查总结:")
    print("=" * 70)

    all_ok = all(results)
    ok_count = sum(results)
    total_count = len(results)

    print(f"\n总服务数: {total_count}")
    print(f"运行中: {ok_count}")
    print(f"未运行: {total_count - ok_count}")

    if all_ok:
        print("\n[OK] 所有服务运行正常！")
        print("\n可以开始测试了:")
        print("  1. 打开浏览器访问: http://localhost:5173")
        print("  2. 点击'录入错题'")
        print("  3. 上传图片测试AI自动检测题目")
        print("  4. 调整框选区域（可选）")
        print("  5. 点击'完成'测试OCR识别")
        print("  6. 点击'AI分析'测试智能分析")
    else:
        print("\n[WARNING] 部分服务未运行")
        print("\n请检查:")
        print("  - 服务是否已启动")
        print("  - 端口是否被占用")
        print("  - 配置文件是否正确")

    print("\n" + "=" * 70)

    return 0 if all_ok else 1

if __name__ == "__main__":
    sys.exit(main())
