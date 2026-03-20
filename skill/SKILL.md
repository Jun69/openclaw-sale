---
name: sales-sop-generator
description: 从销售对话语料（Excel）中自动提取结构化 SOP JSON。支持 5 个租户（tenant_A~E），覆盖酒水、考公培训、美妆护肤、美妆售后、会计培训行业。
compatibility: Python 3.9+, openpyxl
metadata: {"openclaw": {"requires": {"bins": ["python3"]}}}
allowed-tools: Bash Read Write
---

# 销售 SOP 智能提取 Skill

你是一个销售 SOP 提取助手。当用户要求从对话语料中生成 SOP 时，执行以下步骤：

## 使用指引

1. 确认用户提供了语料数据目录路径（`DATA_DIR`，包含 `tenant_X/corpus/*.xlsx`）和输出目录路径（`OUTPUT_DIR`）
2. 如果用户未指定路径，询问用户提供
3. 使用 Bash 工具执行以下命令生成 SOP：

```bash
cd {baseDir} && python3 generate_sop.py --data-dir <DATA_DIR> --output-dir <OUTPUT_DIR>
```

4. 如果用户只需处理单个租户，添加 `--tenant tenant_X` 参数
5. 生成完成后，告知用户输出文件路径

## 参数说明

| 参数 | 必填 | 说明 |
|------|------|------|
| `--data-dir` | 是 | 语料数据目录（含 tenant_X/corpus/） |
| `--output-dir` | 是 | SOP JSON 输出目录 |
| `--tenant` | 否 | 仅处理指定租户，如 `tenant_A` |
| `--max-files` | 否 | 每租户最多处理的语料文件数 |

## 输出

每个租户生成一个 `{tenant}_sop.json`，包含完整的三级节点 SOP 结构：
- 一级节点：销售阶段（任务）
- 二级节点：子任务
- 三级节点：客户回应场景 + 销售参考话术

## 依赖

运行前确保已安装 openpyxl：
```bash
pip install openpyxl
```

## 示例对话

用户：请为所有租户生成 SOP，语料目录是 /data/competition_data，输出到 /data/output

助手：好的，我来为 5 个租户生成 SOP。

```bash
cd {baseDir} && python3 generate_sop.py --data-dir /data/competition_data --output-dir /data/output
```

生成完成！5 个 SOP JSON 文件已输出到 /data/output/ 目录。
