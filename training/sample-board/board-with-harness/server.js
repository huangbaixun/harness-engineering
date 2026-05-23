// Mini 留言板 — with harness（业务代码与 baseline 完全一致）
// 唯一区别：这个分支额外有 CLAUDE.md / .claude/ / .harness/ 配置

const express = require('express');
const path = require('path');

const app = express();
app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));

let messages = [
  { id: 1, text: '欢迎来到留言板', author: 'admin', createdAt: Date.now() - 3600000 },
  { id: 2, text: '今天天气真不错', author: 'simon', createdAt: Date.now() - 1800000 },
];
let nextId = 3;

app.get('/api/messages', (req, res) => {
  res.json(messages);
});

app.post('/api/messages', (req, res) => {
  const { text, author } = req.body;
  if (!text || !author) {
    return res.status(400).json({ error: 'text 和 author 都不能为空' });
  }
  const message = { id: nextId++, text, author, createdAt: Date.now() };
  messages.push(message);
  res.status(201).json(message);
});

app.delete('/api/messages/:id', (req, res) => {
  const id = parseInt(req.params.id, 10);
  const idx = messages.findIndex(m => m.id === id);
  if (idx === -1) return res.status(404).json({ error: 'not found' });
  const removed = messages.splice(idx, 1)[0];
  res.json(removed);
});

module.exports = { app, _reset: () => { messages = []; nextId = 1; }, _seed: (data) => { messages = data; nextId = data.length + 1; } };

if (require.main === module) {
  const port = process.env.PORT || 3000;
  app.listen(port, () => console.log(`Board running at http://localhost:${port}`));
}
