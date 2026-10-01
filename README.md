# PILOT 论文项目网页

参考 [DreamSteer 项目网页](https://dream-steer.github.io/) 的学术项目页面结构，使用提供的 PDF 和 LaTeX 素材制作。页面为英文，纯 HTML/CSS/JavaScript，无需 Node.js、安装依赖或构建，可用于 GitHub Pages 等静态托管。

## 本地预览

在此目录运行：

```bash
python3 -m http.server 8000 --bind 127.0.0.1
```

浏览器打开 <http://localhost:8000>。也可以直接打开 `index.html`；使用本地 HTTP 服务可以获得更完整的剪贴板功能。

## 页面内容

- 论文标题、Anonymous 署名、论文 PDF 下载和关键结果
- 核心动机、完整摘要、方法架构和控制设置
- 四个 UR5e 任务的视频预留区域、论文静态帧和子目标/执行对比
- 真实机器人结果、逐任务成功数、95% Wilson 置信区间、训练数据条件
- 规划效率图、按顺序展开的 Push-T 和 LIBERO-10 完整结果
- 局限与后续研究、可复制 BibTeX、可放大的论文插图
- 手机/平板布局、键盘可操作导航和图片弹窗、无 JavaScript 基础阅读

内容采用居中且有最大宽度的布局：桌面主体宽度为屏幕的 84%，上限 1200px；论文标题上限 1120px，摘要、局限、引用和关键指标区上限 1000px。1440px 屏幕上主体约占 83%，1920px 屏幕上约占 63%，更宽的显示器上内容不会继续拉长。平板两侧各留 24px，手机各留 20px。桌面正文随屏幕从 22px 增大到 28px，图注 21–26px、结果表格 21px；手机正文和图注 20px、表格 19px。排版参考 DreamSteer：连贯的论文标题、轻柔渐变标题区、深色资源按钮、三项核心贡献卡片、单栏摘要与连续的论文内容。真实机器人任务在桌面采用两列展示，手机使用单列；仿真结果都直接展示。手机指标纵向排列，图表在较窄屏幕上切换为单列。宽幅子目标对比图支持手机横向滑动，图片弹窗提供全分辨率原图链接。左上角图标及 favicon 使用用户提供的 PNG 原图。

## 补充视频和链接

编辑 [assets/media.js](assets/media.js)：

```javascript
window.PILOT_CONFIG = {
  codeUrl: "",  // 代码仓库链接，留空时显示 Coming soon
  arxivUrl: "", // arXiv 链接，留空时不显示按钮
  videos: {
    "cup": "assets/videos/cup.mp4",
    "pencil-case": "assets/videos/pencil-case.mp4",
    "bowl-box": "assets/videos/bowl-box.mp4",
    "bowl-bowl": "assets/videos/bowl-bowl.mp4"
  }
};
```

视频文件放入 `assets/videos/`。也支持直接指向视频文件的 HTTPS URL；网页链接（例如 YouTube 播放页面）需要单独集成嵌入播放器。空值保留论文中的预测子目标静态帧。播放器带控制栏，播放一个任务时会暂停其他任务，路径加载失败会退回静态帧。

稿件目前使用 Anonymous 署名，所以没有添加未经确认的作者、单位、会议录用信息、arXiv 编号或正式发表年份。公开时可在 `index.html` 中更新 `.authors` 和 `#bibtex`。

## 文件说明

- `index.html`：网页内容和所有实验数值
- `assets/style.css`：排版、响应式布局
- `assets/fonts/`：本地 Noto Sans 开源字体与 OFL 许可证，无需访问外部字体服务
- `assets/main.js`：视频接入、图片放大、引用复制
- `assets/media.js`：后续视频/代码/arXiv 配置
- `assets/figures/`：由论文素材转换的 WebP 图片
- `assets/pilot-paper.pdf`：用户提供的 PDF 副本
- `paper-source/`：完整解压的 LaTeX 包，保留原始内容
- `scripts/check_site.py`：静态文件、内部链接、图像和实验数据检查
- `scripts/export_site.py`：导出仅包含网页资源的发布包

## 检查与发布包

```bash
python3 scripts/check_site.py
python3 scripts/export_site.py
```

第二条命令生成 `dist/` 和 `pilot-website.zip`，只含网页和网页必需素材，不包含原始 LaTeX 压缩包、LaTeX 源文件或生成日志。将 `dist/` 的内容上传至任意静态托管服务，或放到 GitHub Pages 的发布目录即可。所有资源使用相对路径，支持仓库子路径部署。

真实机器人统计、Push-T 与 LIBERO 数值均来自所提供稿件。40 条示范的匹配数据预算仅适用于真实机器人中 Wan 和 π₀ 的任务微调；页面同时注明世界模型的额外交互数据，以及仿真中不同的视频微调数据规模。
