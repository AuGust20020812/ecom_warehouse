import pymysql
from pyecharts import options as opts
from pyecharts.charts import Line, Bar
from pyecharts.globals import ThemeType

# ===================== 数据库连接 =====================
conn = pymysql.connect(
    host="localhost",
    user="root",
    password="root123456",
    database="ecom_dw",
    charset="utf8mb4"
)
cursor = conn.cursor()

print("📊 正在生成可视化图表...")

# ===================== 1. 读取ADS层数据 =====================
cursor.execute("""
    SELECT order_date, total_order_amount, total_order_cnt 
    FROM ads_order_daily_report 
    ORDER BY order_date DESC LIMIT 10
""")
data = cursor.fetchall()

dates = [str(item[0]) for item in data]
amounts = [float(item[1]) for item in data]
counts = [int(item[2]) for item in data]

# ===================== 2. 生成GMV趋势折线图 =====================
line_chart = (
    Line(init_opts=opts.InitOpts(theme=ThemeType.MACARONS))
    .add_xaxis(dates)
    .add_yaxis("每日GMV(元)", amounts, is_smooth=True, linestyle_opts=opts.LineStyleOpts(width=3))
    .set_global_opts(
        title_opts=opts.TitleOpts(title="电商数仓分析大屏", subtitle="每日GMV趋势分析"),
        xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-15)),
        tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross")
    )
)
line_chart.render("gmv_trend.html")
print("✅ GMV趋势图生成完成 -> gmv_trend.html")

# ===================== 3. 生成订单量柱状图 =====================
bar_chart = (
    Bar(init_opts=opts.InitOpts(theme=ThemeType.MACARONS))
    .add_xaxis(dates)
    .add_yaxis("订单数量", counts)
    .set_global_opts(
        title_opts=opts.TitleOpts(title="电商数仓分析大屏", subtitle="每日订单量分析"),
        xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-15))
    )
)
bar_chart.render("order_count.html")
print("✅ 订单量柱状图生成完成 -> order_count.html")

cursor.close()
conn.close()
print("\n🎉 可视化图表全部生成完成！")