import os
import subprocess

def run_script(name):
    print(f"\n🚀 正在运行 {name}...")
    result = subprocess.run(["python", os.path.join(os.getcwd(), name)], 
                            capture_output=True, text=True)
    print(result.stdout)
    if result.stderr:
        print("❌ 错误:", result.stderr)

# 执行顺序
run_script("generate_data.py")   # 1. 造数+ETL
run_script("visualize.py")       # 2. 生成可视化
run_script("ai_analysis.py")     # 3. AI分析（演示模式）
run_script("monitor.py")         # 4. 数据监控

print("\n🎉 恭喜！你的完整数仓项目一键运行完成！")
print("📁 去桌面查看 gmv_trend.html 和 order_count.html")