F101 执行计划已归档；F102 仍使用的共享设计保留原位。所有特性状态保持不变。

验证通过：git diff --check；所有 Markdown 相对链接目标存在。未提交、同步 Issue、推送或联网。

实际命令及输出：

```json
[
  {
    "command": [
      "git",
      "init"
    ],
    "exit_code": 0,
    "stdout": "Initialized empty Git repository in /private/tmp/harness-f006-none-iteration2/6/.git/\n",
    "stderr": ""
  },
  {
    "command": [
      "git",
      "add",
      "."
    ],
    "exit_code": 0,
    "stdout": "",
    "stderr": ""
  },
  {
    "command": [
      "rg",
      "-n",
      "docs/|\\]\\(",
      "."
    ],
    "exit_code": 0,
    "stdout": "./features.json:7:      \"spec\": \"docs/specs/shared.md\",\n./features.json:8:      \"technical_notes\": \"Plan: docs/plans/f101.md\"\n./features.json:13:      \"spec\": \"docs/specs/shared.md\"\n./docs/plans/f102.md:2:Read [design](../specs/shared.md).\n",
    "stderr": ""
  },
  {
    "command": "Python pathlib.mkdir(parents=True): docs/archive/plans",
    "exit_code": 0,
    "stdout": "",
    "stderr": ""
  },
  {
    "command": [
      "git",
      "mv",
      "docs/plans/f101.md",
      "docs/archive/plans/f101.md"
    ],
    "exit_code": 0,
    "stdout": "",
    "stderr": ""
  },
  {
    "command": "Python pathlib.write_text: features.json",
    "exit_code": 0,
    "stdout": "",
    "stderr": ""
  },
  {
    "command": [
      "git",
      "diff",
      "--check"
    ],
    "exit_code": 0,
    "stdout": "",
    "stderr": ""
  },
  {
    "command": "Python: verify all relative Markdown link targets exist",
    "exit_code": 0,
    "stdout": "",
    "stderr": ""
  },
  {
    "command": [
      "git",
      "status",
      "--short"
    ],
    "exit_code": 0,
    "stdout": "A  CLAUDE.md\nA  docs/architecture.md\nA  docs/archive/plans/f101.md\nA  docs/plans/f102.md\nA  docs/specs/shared.md\nAM features.json\n",
    "stderr": ""
  }
]
```

不确定性：归档目录约定未指定，采用 docs/archive/。

Token/cost: unknown.
