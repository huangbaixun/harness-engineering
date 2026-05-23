// 90-min Harness Engineering 培训 PPT 构建脚本
// 输出：output.pptx，19 页，16:9，中文，深蓝 + 古铜 + 米色配色

const pptxgen = require("pptxgenjs");

const pres = new pptxgen();
pres.layout = "LAYOUT_16x9";  // 10" × 5.625"
pres.author = "Harness Engineering";
pres.title = "Harness Engineering 入门 — 90 分钟";

// ========== 配色与字体 ==========
const NAVY = "1E2A38";       // 深蓝（主导）
const BRONZE = "C8A65A";     // 古铜（accent，"harness/缰绳"色）
const CREAM = "F4EFE6";      // 米色（内容页底色）
const WHITE = "FFFFFF";
const INK = "1A1F2C";        // 深墨色（正文）
const GRAY = "6B7280";       // 中灰（辅文）
const LIGHT = "E5E7EB";      // 浅灰（边框）
const DANGER = "C03A2B";     // 警示红
const SUCCESS = "0E7C4F";    // 成功绿
const SOFTBRONZE = "EAD7A8"; // 古铜浅色（card 底）

const FONT_HEADER = "Microsoft YaHei";  // 跨 Mac/Windows 中文字体
const FONT_BODY = "Microsoft YaHei";

// ========== 通用辅助 ==========

// 内容页底色 + 顶部细古铜横条（视觉 motif）
function lightBg(slide) {
  slide.background = { color: CREAM };
  // 顶部古铜横条（占满宽，h=0.06）
  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0, y: 0, w: 10, h: 0.06,
    fill: { color: BRONZE }, line: { color: BRONZE }
  });
}

// 深色页（封面 / 节标题 / 致谢）
function darkBg(slide) {
  slide.background = { color: NAVY };
  // 古铜竖条 motif，左侧
  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0, y: 0, w: 0.12, h: 5.625,
    fill: { color: BRONZE }, line: { color: BRONZE }
  });
}

// 页眉小字（左上）
function pageEyebrow(slide, text) {
  slide.addText(text, {
    x: 0.5, y: 0.18, w: 9, h: 0.3,
    fontFace: FONT_BODY, fontSize: 11, color: GRAY,
    bold: false, charSpacing: 4, margin: 0
  });
}

// 大标题（深色文字）
function pageTitle(slide, text, y = 0.55) {
  slide.addText(text, {
    x: 0.5, y: y, w: 9, h: 0.7,
    fontFace: FONT_HEADER, fontSize: 30, color: INK,
    bold: true, margin: 0
  });
}

// 副标题
function pageSubtitle(slide, text, y = 1.2) {
  slide.addText(text, {
    x: 0.5, y: y, w: 9, h: 0.4,
    fontFace: FONT_BODY, fontSize: 14, color: GRAY,
    italic: true, margin: 0
  });
}

// 页脚标号
function pageFooter(slide, num, total = 19, sectionLabel = "") {
  slide.addText(`${num} / ${total}`, {
    x: 9.0, y: 5.30, w: 0.9, h: 0.2,
    fontFace: FONT_BODY, fontSize: 9, color: GRAY,
    align: "right", margin: 0
  });
  if (sectionLabel) {
    slide.addText(sectionLabel, {
      x: 0.5, y: 5.30, w: 5, h: 0.2,
      fontFace: FONT_BODY, fontSize: 9, color: GRAY,
      align: "left", margin: 0
    });
  }
}

// 圆形带数字（角色编号 / 步骤编号）
function numberCircle(slide, x, y, num, color = BRONZE) {
  slide.addShape(pres.shapes.OVAL, {
    x: x, y: y, w: 0.5, h: 0.5,
    fill: { color: color }, line: { color: color }
  });
  slide.addText(String(num), {
    x: x, y: y, w: 0.5, h: 0.5,
    fontFace: FONT_HEADER, fontSize: 18, color: WHITE,
    bold: true, align: "center", valign: "middle", margin: 0
  });
}

// 圆角卡片（米色页用）
function card(slide, x, y, w, h, fillColor = WHITE) {
  slide.addShape(pres.shapes.RECTANGLE, {
    x: x, y: y, w: w, h: h,
    fill: { color: fillColor }, line: { color: LIGHT, width: 0.75 },
    shadow: { type: "outer", blur: 8, offset: 2, angle: 90, color: "000000", opacity: 0.06 }
  });
}

// =================================================================
// P1 — 封面
// =================================================================
{
  const slide = pres.addSlide();
  darkBg(slide);

  // 顶部 eyebrow（白色）
  slide.addText("DEPARTMENT TRAINING · 90 MINUTES", {
    x: 0.6, y: 0.6, w: 9, h: 0.3,
    fontFace: FONT_BODY, fontSize: 11, color: BRONZE,
    bold: true, charSpacing: 8, margin: 0
  });

  // 主标题（中文大字）
  slide.addText("Harness Engineering", {
    x: 0.6, y: 1.4, w: 9, h: 0.9,
    fontFace: FONT_HEADER, fontSize: 48, color: WHITE,
    bold: true, margin: 0
  });

  slide.addText("AI 编程时代的工程实践", {
    x: 0.6, y: 2.3, w: 9, h: 0.7,
    fontFace: FONT_HEADER, fontSize: 28, color: SOFTBRONZE,
    bold: false, margin: 0
  });

  // 装饰横线 + 副文
  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0.6, y: 3.2, w: 0.6, h: 0.04,
    fill: { color: BRONZE }, line: { color: BRONZE }
  });
  slide.addText("从 prompt → context → harness", {
    x: 0.6, y: 3.35, w: 9, h: 0.4,
    fontFace: FONT_BODY, fontSize: 16, color: WHITE,
    italic: true, margin: 0
  });
  slide.addText("一项让 AI 可以可靠工作的工程实践", {
    x: 0.6, y: 3.75, w: 9, h: 0.4,
    fontFace: FONT_BODY, fontSize: 14, color: SOFTBRONZE,
    margin: 0
  });

  // 底部讲师与日期
  slide.addText("simon · 2026", {
    x: 0.6, y: 4.85, w: 9, h: 0.3,
    fontFace: FONT_BODY, fontSize: 11, color: GRAY, margin: 0
  });
}

