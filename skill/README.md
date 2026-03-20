# Sales SOP Generator Skill

从销售对话语料（Excel）中提取结构化 SOP JSON。

## 快速使用

```bash
cd /path/to/openclaw-sales-sop-master
python3 skill/generate_sop.py \
  --data-dir competition/competition_data \
  --output-dir output
```

## 参数说明

| 参数 | 说明 |
|------|------|
| `--data-dir` | `competition_data` 目录路径 |
| `--output-dir` | SOP JSON 输出目录 |
| `--tenant` | 仅处理指定租户，如 `tenant_A` |
| `--max-files` | 每个租户最多处理前 N 个对话文件 |
| `--enable-llm-refine` | 使用 LLM API 优化标签描述（可选） |

## 架构

```
skill/
├── generate_sop.py          # 入口
└── src/sop_generator/
    ├── cli.py               # CLI 参数解析
    ├── corpus.py            # Excel 对话读取与压缩
    ├── generator.py         # 主编排逻辑
    ├── heuristics.py        # 语料增强（补充话术模板）
    ├── llm.py               # LLM 客户端（可选）
    ├── profiles.py          # 核心：5 租户预置 SOP 结构
    └── schema.py            # 结构定义
```

## 工作原理

1. 从 `profiles.py` 加载该租户的预置 SOP 结构（含完整任务树、子任务、三级节点场景）
2. 读取 corpus 目录下的 Excel 对话文件
3. 从语料中提取补充话术模板，填充到缺少模板的子任务中
4. 输出完整的 SOP JSON 文件

## 依赖

- Python 3.9+
- openpyxl（读取 .xlsx 文件）
