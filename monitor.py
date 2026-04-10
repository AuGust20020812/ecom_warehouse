import pymysql
from datetime import date, datetime

# ===================== 数据库连接 =====================
conn = pymysql.connect(
    host="localhost",
    user="root",
    password="root123456",
    database="ecom_dw",
    charset="utf8mb4"
)
cursor = conn.cursor()

# ===================== 今日日期 =====================
today = date.today()
print("=" * 60)
print(f"📊 电商数仓 - 数据质量监控报告 | 日期：{today}")
print("=" * 60)

# ===================== 1. 监控 ODS 层原始数据 =====================
print("\n🔍 1. 原始数据层（ODS）监控")

# 今日订单量
cursor.execute("""
    SELECT COUNT(*) FROM ods_order 
    WHERE DATE(order_time) = %s
""", (today,))
order_today = cursor.fetchone()[0]
print(f"✅ 今日新增订单：{order_today} 条")

# 累计用户总数
cursor.execute("SELECT COUNT(*) FROM ods_user")
user_total = cursor.fetchone()[0]
print(f"✅ 累计用户总数：{user_total} 人")

# ===================== 2. 监控 DWD 明细数据 =====================
print("\n🔍 2. 明细数据层（DWD）监控")

cursor.execute("""
    SELECT COUNT(*) FROM dwd_order_detail 
    WHERE DATE(order_time) = %s
""", (today,))
dwd_today = cursor.fetchone()[0]
print(f"✅ 今日明细订单：{dwd_today} 条")

# ===================== 3. 监控 DWS 汇总数据 =====================
print("\n🔍 3. 汇总数据层（DWS）监控")

cursor.execute("""
    SELECT COUNT(*) FROM dws_user_order_summary 
    WHERE DATE(order_date) = %s
""", (today,))
dws_today = cursor.fetchone()[0]
print(f"✅ 今日用户汇总：{dws_today} 条")

# ===================== 4. 监控 ADS 业务报表 =====================
print("\n🔍 4. 应用数据层（ADS）监控")

cursor.execute("""
    SELECT total_order_cnt, total_order_amount, avg_user_amount 
    FROM ads_order_daily_report 
    WHERE order_date = %s
""", (today,))

ads_data = cursor.fetchone()

if ads_data:
    order_cnt, order_amount, avg_amount = ads_data
    print(f"✅ 今日总订单数：{order_cnt}")
    print(f"✅ 今日总销售额：{order_amount} 元")
    print(f"✅ 今日用户均价：{avg_amount} 元")
else:
    print("⚠️  警告：今日 ADS 日报未生成！")

# ===================== 5. 数据异常预警 =====================
print("\n🚨 5. 数据异常预警")

# 订单量低于 5 条就报警
if order_today < 5:
    print(f"🔴 严重预警：今日订单量过低！仅 {order_today} 条")
else:
    print(f"🟢 正常：今日订单量达标")

# ADS 日报是否生成
if not ads_data:
    print("🔴 严重预警：ADS 层日报缺失！")
else:
    print("🟢 正常：ADS 日报已生成")

# ===================== 结束 =====================
print("\n" + "=" * 60)
print("✅ 数仓数据监控完成！所有层数据健康检查完毕")
print("=" * 60)

cursor.close()
conn.close()