// =================================================================
// P2 — 三个调研举手
// =================================================================
{
  const slide = pres.addSlide();
  lightBg(slide);
  pageEyebrow(slide, "§A · 0:00–0:05 · 开场");
  pageTitle(slide, "三个问题，请举手");
  pageFooter(slide, 2, 19, "§A 开场");

  const questions = [
    "用过 ChatGPT 写过 / 改过自己工作中代码的，请举手",
    "用过 Claude Code、Cursor 这类 agentic 编程工具的，请举手",
    "曾经因为 AI 给了错代码，让你花了更多时间排查的，请举手",
  ];

  let y = 1.7;
  questions.forEach((q, i) => {
    numberCircle(slide, 0.8, y, i + 1);
    slide.addText(q, {
      x: 1.55, y: y, w: 7.8, h: 0.5,
      fontFace: FONT_BODY, fontSize: 16, color: INK,
      valign: "middle", margin: 0
    });
    y += 1.05;
  });

  // 底部画外音
  slide.addText("第三问通常举手最多 — 这就是今天要讲的", {
    x: 0.5, y: 4.95, w: 9, h: 0.3,
    fontFace: FONT_BODY, fontSize: 12, color: BRONZE,
    italic: true, align: "center", margin: 0
  });
}

// =================================================================
// P3 — 三阶段演进时间轴
// =================================================================
{
  const slide = pres.addSlide();
  lightBg(slide);
  pageEyebrow(slide, "§B · 0:05–0:08 · 背景");
  pageTitle(slide, "三阶段演进 · 三年跳了三次");
  pageFooter(slide, 3, 19, "§B 背景");

  // 时间轴底线
  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0.7, y: 3.2, w: 8.6, h: 0.02,
    fill: { color: BRONZE }, line: { color: BRONZE }
  });

  const stages = [
    { x: 0.7, year: "2022 — 2024", title: "Prompt", subtitle: "Engineering", desc: "把 prompt 写好\n模型就输出对的", tone: GRAY },
    { x: 3.85, year: "2025", title: "Context", subtitle: "Engineering", desc: "给模型喂对的上下文\nRAG / 工具 / 长 context", tone: GRAY },
    { x: 7.0, year: "2026 起", title: "Harness", subtitle: "Engineering", desc: "搭建让 AI 可靠工作的环境\n约束 + 反馈 + 验证", tone: BRONZE, highlight: true },
  ];

  stages.forEach(s => {
    // 时间标签（线上方）
    slide.addText(s.year, {
      x: s.x, y: 1.6, w: 2.5, h: 0.3,
      fontFace: FONT_BODY, fontSize: 11, color: GRAY,
      bold: true, charSpacing: 3, margin: 0
    });

    // 大标题
    slide.addText(s.title, {
      x: s.x, y: 1.95, w: 2.5, h: 0.55,
      fontFace: FONT_HEADER, fontSize: 26, color: s.highlight ? BRONZE : INK,
      bold: true, margin: 0
    });
    slide.addText(s.subtitle, {
      x: s.x, y: 2.55, w: 2.5, h: 0.4,
      fontFace: FONT_HEADER, fontSize: 16, color: s.highlight ? BRONZE : GRAY,
      bold: false, margin: 0
    });

    // 时间轴节点圆
    slide.addShape(pres.shapes.OVAL, {
      x: s.x + 0.2, y: 3.07, w: 0.3, h: 0.3,
      fill: { color: s.highlight ? BRONZE : GRAY }, line: { color: s.highlight ? BRONZE : GRAY }
    });

    // 描述
    slide.addText(s.desc, {
      x: s.x, y: 3.5, w: 2.6, h: 1.0,
      fontFace: FONT_BODY, fontSize: 13, color: s.highlight ? INK : GRAY,
      margin: 0
    });
  });

  // 底部备注
  slide.addText("Harness ＝ 缰绳、马鞍、衔铁。引导骏马（模型）力量的方向。", {
    x: 0.5, y: 4.85, w: 9, h: 0.3,
    fontFace: FONT_BODY, fontSize: 12, color: BRONZE,
    italic: true, align: "center", margin: 0
  });
}

