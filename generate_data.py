import pymysql
import random
from datetime import date, datetime, timedelta

# ===================== 数据库连接 =====================
conn = pymysql.connect(
    host="localhost",
    user="root",
    password="root123456",
    database="ecom_dw",
    charset="utf8mb4"
)
cursor = conn.cursor()

print("🚀 正在生成今日测试数据...")

# ===================== 1. 一次性获取最大订单ID，保证绝对唯一 =====================
cursor.execute("SELECT MAX(order_id) FROM ods_order")
max_order_id = cursor.fetchone()[0] or 0
current_order_id = max_order_id + 1

today = date.today()
order_list = []

# 生成50条今日新订单
for i in range(50):
    user_id = random.randint(1, 1000)
    order_amount = round(random.uniform(100, 5000), 2)
    pay_status = 1
    order_time = datetime.combine(today, datetime.min.time()) + timedelta(hours=random.randint(0, 23))
    
    order_list.append((current_order_id, user_id, order_amount, pay_status, order_time))
    current_order_id += 1

# 批量插入订单
cursor.executemany("""
    INSERT INTO ods_order (order_id, user_id, order_amount, pay_status, order_time)
    VALUES (%s, %s, %s, %s, %s)
""", order_list)
conn.commit()

print(f"✅ 成功生成 {len(order_list)} 条今日订单数据！")

# ===================== 2. 自动刷新全链路ETL =====================
print("\n🔄 正在刷新数仓全链路...")

# 刷新DWD层
cursor.execute("TRUNCATE TABLE dwd_order_detail")
cursor.execute("INSERT INTO dwd_order_detail SELECT * FROM ods_order WHERE pay_status = 1")
conn.commit()

# 刷新DWS层
cursor.execute("TRUNCATE TABLE dws_user_order_summary")
cursor.execute("""
    INSERT INTO dws_user_order_summary
    SELECT user_id, DATE(order_time) AS order_date,
           COUNT(order_id) AS order_cnt,
           SUM(order_amount) AS total_amount
    FROM dwd_order_detail
    GROUP BY user_id, DATE(order_time)
""")
conn.commit()

# 刷新ADS层
cursor.execute("TRUNCATE TABLE ads_order_daily_report")
cursor.execute("""
    INSERT INTO ads_order_daily_report
    SELECT order_date,
           SUM(order_cnt) AS total_order_cnt,
           SUM(total_amount) AS total_order_amount,
           AVG(total_amount) AS avg_user_amount
    FROM dws_user_order_summary
    GROUP BY order_date
    ORDER BY order_date DESC
""")
conn.commit()

print("✅ 数仓ETL全流程刷新完成！")

# ===================== 结束 =====================
cursor.close()
conn.close()
print("\n🎉 今日数据生成+数仓刷新全部完成！")
print("👉 运行 monitor.py 查看监控报告")