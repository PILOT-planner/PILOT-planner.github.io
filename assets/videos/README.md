将四个真实机器人视频放在此目录，建议命名：

- cup.mp4
- pencil-case.mp4
- bowl-box.mp4
- bowl-bowl.mp4

然后在 `../media.js` 的对应任务中填写路径，例如 `"cup": "assets/videos/cup.mp4"`。

视频可使用 MP4（H.264）或 WebM。页面使用原生播放器；未配置视频的任务继续显示论文静态帧和占位提示。填写的视频路径出错时，页面会恢复静态帧。