// =================================================================
// P4 — 骏马与缰绳隐喻
// =================================================================
{
  const slide = pres.addSlide();
  lightBg(slide);
  pageEyebrow(slide, "§B · 0:08–0:11 · 隐喻");
  pageTitle(slide, "你不是在训马，你是在装马具");
  pageFooter(slide, 4, 19, "§B 背景");

  // 左卡片：骏马
  card(slide, 0.5, 1.5, 4.3, 3.3);
  slide.addShape(pres.shapes.OVAL, {
    x: 2.4, y: 1.85, w: 0.6, h: 0.6,
    fill: { color: NAVY }, line: { color: NAVY }
  });
  slide.addText("M", {
    x: 2.4, y: 1.85, w: 0.6, h: 0.6,
    fontFace: FONT_HEADER, fontSize: 22, color: WHITE,
    bold: true, align: "center", valign: "middle", margin: 0
  });
  slide.addText("骏马", {
    x: 0.5, y: 2.6, w: 4.3, h: 0.5,
    fontFace: FONT_HEADER, fontSize: 24, color: INK,
    bold: true, align: "center", margin: 0
  });
  slide.addText("Model · 模型", {
    x: 0.5, y: 3.0, w: 4.3, h: 0.3,
    fontFace: FONT_BODY, fontSize: 12, color: GRAY,
    italic: true, align: "center", margin: 0
  });
  slide.addText([
    { text: "力量惊人", options: { bullet: true, breakLine: true } },
    { text: "已经被训练完成", options: { bullet: true, breakLine: true } },
    { text: "但不知道方向", options: { bullet: true } },
  ], {
    x: 1.0, y: 3.5, w: 3.3, h: 1.3,
    fontFace: FONT_BODY, fontSize: 14, color: INK, margin: 0
  });

  // 中间箭头
  slide.addShape(pres.shapes.RIGHT_TRIANGLE, {
    x: 4.95, y: 2.95, w: 0.4, h: 0.6,
    fill: { color: BRONZE }, line: { color: BRONZE },
    rotate: 0
  });

  // 右卡片：缰绳/Harness
  card(slide, 5.45, 1.5, 4.05, 3.3, SOFTBRONZE);
  slide.addShape(pres.shapes.OVAL, {
    x: 7.2, y: 1.85, w: 0.6, h: 0.6,
    fill: { color: BRONZE }, line: { color: BRONZE }
  });
  slide.addText("H", {
    x: 7.2, y: 1.85, w: 0.6, h: 0.6,
    fontFace: FONT_HEADER, fontSize: 22, color: WHITE,
    bold: true, align: "center", valign: "middle", margin: 0
  });
  slide.addText("缰绳与马鞍", {
    x: 5.45, y: 2.6, w: 4.05, h: 0.5,
    fontFace: FONT_HEADER, fontSize: 24, color: INK,
    bold: true, align: "center", margin: 0
  });
  slide.addText("Harness · 工程实践", {
    x: 5.45, y: 3.0, w: 4.05, h: 0.3,
    fontFace: FONT_BODY, fontSize: 12, color: INK,
    italic: true, align: "center", margin: 0
  });
  slide.addText([
    { text: "你能控制的工具", options: { bullet: true, breakLine: true } },
    { text: "持续迭代演进", options: { bullet: true, breakLine: true } },
    { text: "把方向交给环境", options: { bullet: true } },
  ], {
    x: 5.95, y: 3.5, w: 3.05, h: 1.3,
    fontFace: FONT_BODY, fontSize: 14, color: INK, margin: 0
  });

  // 底部留白即可
}

// =================================================================
// P5 — 失败剖面（4 round 故事）
// =================================================================
{
  const slide = pres.addSlide();
  lightBg(slide);
  pageEyebrow(slide, "§B · 0:11–0:14 · 真实故事");
  pageTitle(slide, "一次 AI 失败的真实剖面");
  pageSubtitle(slide, "任务：在 todo 应用里加一个删除按钮");
  pageFooter(slide, 5, 19, "§B 背景");

  const rounds = [
    { num: 1, action: "AI 加了删除按钮", mark: "✓", color: SUCCESS },
    { num: 2, action: "用户：'删除前要弹确认框'\nAI 加了确认框，但顺手把所有按钮颜色改成红色", mark: "✗", color: DANGER },
    { num: 3, action: "用户：'你为什么改颜色'\nAI 撤回颜色改动，但顺手删掉了之前的确认框", mark: "✗", color: DANGER },
    { num: 4, action: "用户已心累，决定自己写", mark: "—", color: GRAY },
  ];

  let y = 1.7;
  rounds.forEach(r => {
    // 圆形 round 编号
    slide.addShape(pres.shapes.OVAL, {
      x: 0.7, y: y, w: 0.5, h: 0.5,
      fill: { color: NAVY }, line: { color: NAVY }
    });
    slide.addText(`R${r.num}`, {
      x: 0.7, y: y, w: 0.5, h: 0.5,
      fontFace: FONT_HEADER, fontSize: 13, color: WHITE,
      bold: true, align: "center", valign: "middle", margin: 0
    });

    // 描述
    slide.addText(r.action, {
      x: 1.45, y: y - 0.05, w: 7.0, h: 0.7,
      fontFace: FONT_BODY, fontSize: 13, color: INK,
      valign: "middle", margin: 0
    });

    // 标记
    slide.addText(r.mark, {
      x: 8.6, y: y - 0.05, w: 0.6, h: 0.7,
      fontFace: FONT_HEADER, fontSize: 22, color: r.color,
      bold: true, align: "center", valign: "middle", margin: 0
    });

    y += 0.78;
  });

  // 底部金句
  slide.addText("AI 不是笨 — 它每一步都'自以为合理'。问题在环境里没有任何机械约束。", {
    x: 0.5, y: 4.95, w: 9, h: 0.3,
    fontFace: FONT_BODY, fontSize: 12, color: BRONZE,
    italic: true, align: "center", margin: 0
  });
}

