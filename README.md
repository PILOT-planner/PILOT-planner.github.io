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
- 四个 UR5e 任务的真实机器人演示视频、视频封面和子目标/执行对比
- 真实机器人结果、逐任务成功数、95% Wilson 置信区间、机器人设置
- 规划效率图、支持标签切换的 Push-T 和 LIBERO-10 完整结果
- 可复制 BibTeX、可放大的论文插图
- 手机/平板布局、键盘可操作导航和图片弹窗、无 JavaScript 基础阅读

内容采用居中且有最大宽度的布局：桌面主体宽度为屏幕的 84%，上限 1200px；论文标题上限 1120px，摘要、引用和关键指标区上限 1000px。1440px 屏幕上主体约占 83%，1920px 屏幕上约占 63%，更宽的显示器上内容不会继续拉长。平板两侧各留 24px，手机各留 20px。桌面正文随屏幕从 22px 增大到 28px，图注 21–26px、结果表格 21px；手机正文和图注 20px、表格 19px。排版参考 DreamSteer：连贯的论文标题、轻柔渐变标题区、深色资源按钮、首张示意图下方的三项核心贡献卡片、单栏摘要与连续的论文内容。真实机器人任务在桌面以四张视频卡片横排展示，平板使用两列、手机使用单列。真实机器人结果上方采用成功率条形图与实验设置图文的两列布局；较小屏幕恢复单列。Push-T 与 LIBERO-10 采用标签切换，支持鼠标和方向键操作；无 JavaScript 时两组结果都直接展示。手机指标纵向排列，图表在较窄屏幕上切换为单列。宽幅子目标对比图支持手机横向滑动，图片弹窗提供全分辨率原图链接。左上角图标及 favicon 使用用户提供的 PNG 原图。

## 视频和资源链接

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

四个演示视频已放入 `assets/videos/`，来源为用户提供压缩包中各任务的 `Ours.mp4` / `bowlBox_ours.mp4`。完整保留动作过程，以 4 倍速、960px 宽、30fps、H.264 编码并移除音轨，使用 faststart 支持边下载边播放。单个文件约 0.4–1.0MB，四个合计约 2.6MB。封面取自真实视频帧。具体来源和压缩参数见 [assets/videos/README.md](assets/videos/README.md)。

每个视频右上角显示 `×4` 速度标记。播放器带控制栏并支持手机内联播放；点击 `Enlarge` 在页面内打开最大 960px 的播放器弹窗，不进入全屏。弹窗同样显示速度标记，保留播放进度；支持关闭按钮、Esc 和点击背景关闭，关闭后返回原播放器。启用 JavaScript 时，播放一个任务会暂停其他任务，加载失败会退回视频封面。无 JavaScript 时原生播放器仍可使用。更换视频时同步更新 `assets/media.js` 和 `index.html` 中的路径及播放速度说明。也支持直接指向视频文件的 HTTPS URL；网页链接（例如 YouTube 播放页面）需要单独集成嵌入播放器。

稿件目前使用 Anonymous 署名，所以没有添加未经确认的作者、单位、会议录用信息、arXiv 编号或正式发表年份。公开时可在 `index.html` 中更新 `.authors` 和 `#bibtex`。

## 文件说明

- `index.html`：网页内容和所有实验数值
- `assets/style.css`：排版、响应式布局
- `assets/fonts/`：本地 Noto Sans 开源字体与 OFL 许可证，无需访问外部字体服务
- `assets/main.js`：视频接入、图片放大、引用复制
- `assets/media.js`：视频/代码/arXiv 配置
- `assets/videos/`：网页用 MP4 演示视频、真实视频封面与素材来源说明
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

真实机器人统计、Push-T 与 LIBERO 数值均来自所提供稿件。
