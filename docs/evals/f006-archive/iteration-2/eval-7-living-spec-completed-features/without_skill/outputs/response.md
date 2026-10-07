共享 API 设计已归档一次；两条特性引用、源码契约注释和用户指南链接均已更新。特性状态和运行行为保持不变。

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
    "stdout": "Initialized empty Git repository in /private/tmp/harness-f006-none-iteration2/7/.git/\n",
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
    "stdout": "./src/api.py:1:# Contract: docs/specs/api.md\n./docs/guide.md:2:See [API contract](specs/api.md).\n./features.json:7:      \"spec\": \"docs/specs/api.md\"\n./features.json:12:      \"spec\": \"docs/specs/api.md\"\n",
    "stderr": ""
  },
  {
    "command": "Python pathlib.mkdir(parents=True): docs/archive/specs",
    "exit_code": 0,
    "stdout": "",
    "stderr": ""
  },
  {
    "command": [
      "git",
      "mv",
      "docs/specs/api.md",
      "docs/archive/specs/api.md"
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
    "command": "Python pathlib.write_text: src/api.py",
    "exit_code": 0,
    "stdout": "",
    "stderr": ""
  },
  {
    "command": "Python pathlib.write_text: docs/guide.md",
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
    "stdout": "A  CLAUDE.md\nA  docs/architecture.md\nA  docs/archive/specs/api.md\nAM docs/guide.md\nAM features.json\nAM src/api.py\n",
    "stderr": ""
  }
]
```

不确定性：API contract remains referenced by live source and user guide. Interpreted explicit archive request as relocating it while repairing all references; future contract updates may still be necessary.

Token/cost: unknown.