// =================================================================
// P6 — 工程师工作重心的转变
// =================================================================
{
  const slide = pres.addSlide();
  lightBg(slide);
  pageEyebrow(slide, "§B · 0:14–0:18 · 转变");
  pageTitle(slide, "工程师工作的重心要变了");
  pageFooter(slide, 6, 19, "§B 背景");

  // 左：传统
  card(slide, 0.5, 1.5, 4.3, 3.3);
  slide.addText("传 统", {
    x: 0.5, y: 1.7, w: 4.3, h: 0.5,
    fontFace: FONT_HEADER, fontSize: 16, color: GRAY,
    bold: true, align: "center", charSpacing: 8, margin: 0
  });
  slide.addText("写代码", {
    x: 0.5, y: 2.4, w: 4.3, h: 0.8,
    fontFace: FONT_HEADER, fontSize: 36, color: GRAY,
    bold: true, align: "center", margin: 0
  });
  slide.addText([
    { text: "线性产出 1x 代码", options: { bullet: true, breakLine: true } },
    { text: "AI 失败 = 自己花时间排查", options: { bullet: true, breakLine: true } },
    { text: "经验难以复用", options: { bullet: true } },
  ], {
    x: 0.9, y: 3.4, w: 3.6, h: 1.3,
    fontFace: FONT_BODY, fontSize: 13, color: GRAY, margin: 0
  });

  // 右：Harness 时代
  card(slide, 5.2, 1.5, 4.3, 3.3, SOFTBRONZE);
  slide.addText("HARNESS 时代", {
    x: 5.2, y: 1.7, w: 4.3, h: 0.5,
    fontFace: FONT_HEADER, fontSize: 16, color: BRONZE,
    bold: true, align: "center", charSpacing: 8, margin: 0
  });
  slide.addText("设计环境", {
    x: 5.2, y: 2.4, w: 4.3, h: 0.8,
    fontFace: FONT_HEADER, fontSize: 36, color: INK,
    bold: true, align: "center", margin: 0
  });
  slide.addText([
    { text: "杠杆 3-5x，单工程师管更多", options: { bullet: true, breakLine: true } },
    { text: "AI 失败 = 免费的改进材料", options: { bullet: true, breakLine: true } },
    { text: "约束累积，越用越靠谱", options: { bullet: true } },
  ], {
    x: 5.6, y: 3.4, w: 3.6, h: 1.3,
    fontFace: FONT_BODY, fontSize: 13, color: INK, margin: 0
  });

  // 底部金句
  slide.addText("你不是被 AI 替代 — 你是变成 AI 团队的'马具工程师'。", {
    x: 0.5, y: 5.0, w: 9, h: 0.3,
    fontFace: FONT_BODY, fontSize: 12, color: BRONZE,
    italic: true, align: "center", margin: 0
  });
}

// =================================================================
// P7-P10 — 四角色痛点（共用模板）
// =================================================================
function rolePainSlide(num, role, painText, fixes, motifColor) {
  const slide = pres.addSlide();
  lightBg(slide);
  pageEyebrow(slide, `§C · 角色痛点 ${num - 6} / 4`);
  pageTitle(slide, `${role} · 没有 harness 的痛`);
  pageFooter(slide, num, 19, "§C 多角色痛点");

  // 角色徽章（向左移 0.4"，远离右边缘）
  slide.addShape(pres.shapes.OVAL, {
    x: 8.2, y: 0.55, w: 0.7, h: 0.7,
    fill: { color: motifColor }, line: { color: motifColor }
  });
  slide.addText(role.slice(0, 2), {
    x: 8.2, y: 0.55, w: 0.7, h: 0.7,
    fontFace: FONT_HEADER, fontSize: 15, color: WHITE,
    bold: true, align: "center", valign: "middle", margin: 0
  });

  // 痛点 card（高度从 1.6 减到 1.4，避免内部空旷）
  card(slide, 0.5, 1.5, 9.0, 1.4);
  // 左侧色条 motif（增强角色色彩识别）
  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0.5, y: 1.5, w: 0.08, h: 1.4,
    fill: { color: motifColor }, line: { color: motifColor }
  });
  slide.addText("痛 点", {
    x: 0.75, y: 1.6, w: 1.5, h: 0.3,
    fontFace: FONT_HEADER, fontSize: 11, color: motifColor,
    bold: true, charSpacing: 6, margin: 0
  });
  slide.addText(painText, {
    x: 0.75, y: 1.92, w: 8.55, h: 0.95,
    fontFace: FONT_BODY, fontSize: 14, color: INK,
    italic: true, valign: "top", margin: 0
  });

  // Harness 怎么治 card
  card(slide, 0.5, 3.1, 9.0, 1.9, SOFTBRONZE);
  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0.5, y: 3.1, w: 0.08, h: 1.9,
    fill: { color: BRONZE }, line: { color: BRONZE }
  });
  slide.addText("HARNESS 怎么治", {
    x: 0.75, y: 3.2, w: 4.0, h: 0.3,
    fontFace: FONT_HEADER, fontSize: 11, color: BRONZE,
    bold: true, charSpacing: 6, margin: 0
  });
  const fixItems = fixes.map((f, i) => ({
    text: f, options: { bullet: true, breakLine: i < fixes.length - 1 },
  }));
  slide.addText(fixItems, {
    x: 0.95, y: 3.55, w: 8.35, h: 1.35,
    fontFace: FONT_BODY, fontSize: 13, color: INK,
    paraSpaceAfter: 4, margin: 0
  });
}

rolePainSlide(7, "后端开发",
  "让 AI 加个 user 删除接口，它顺手把整个 user model 重构了，还引入了一个新依赖 redis。我只想加一个 endpoint。",
  [
    "features.json 的 out_of_scope 字段明确禁止重构和加依赖",
    "harness:plan 强制声明改动范围",
    "Stop Hook 检查 dependencies diff，发现新依赖直接 fail",
  ],
  "1F4E79"
);

rolePainSlide(8, "前端开发",
  "让 AI 加个 modal，它把全局 css 变量改了。整个 app 颜色都变了，回滚要找半小时。",
  [
    "PreToolUse Hook 拦截对全局样式文件的修改",
    "harness:plan 的 forbidden_patterns 声明禁止改 tokens.css",
    "/careful 模式包裹破坏性广播变更",
  ],
  "9B2226"
);

rolePainSlide(9, "QA 测试",
  "AI 改完代码说'已实现'，但去看根本没加测试。提它，说'下次补'，下次也没补。",
  [
    "harness:tdd 强制 Red-Green-Refactor，没测试不能进 Green",
    "Stop Hook 拒绝任何'代码改了但 test 文件没改'的 diff",
    "harness:audit 给项目打分，测试缺位会显示在七维度报告里",
  ],
  "0E7C4F"
);

