# 电商用户行为数仓建设项目
基于 MySQL 8.0 + Python 实现的企业级电商数仓项目，包含完整 ETL 流程、数据可视化、AI 智能分析、数据质量监控，支持 Linux 自动化运行与 Git 规范化协作，可直接用于春招简历与作品集。

---

## 📌 项目架构（标准数仓分层）
- **ODS 层**：原始数据层，存储用户、订单原始数据
- **DWD 层**：明细数据层，清洗、过滤无效数据
- **DWS 层**：汇总数据层，按用户+日期聚合订单指标
- **ADS 层**：应用数据层，生成每日GMV、订单量、用户消费等业务报表

---

## 🛠 技术栈
- 数据库：MySQL 8.0
- 开发语言：Python 3.x
- 数据处理：pymysql
- 数据可视化：Pyecharts
- AI 能力：火山引擎·豆包大模型 API（自然语言转 SQL）
- 运维：Linux Shell、crontab 定时任务、数据质量监控
- 协作：Git Workflow 规范

---

## 🚀 核心功能
1.  **自动化造数**：支持每日增量生成订单数据，彻底解决主键冲突
2.  **数仓 ETL**：全流程自动化数据清洗、聚合、指标计算，一键刷新全链路
3.  **数据可视化**：生成交互式网页图表（GMV 趋势、订单量分析）
4.  **AI 智能分析**：接入豆包大模型，自然语言转 SQL，自动分析业务数据
5.  **企业级监控**：全链路数据质量检查 + 异常自动预警
6.  **Linux 自动化**：Shell 一键启动脚本 + crontab 定时调度
7.  **Git 规范化**：标准工作流 + 提交规范，工程化项目管理

---

## 🖥️ 运行方式
### Windows
```bash
# 一键运行所有脚本
python run_all.py

# 赋予执行权限
chmod +x run.sh

# 一键启动
sh run.sh

## Linux
```bash

# 赋予执行权限
chmod +x run.sh

# 一键启动
sh run.sh

---

## ⏰ Linux 定时任务
### 配置步骤
编辑定时任务：
bash
运行
crontab -e
在文件末尾添加（每天凌晨 2 点自动跑数仓）：
bash
运行
0 2 * * * cd /home/project/ecom_warehouse && sh run.sh
保存退出，定时任务自动生效
查看定时任务：
bash
运行
crontab -l
查看定时任务日志：
bash
运行
tail -f /var/log/cron
📌 Git Workflow 协作规范
分支规范
main：生产环境稳定分支
feature：功能开发分支
fix：bug 修复分支
提交规范
bash
运行
git add .
git commit -m "feat: 新增XX功能"
git commit -m "fix: 修复XX问题"
git commit -m "docs: 更新项目文档"
git push origin main
