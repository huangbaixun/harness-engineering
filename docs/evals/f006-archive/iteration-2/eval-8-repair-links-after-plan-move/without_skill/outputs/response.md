F301 执行计划已归档；特性引用、历史记录链接及计划内架构链接已修复。frontmatter 和特性状态保持不变。

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
    "stdout": "Initialized empty Git repository in /private/tmp/harness-f006-none-iteration2/8/.git/\n",
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
    "stdout": "./docs/history.md:2:Completed implementation: [plan](plans/f301.md).\n./docs/plans/f301.md:5:Verified complete. See [architecture](../architecture.md).\n./features.json:7:      \"technical_notes\": \"Plan: docs/plans/f301.md\"\n",
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
      "docs/plans/f301.md",
      "docs/archive/plans/f301.md"
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
    "command": "Python pathlib.write_text: docs/history.md",
    "exit_code": 0,
    "stdout": "",
    "stderr": ""
  },
  {
    "command": "Python pathlib.write_text: docs/archive/plans/f301.md",
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
    "stdout": "A  CLAUDE.md\nA  docs/architecture.md\nAM docs/archive/plans/f301.md\nAM docs/history.md\nAM features.json\n",
    "stderr": ""
  }
]
```

不确定性：归档目录约定未指定，采用 docs/archive/。

Token/cost: unknown.