rolePainSlide(10, "PM 产品",
  "三个月前为什么选 Kafka 不选 SQS？AI 当时给了分析。聊天记录早被冲掉了。现在团队讨论换型，没人记得当时的理由。",
  [
    "ADR（架构决策记录）作为活文档归档",
    "harness:archive 把 proposal / design / tasks 永久落盘",
    "三个月后任何人 grep 关键词都能找到当时的决策上下文",
  ],
  "5B3F8E"  // 深紫，与其他三角色（蓝/红/绿）形成第四种识别色，与古铜底色对比清晰
);

// =================================================================
// P11 — Demo 入场（深色节标题页）
// =================================================================
{
  const slide = pres.addSlide();
  darkBg(slide);

  slide.addText("§D · DEMO TIME", {
    x: 0.6, y: 0.6, w: 9, h: 0.3,
    fontFace: FONT_BODY, fontSize: 11, color: BRONZE,
    bold: true, charSpacing: 8, margin: 0
  });

  slide.addText("现场对比演示", {
    x: 0.6, y: 1.5, w: 9, h: 0.9,
    fontFace: FONT_HEADER, fontSize: 44, color: WHITE,
    bold: true, margin: 0
  });

  slide.addText("Mini 留言板加点赞功能", {
    x: 0.6, y: 2.5, w: 9, h: 0.6,
    fontFace: FONT_HEADER, fontSize: 22, color: SOFTBRONZE, margin: 0
  });

  // 三行对照
  const lines = [
    "同一个项目",
    "同一个 AI 模型",
    "同一个任务",
  ];
  lines.forEach((t, i) => {
    slide.addShape(pres.shapes.RECTANGLE, {
      x: 0.6, y: 3.5 + i * 0.4, w: 0.04, h: 0.3,
      fill: { color: BRONZE }, line: { color: BRONZE }
    });
    slide.addText(t, {
      x: 0.85, y: 3.5 + i * 0.4, w: 9, h: 0.3,
      fontFace: FONT_BODY, fontSize: 16, color: WHITE, margin: 0
    });
  });

  slide.addText("唯一的区别：装与不装 harness — 25 分钟", {
    x: 0.6, y: 5.0, w: 9, h: 0.3,
    fontFace: FONT_BODY, fontSize: 13, color: BRONZE,
    italic: true, margin: 0
  });
}

// =================================================================
// P12 — Demo 对比表
// =================================================================
{
  const slide = pres.addSlide();
  lightBg(slide);
  pageEyebrow(slide, "§D · 0:48–0:55 · Demo 对比");
  pageTitle(slide, "把刚才你看到的差距浓缩成一张表");
  pageFooter(slide, 12, 19, "§D Demo 对比");

  const rows = [
    ["维度", "Baseline", "Treatment"],
    ["文件改动数", "5 个", "2 个"],
    ["原测试通过", "2/3（坏 1 个）", "3/3 全绿"],
    ["新测试覆盖", "0 个", "2 个"],
    ["范围越界", "改了存储层", "无"],
    ["决策归档", "无", "proposal.md 落盘"],
    ["Hook 拦截次数", "0（没装）", "1（CSS 变量）"],
    ["commit 整洁度", "1 个超长 commit", "red / green / refactor"],
    ["预估 review 时长", "~60 min", "~10 min"],
    ["你信任这个 PR 吗", "不太敢", "敢"],
  ];

  // 用 addTable
  const tableData = rows.map((row, ri) =>
    row.map((cell, ci) => {
      const isHeader = ri === 0;
      const isFirstCol = ci === 0;
      const isBaseline = ci === 1 && !isHeader;
      const isTreatment = ci === 2 && !isHeader;
      return {
        text: cell,
        options: {
          fontFace: FONT_BODY,
          fontSize: isHeader ? 13 : 12,
          bold: isHeader || isFirstCol,
          color: isHeader ? WHITE : (isTreatment ? "0E7C4F" : (isBaseline ? "9B2226" : INK)),
          fill: { color: isHeader ? NAVY : (ri % 2 === 0 ? CREAM : WHITE) },
          align: ci === 0 ? "left" : "center",
          valign: "middle",
        },
      };
    })
  );

  slide.addTable(tableData, {
    x: 0.5, y: 1.4, w: 9.0,
    colW: [3.0, 3.0, 3.0],
    rowH: 0.34,
    border: { pt: 0.75, color: LIGHT },
  });

  slide.addText("Harness 不是给 AI 用的 — 是给整个团队用的。", {
    x: 0.5, y: 5.0, w: 9, h: 0.3,
    fontFace: FONT_BODY, fontSize: 12, color: BRONZE,
    italic: true, align: "center", margin: 0
  });
}

// =================================================================
// P13 — 三大核心原则
// =================================================================
{
  const slide = pres.addSlide();
  lightBg(slide);
  pageEyebrow(slide, "§E · 0:55–1:00 · 原则");
  pageTitle(slide, "Harness 的三大核心原则");
  pageFooter(slide, 13, 19, "§E 原则与模型");

  const principles = [
    {
      num: "1",
      title: "永远不要让创建者独立评审自己的产出",
      body: "写代码的 Agent 不应同时是评审代码的 Agent。\n生成与评估必须分离。",
    },
    {
      num: "2",
      title: "上下文重置优于无限压缩",
      body: "长任务里，定期清空并结构化交接，比让 context 越累越长有效。",
    },
    {
      num: "3",
      title: "约束赋能，而不是限制",
      body: "AI 越紧的边界，输出越靠谱 — 因为约束帮它做了决策。\n这条最反直觉。",
      highlight: true,
    },
  ];

  let y = 1.55;
  principles.forEach(p => {
    card(slide, 0.5, y, 9.0, 1.0, p.highlight ? SOFTBRONZE : WHITE);
    numberCircle(slide, 0.7, y + 0.2, p.num, p.highlight ? BRONZE : NAVY);
    slide.addText(p.title, {
      x: 1.5, y: y + 0.15, w: 7.8, h: 0.4,
      fontFace: FONT_HEADER, fontSize: 16, color: INK,
      bold: true, margin: 0
    });
    slide.addText(p.body, {
      x: 1.5, y: y + 0.5, w: 7.8, h: 0.55,
      fontFace: FONT_BODY, fontSize: 12, color: GRAY, margin: 0
    });
    y += 1.13;
  });
}

