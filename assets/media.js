// 四个真实机器人任务的 PILOT 视频，已压缩并以 4 倍速编码。
// 支持同目录中的本地 MP4/WebM 文件或直接指向视频文件的 HTTPS 链接。
// 更换视频时，也更新 index.html 中的默认路径，供无 JavaScript 时播放。
window.PILOT_CONFIG = {
  codeUrl: "",
  arxivUrl: "",
  videos: {
    "cup": "assets/videos/cup.mp4",
    "pencil-case": "assets/videos/pencil-case.mp4",
    "bowl-box": "assets/videos/bowl-box.mp4",
    "bowl-bowl": "assets/videos/bowl-bowl.mp4"
  }
};
