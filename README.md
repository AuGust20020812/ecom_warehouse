# 电商用户行为数仓建设项目
基于 MySQL 8.0 + Python 实现的企业级电商数仓项目，包含完整 ETL 流程、数据可视化、AI 智能分析、数据质量监控，支持 Linux 自动化运行与 Git 规范化协作。

---

## 📌 项目架构（标准数仓分层）
- **ODS 层**：原始数据层
- **DWD 层**：明细数据层
- **DWS 层**：汇总数据层
- **ADS 层**：应用数据层

---

## 🛠 技术栈
- 数据库：MySQL 8.0
- 开发语言：Python 3.x
- 可视化：Pyecharts
- AI 能力：火山引擎·豆包大模型
- 运维：Linux Shell、定时任务、数据监控
- 协作：Git Workflow 规范

---

## 🚀 核心功能
1. **自动化 ETL**：全链路数据清洗、聚合、计算
2. **交互式可视化**：GMV 趋势、订单量分析
3. **AI 智能分析**：自然语言转 SQL，自动查询数据
4. **企业级监控**：全链路数据质量检查 + 异常预警
5. **Linux 自动化**：Shell 脚本 + 定时调度
6. **Git 规范化**：标准工作流 + 提交规范

---

## 🖥️ 运行方式

### Windows
```bash
python run_all.py


## Linux（企业标准）s
# 赋予执行权限
chmod +x run.sh

# 一键启动
sh run.sh


### ⏰ Linux 定时任务配置步骤
1.  编辑定时任务：
    ```bash
    crontab -e



    0 2 * * * cd /home/project/ecom_warehouse && sh run.sh

    ## 📌 Git Workflow 协作规范
### 分支规范
- `main`：生产稳定分支
- `feature`：功能开发分支
- `fix`：BUG 修复分支

### 提交规范
```bash
git add .
git commit -m "feat: 新增XX功能"
git commit -m "fix: 修复XX问题"
git commit -m "docs: 更新文档"
git push origin main