// =================================================================
// P14 — 六层模型
// =================================================================
{
  const slide = pres.addSlide();
  lightBg(slide);
  pageEyebrow(slide, "§E · 1:00–1:05 · 六层");
  pageTitle(slide, "Harness 六层模型 · 强度从弱到强");
  pageFooter(slide, 14, 19, "§E 原则与模型");

  const layers = [
    { num: "①", name: "记忆层", what: "CLAUDE.md", why: "静态知识：架构约定、禁止规则、测试命令" },
    { num: "②", name: "规则层", what: "settings.json", why: "确定性行为：权限、模型、配置" },
    { num: "③", name: "技能层", what: "skills/ + commands/", why: "按需知识 + 显式工作流入口" },
    { num: "④", name: "智能体层", what: "agents/", why: "上下文隔离的专用 subagent" },
    { num: "⑤", name: "钩子层", what: "Pre/Post/Stop Hook", why: "确定性强制 — 模型绕不过", highlight: true },
    { num: "⑥", name: "工具层", what: "MCP servers", why: "能力扩展：外部服务接入" },
  ];

  let y = 1.5;
  const rowH = 0.55;
  layers.forEach((L, i) => {
    const fillC = L.highlight ? SOFTBRONZE : WHITE;
    card(slide, 0.5, y, 9.0, rowH - 0.05, fillC);
    // 左侧编号
    slide.addText(L.num, {
      x: 0.65, y: y + 0.05, w: 0.5, h: rowH - 0.15,
      fontFace: FONT_HEADER, fontSize: 22, color: L.highlight ? BRONZE : NAVY,
      bold: true, align: "center", valign: "middle", margin: 0
    });
    // 层名
    slide.addText(L.name, {
      x: 1.2, y: y + 0.05, w: 1.5, h: rowH - 0.15,
      fontFace: FONT_HEADER, fontSize: 14, color: INK,
      bold: true, valign: "middle", margin: 0
    });
    // what（用 body 字体，不用 Consolas — 中文环境下回退会让英文字距异常）
    slide.addText(L.what, {
      x: 2.7, y: y + 0.05, w: 2.5, h: rowH - 0.15,
      fontFace: FONT_BODY, fontSize: 11, color: GRAY,
      italic: true, valign: "middle", margin: 0
    });
    // why
    slide.addText(L.why, {
      x: 5.3, y: y + 0.05, w: 4.0, h: rowH - 0.15,
      fontFace: FONT_BODY, fontSize: 11, color: INK,
      valign: "middle", margin: 0
    });
    y += rowH;
  });

  // 底部贴士
  slide.addText("不要一上来六层全做 — 先 ① 记忆，再 ⑤ 钩子，其他按需补。", {
    x: 0.5, y: 5.0, w: 9, h: 0.3,
    fontFace: FONT_BODY, fontSize: 12, color: BRONZE,
    italic: true, align: "center", margin: 0
  });
}

// =================================================================
// P15 — 反馈循环
// =================================================================
{
  const slide = pres.addSlide();
  lightBg(slide);
  pageEyebrow(slide, "§E · 1:05–1:10 · 灵魂");
  pageTitle(slide, "Harness Engineering 的核心反馈循环");
  pageSubtitle(slide, "每个失败都不是事故 — 是免费的 harness 改进材料");
  pageFooter(slide, 15, 19, "§E 原则与模型");

  // 四步循环（横向连线）
  const steps = [
    { x: 0.6, y: 2.2, label: "Agent 失败", color: DANGER },
    { x: 2.95, y: 2.2, label: "识别缺失能力", color: NAVY },
    { x: 5.3, y: 2.2, label: "工程化修复", color: BRONZE },
    { x: 7.65, y: 2.2, label: "永不再发生", color: SUCCESS },
  ];

  // 连线（步骤之间）
  steps.forEach((s, i) => {
    if (i < steps.length - 1) {
      slide.addShape(pres.shapes.RECTANGLE, {
        x: s.x + 1.85, y: s.y + 0.8, w: 0.5, h: 0.04,
        fill: { color: BRONZE }, line: { color: BRONZE }
      });
    }
    // 用 RECTANGLE 而非 ROUNDED_RECTANGLE 以保证顶部色带能完全覆盖（pptxgenjs.md 提示）
    slide.addShape(pres.shapes.RECTANGLE, {
      x: s.x, y: s.y, w: 1.8, h: 1.6,
      fill: { color: WHITE }, line: { color: s.color, width: 1.5 }
    });
    // 顶部色带
    slide.addShape(pres.shapes.RECTANGLE, {
      x: s.x, y: s.y, w: 1.8, h: 0.18,
      fill: { color: s.color }, line: { color: s.color }
    });
    slide.addText(`${i + 1}`, {
      x: s.x, y: s.y + 0.25, w: 1.8, h: 0.4,
      fontFace: FONT_HEADER, fontSize: 22, color: s.color,
      bold: true, align: "center", margin: 0
    });
    slide.addText(s.label, {
      x: s.x, y: s.y + 0.7, w: 1.8, h: 0.8,
      fontFace: FONT_HEADER, fontSize: 13, color: INK,
      bold: true, align: "center", valign: "middle", margin: 0
    });
  });

  // 底部"四种修复方式"
  slide.addText("第 3 步'工程化修复'的四种方式：", {
    x: 0.5, y: 4.05, w: 9, h: 0.3,
    fontFace: FONT_BODY, fontSize: 13, color: INK, bold: true, margin: 0
  });
  const fixWays = [
    { x: 0.5, label: "写到 CLAUDE.md", num: "1" },
    { x: 2.85, label: "加 Hook 强制", num: "2" },
    { x: 5.2, label: "写 Skill 沉淀", num: "3" },
    { x: 7.55, label: "lint 自动校验", num: "4" },
  ];
  fixWays.forEach(f => {
    slide.addShape(pres.shapes.OVAL, {
      x: f.x, y: 4.45, w: 0.35, h: 0.35,
      fill: { color: BRONZE }, line: { color: BRONZE }
    });
    slide.addText(f.num, {
      x: f.x, y: 4.45, w: 0.35, h: 0.35,
      fontFace: FONT_HEADER, fontSize: 13, color: WHITE,
      bold: true, align: "center", valign: "middle", margin: 0
    });
    slide.addText(f.label, {
      x: f.x + 0.45, y: 4.45, w: 1.95, h: 0.4,
      fontFace: FONT_BODY, fontSize: 12, color: INK,
      valign: "middle", margin: 0
    });
  });

  slide.addText("项目用得越久，AI 在你这里失败率越低 — 因为环境一直在累积它撞过的墙。", {
    x: 0.5, y: 5.05, w: 9, h: 0.3,
    fontFace: FONT_BODY, fontSize: 12, color: BRONZE,
    italic: true, align: "center", margin: 0
  });
}

