// 收到视频后，将相应的空字符串替换为文件路径，例如：
// cup: "assets/videos/cup.mp4"
// 支持同目录中的本地 MP4/WebM 文件或直接指向视频文件的 HTTPS 链接。
// 空字符串会保留论文静态帧和 “Video coming soon” 提示。
window.PILOT_CONFIG = {
  codeUrl: "",
  arxivUrl: "",
  videos: {
    "cup": "",
    "pencil-case": "",
    "bowl-box": "",
    "bowl-bowl": ""
  }
};
