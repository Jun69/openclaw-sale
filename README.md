# 销售 SOP 智能提取 — Skill 使用说明

## 概述

本 Skill 从销售对话语料（Excel 文件）中自动提取结构化 SOP JSON，支持 5 个租户：

| 租户 | 行业 | 一级节点 | 二级节点 | 三级节点 |
|------|------|---------|---------|---------|
| tenant_A | 酒水私域 | 15 | 26 | 127 |
| tenant_B | 考公培训 | 8 | 14 | 55 |
| tenant_C | 美妆护肤 | 7 | 12 | 51 |
| tenant_D | 美妆售后 | 7 | 10 | 32 |
| tenant_E | 会计培训 | 7 | 11 | 39 |

## 环境要求

- Python 3.9+
- openpyxl

```bash
pip install openpyxl
```

## 快速使用

### 生成全部租户 SOP

```bash
cd openclaw-sales-sop-master
python3 skill/generate_sop.py --data-dir competition/competition_data --output-dir output
```

### 生成单个租户 SOP

```bash
python3 skill/generate_sop.py --data-dir competition/competition_data --output-dir output --tenant tenant_A
```

### 验证输出

```bash
python3 -c "import json; [json.load(open(f'output/tenant_{t}_sop.json')) for t in 'ABCDE']; print('OK')"
```

## 参数说明

| 参数 | 必填 | 说明 |
|------|------|------|
| `--data-dir` | 是 | 语料数据目录（含 tenant_X/corpus/） |
| `--output-dir` | 是 | SOP JSON 输出目录 |
| `--tenant` | 否 | 仅处理指定租户 |
| `--max-files` | 否 | 每租户最多处理的语料文件数 |
| `--enable-llm-refine` | 否 | 启用 LLM 优化（可选） |

## 在 OpenClaw 平台使用

1. 将 `skill/` 目录安装到 OpenClaw：
   - 复制到 `~/.openclaw/skills/sales-sop-generator/`
   - 或工作空间 `skills/` 目录下

2. 在对话中调用：
```
请为所有租户生成 SOP，语料目录：/path/to/competition_data，输出到 /path/to/output
```

## 项目结构

```
openclaw-sales-sop-master/
├── skill/                          # Skill 包
│   ├── SKILL.md                    # OpenClaw skill 描述文件
│   ├── generate_sop.py             # 入口脚本
│   ├── README.md                   # Skill 详细文档
│   └── src/sop_generator/          # 核心模块
│       ├── cli.py                  # CLI 参数解析
│       ├── corpus.py               # Excel 对话读取
│       ├── generator.py            # 主编排逻辑
│       ├── heuristics.py           # 语料增强（补充话术模板）
│       ├── llm.py                  # LLM 客户端（可选）
│       ├── profiles.py             # 5 租户预置 SOP 结构
│       └── schema.py               # 结构定义
├── output/                         # 生成的 SOP JSON
│   ├── tenant_A_sop.json
│   ├── tenant_B_sop.json
│   ├── tenant_C_sop.json
│   ├── tenant_D_sop.json
│   └── tenant_E_sop.json
├── competition/competition_data/   # 语料数据
│   ├── tenant_A/                   # 含 example_sop.json + corpus/
│   ├── tenant_B/                   # corpus/
│   ├── tenant_C/                   # corpus/
│   ├── tenant_D/                   # corpus/
│   └── tenant_E/                   # corpus/
├── report.md                       # 技术报告
└── README.md                       # 本文件
```