// =================================================================
// P16 — 工作纸（动手时间）
// =================================================================
{
  const slide = pres.addSlide();
  lightBg(slide);
  pageEyebrow(slide, "§F · 1:10–1:20 · 纸上动手");
  pageTitle(slide, "10 分钟：把今天讲的方法应用到自己");
  pageFooter(slide, 16, 19, "§F 动手");

  // 大题面
  card(slide, 0.5, 1.5, 9.0, 1.1, SOFTBRONZE);
  slide.addText("回想过去一个月，AI 让你失望或返工的一个具体场景。", {
    x: 0.7, y: 1.65, w: 8.6, h: 0.4,
    fontFace: FONT_HEADER, fontSize: 17, color: INK,
    bold: true, margin: 0
  });
  slide.addText("场景越具体越好 — 'AI 不靠谱'不算具体；'AI 把我 user model 重构了'才算。", {
    x: 0.7, y: 2.05, w: 8.6, h: 0.4,
    fontFace: FONT_BODY, fontSize: 12, color: GRAY,
    italic: true, margin: 0
  });

  // 三个子问题
  const subQs = [
    "1. 这次失败，AI 是缺了'上下文'还是缺了'约束'？",
    "2. 如果让你给这种失败设计一道护栏，放在六层里的哪一层？\n     ① 记忆 / ② 规则 / ③ 技能 / ④ 智能体 / ⑤ 钩子 / ⑥ 工具",
    "3. 这道护栏如果落地，每月给你省多少小时？",
  ];

  let y = 2.85;
  subQs.forEach(q => {
    slide.addText(q, {
      x: 0.7, y: y, w: 8.6, h: 0.6,
      fontFace: FONT_BODY, fontSize: 13, color: INK, margin: 0
    });
    y += 0.7;
  });

  // 操作说明
  slide.addText("5 分钟独立写 → 5 分钟 4 人小组讨论 → 2 组上台分享", {
    x: 0.5, y: 4.95, w: 9, h: 0.3,
    fontFace: FONT_BODY, fontSize: 12, color: BRONZE,
    italic: true, align: "center", margin: 0
  });
}

// =================================================================
// P17 — 落地路径
// =================================================================
{
  const slide = pres.addSlide();
  lightBg(slide);
  pageEyebrow(slide, "§G · 1:20–1:25 · 落地");
  pageTitle(slide, "怎么开始 · 从最小可用到完整体系");
  pageFooter(slide, 17, 19, "§G 落地与 Q&A");

  // 左：个人路径
  card(slide, 0.5, 1.45, 4.4, 3.5);
  slide.addText("个 人 路 径", {
    x: 0.5, y: 1.55, w: 4.4, h: 0.4,
    fontFace: FONT_HEADER, fontSize: 14, color: BRONZE,
    bold: true, charSpacing: 6, align: "center", margin: 0
  });

  const personalSteps = [
    { time: "本周", action: "给常用项目写一份 CLAUDE.md", note: "60 行内 · 30 分钟" },
    { time: "本月", action: "把今天工作纸里的失败做成一个 Hook", note: "针对最高频痛点" },
    { time: "本季度", action: "用 harness:audit 给项目做一次体检", note: "七维度健康度报告" },
  ];

  let py = 2.05;
  personalSteps.forEach((s, i) => {
    slide.addShape(pres.shapes.OVAL, {
      x: 0.7, y: py, w: 0.35, h: 0.35,
      fill: { color: BRONZE }, line: { color: BRONZE }
    });
    slide.addText(String(i + 1), {
      x: 0.7, y: py, w: 0.35, h: 0.35,
      fontFace: FONT_HEADER, fontSize: 11, color: WHITE,
      bold: true, align: "center", valign: "middle", margin: 0
    });
    slide.addText(s.time, {
      x: 1.15, y: py - 0.05, w: 1.0, h: 0.3,
      fontFace: FONT_HEADER, fontSize: 11, color: GRAY,
      bold: true, charSpacing: 4, margin: 0
    });
    slide.addText(s.action, {
      x: 1.15, y: py + 0.18, w: 3.6, h: 0.35,
      fontFace: FONT_BODY, fontSize: 12, color: INK,
      bold: true, margin: 0
    });
    slide.addText(s.note, {
      x: 1.15, y: py + 0.5, w: 3.6, h: 0.3,
      fontFace: FONT_BODY, fontSize: 10, color: GRAY,
      italic: true, margin: 0
    });
    py += 0.95;
  });

  // 右：团队路径
  card(slide, 5.1, 1.45, 4.4, 3.5, SOFTBRONZE);
  slide.addText("团 队 路 径", {
    x: 5.1, y: 1.55, w: 4.4, h: 0.4,
    fontFace: FONT_HEADER, fontSize: 14, color: BRONZE,
    bold: true, charSpacing: 6, align: "center", margin: 0
  });

  const teamSteps = [
    { time: "Week 1", action: "一份 CLAUDE.md（最小可用）" },
    { time: "Week 2-4", action: "加 1-2 个 Hook（最高频失败）" },
    { time: "Month 2-3", action: "引入 skills（plan / tdd / audit）" },
    { time: "Month 4+", action: "ADR、归档机制、多 agent 协作" },
  ];

  let ty = 2.05;
  teamSteps.forEach(s => {
    slide.addText(s.time, {
      x: 5.3, y: ty, w: 1.7, h: 0.3,
      fontFace: FONT_HEADER, fontSize: 11, color: BRONZE,
      bold: true, charSpacing: 4, margin: 0
    });
    slide.addText(s.action, {
      x: 5.3, y: ty + 0.25, w: 4.0, h: 0.35,
      fontFace: FONT_BODY, fontSize: 12, color: INK, margin: 0
    });
    ty += 0.7;
  });

  // 关键提醒
  slide.addText("不要一上来六层全做 — 先一层，看效果，再一层。", {
    x: 0.5, y: 5.05, w: 9, h: 0.3,
    fontFace: FONT_BODY, fontSize: 12, color: BRONZE,
    italic: true, align: "center", bold: true, margin: 0
  });
}

