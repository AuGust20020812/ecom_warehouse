import pymysql
import requests

# --------------------- 数据库连接 ---------------------
conn = pymysql.connect(
    host="localhost",
    user="root",
    password="root123456",
    database="ecom_dw",
    charset="utf8mb4"
)
cursor = conn.cursor()

# --------------------- 你的 API Key ---------------------
API_KEY = "06403524-e3e5-4ffb-b9d9-517f96fb060d"
BASE_URL = "https://ark.cn-beijing.volces.com/api/v3"

def ai_generate_sql(question):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "doubao-seed-1.6-flash",
        "messages": [
            {
                "role": "system",
                "content": """你是专业MySQL数据分析师。
表名：ads_order_daily_report
字段：order_date, total_order_cnt, total_order_amount, avg_user_amount
要求：
1. 涉及“最近10天/最近5天/最新” 必须加 ORDER BY order_date DESC
2. 只返回标准SQL语句，不要任何解释、不要废话、不要多余文字。"""
            },
            {"role": "user", "content": question}
        ]
    }

    try:
        response = requests.post(f"{BASE_URL}/chat/completions", json=data, headers=headers)
        res_json = response.json()
        return res_json["choices"][0]["message"]["content"].strip()
    except Exception as e:
        print(f"⚠️ API调用失败，启用演示模式: {e}")
        # 演示兜底逻辑
        if "最近" in question and ("销售额" in question or "GMV" in question):
            return "SELECT order_date, total_order_amount FROM ads_order_daily_report ORDER BY order_date DESC LIMIT 10;"
        elif "最近" in question and "订单" in question:
            return "SELECT order_date, total_order_cnt FROM ads_order_daily_report ORDER BY order_date DESC LIMIT 10;"
        else:
            return "SELECT * FROM ads_order_daily_report ORDER BY order_date DESC LIMIT 5;"

# --------------------- 主程序 ---------------------
print("=" * 60)
print("🤖 电商数仓 AI 智能分析助手（已接入豆包大模型）")
print("💡 输入问题即可自动分析数据，输入 exit 退出")
print("=" * 60)

while True:
    question = input("\n请输入你的分析问题：")
    if question.lower() == "exit":
        break

    try:
        sql = ai_generate_sql(question)
        print(f"\n✅ AI 生成的 SQL：\n{sql}")

        cursor.execute(sql)
        results = cursor.fetchall()

        print("\n📊 分析结果（最新日期在前）：")
        for row in results:
            print(row)
    except Exception as e:
        print(f"❌ 执行失败：{e}")

conn.close()