// =================================================================
// P18 — Q&A
// =================================================================
{
  const slide = pres.addSlide();
  darkBg(slide);

  slide.addText("§G · Q&A", {
    x: 0.6, y: 0.6, w: 9, h: 0.3,
    fontFace: FONT_BODY, fontSize: 11, color: BRONZE,
    bold: true, charSpacing: 8, margin: 0
  });

  slide.addText("Q & A", {
    x: 0.6, y: 1.6, w: 9, h: 1.5,
    fontFace: FONT_HEADER, fontSize: 96, color: WHITE,
    bold: true, charSpacing: 12, margin: 0
  });

  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0.6, y: 3.4, w: 0.6, h: 0.04,
    fill: { color: BRONZE }, line: { color: BRONZE }
  });

  // 三个引导问题
  const qs = [
    "我们用别的 IDE / 模型，这套还能用吗？",
    "学这一套要多长时间？",
    "AI 越来越强，未来还需要 harness 吗？",
  ];
  qs.forEach((q, i) => {
    slide.addText(q, {
      x: 0.6, y: 3.7 + i * 0.42, w: 9, h: 0.35,
      fontFace: FONT_BODY, fontSize: 14, color: SOFTBRONZE,
      italic: true, margin: 0
    });
  });
}

// =================================================================
// P19 — 致谢 + 离场问卷
// =================================================================
{
  const slide = pres.addSlide();
  darkBg(slide);

  slide.addText("THANK YOU", {
    x: 0.6, y: 0.6, w: 9, h: 0.3,
    fontFace: FONT_BODY, fontSize: 11, color: BRONZE,
    bold: true, charSpacing: 8, margin: 0
  });

  slide.addText("谢谢大家", {
    x: 0.6, y: 1.4, w: 9, h: 0.9,
    fontFace: FONT_HEADER, fontSize: 44, color: WHITE,
    bold: true, margin: 0
  });

  slide.addShape(pres.shapes.RECTANGLE, {
    x: 0.6, y: 2.5, w: 0.6, h: 0.04,
    fill: { color: BRONZE }, line: { color: BRONZE }
  });

  // 两个 next step
  const nexts = [
    { num: "1", title: "扫码做离场问卷", desc: "三道题 1 分钟 · 主要问你下周会动手的一件事" },
    { num: "2", title: "克隆 sample-board 自己跑一遍", desc: "比看视频效果好十倍 · 链接已发群" },
  ];

  let y = 2.85;
  nexts.forEach(n => {
    slide.addShape(pres.shapes.OVAL, {
      x: 0.6, y: y, w: 0.5, h: 0.5,
      fill: { color: BRONZE }, line: { color: BRONZE }
    });
    slide.addText(n.num, {
      x: 0.6, y: y, w: 0.5, h: 0.5,
      fontFace: FONT_HEADER, fontSize: 18, color: WHITE,
      bold: true, align: "center", valign: "middle", margin: 0
    });
    slide.addText(n.title, {
      x: 1.3, y: y - 0.05, w: 8, h: 0.4,
      fontFace: FONT_HEADER, fontSize: 18, color: WHITE,
      bold: true, margin: 0
    });
    slide.addText(n.desc, {
      x: 1.3, y: y + 0.32, w: 8, h: 0.3,
      fontFace: FONT_BODY, fontSize: 12, color: SOFTBRONZE, margin: 0
    });
    y += 0.95;
  });

  // 底部签名
  slide.addText("simon · 30 天后我会找问卷上写'会做'的同事 follow up", {
    x: 0.6, y: 5.05, w: 9, h: 0.3,
    fontFace: FONT_BODY, fontSize: 11, color: GRAY,
    italic: true, margin: 0
  });
}

// =================================================================
// 输出
// =================================================================
pres.writeFile({ fileName: "output.pptx" })
  .then(() => console.log("PPTX written: output.pptx"))
  .catch(err => { console.error(err); process.exit(1); });
