(() => {
  "use strict";

  const config = window.PILOT_CONFIG || {};

  // Optional resources stay unavailable until a real URL is supplied.
  const validResource = (value) => {
    if (typeof value !== "string" || !value.trim()) return false;
    try {
      const url = new URL(value, window.location.href);
      return ["http:", "https:", "file:"].includes(url.protocol);
    } catch {
      return false;
    }
  };

  if (validResource(config.codeUrl)) {
    const codeLink = document.querySelector("[data-code-link]");
    codeLink.href = config.codeUrl;
    codeLink.target = "_blank";
    codeLink.rel = "noopener";
    codeLink.removeAttribute("aria-disabled");
    codeLink.classList.remove("is-disabled");
    document.querySelector("[data-code-status]").hidden = true;
  }
  if (validResource(config.arxivUrl)) {
    const arxivLink = document.querySelector("[data-arxiv-link]");
    arxivLink.href = config.arxivUrl;
    arxivLink.hidden = false;
  }

  const videoDialog = document.querySelector(".video-dialog");
  const enlargedVideo = videoDialog?.querySelector("video");
  let activeVideo;
  let videoOpener;
  let pendingVideoSync;
  let videoSynced = false;
  const pauseOtherVideos = (current) => {
    document.querySelectorAll(".task-media video, .video-dialog video").forEach((video) => {
      if (video !== current) video.pause();
    });
  };

  document.querySelectorAll("[data-video]").forEach((card) => {
    const src = config.videos?.[card.dataset.video];
    if (!validResource(src)) return;
    const media = card.querySelector(".task-media");
    const still = media.querySelector("img");
    const placeholder = media.querySelector(".video-placeholder");
    const enlargeButton = media.querySelector("[data-video-enlarge]");
    const speed = card.dataset.videoSpeed || "1";
    const video = media.querySelector("video") || document.createElement("video");
    video.controls = true;
    video.playsInline = true;
    video.preload = "metadata";
    video.poster = still.src;
    video.setAttribute("aria-label", `${card.querySelector("h3").textContent} robot demonstration, ${speed}× speed`);
    video.setAttribute("controlslist", "nofullscreen");
    if (video.src !== new URL(src, window.location.href).href) video.src = src;
    still.hidden = true;
    placeholder.hidden = true;
    if (video.parentElement !== media) media.append(video);
    video.addEventListener("play", () => pauseOtherVideos(video));
    if (enlargeButton && videoDialog && typeof videoDialog.showModal === "function") {
      enlargeButton.hidden = false;
      enlargeButton.addEventListener("click", () => {
        const wasPlaying = !video.paused && !video.ended;
        const position = video.currentTime;
        video.pause();
        enlargedVideo.pause();
        if (pendingVideoSync) enlargedVideo.removeEventListener("loadedmetadata", pendingVideoSync);
        activeVideo = video;
        videoOpener = enlargeButton;
        videoSynced = false;
        const title = `${card.querySelector("h3").textContent} demonstration`;
        videoDialog.querySelector("h3").textContent = title;
        enlargedVideo.setAttribute("aria-label", `${title}, ${speed}× speed`);
        enlargedVideo.poster = video.poster;
        enlargedVideo.src = video.currentSrc || video.src;
        enlargedVideo.playbackRate = video.playbackRate;
        enlargedVideo.muted = video.muted;
        enlargedVideo.volume = video.volume;
        const badge = videoDialog.querySelector(".video-speed");
        badge.textContent = `×${speed}`;
        badge.setAttribute("aria-label", `${speed} times speed`);
        badge.hidden = Number(speed) <= 1;
        pendingVideoSync = () => {
          if (!videoDialog.open || activeVideo !== video) return;
          enlargedVideo.currentTime = position;
          videoSynced = true;
          pendingVideoSync = undefined;
          if (wasPlaying) enlargedVideo.play().catch(() => {});
        };
        videoDialog.showModal();
        document.body.classList.add("dialog-open");
        if (enlargedVideo.readyState >= 1) pendingVideoSync();
        else enlargedVideo.addEventListener("loadedmetadata", pendingVideoSync, { once: true });
      });
    }
    video.addEventListener("error", () => {
      video.remove();
      still.hidden = false;
      placeholder.hidden = false;
      placeholder.querySelector("span").textContent = "Video unavailable";
      media.querySelector(".video-speed").hidden = true;
      if (enlargeButton) enlargeButton.hidden = true;
      if (activeVideo === video && videoDialog.open) videoDialog.close();
    }, { once: true });
  });

  if (videoDialog && typeof videoDialog.showModal === "function") {
    enlargedVideo.addEventListener("play", () => pauseOtherVideos(enlargedVideo));
    videoDialog.querySelector(".dialog-close").addEventListener("click", () => videoDialog.close());
    videoDialog.addEventListener("click", (event) => {
      const bounds = videoDialog.getBoundingClientRect();
      if (event.target === videoDialog && (event.clientX < bounds.left || event.clientX > bounds.right || event.clientY < bounds.top || event.clientY > bounds.bottom)) videoDialog.close();
    });
    videoDialog.addEventListener("close", () => {
      const wasPlaying = !enlargedVideo.paused && !enlargedVideo.ended;
      enlargedVideo.pause();
      if (pendingVideoSync) enlargedVideo.removeEventListener("loadedmetadata", pendingVideoSync);
      pendingVideoSync = undefined;
      if (activeVideo && !activeVideo.error && videoSynced) {
        activeVideo.currentTime = enlargedVideo.currentTime;
        activeVideo.playbackRate = enlargedVideo.playbackRate;
        if (wasPlaying) activeVideo.play().catch(() => {});
      }
      enlargedVideo.removeAttribute("src");
      enlargedVideo.load();
      activeVideo = undefined;
      videoSynced = false;
      document.body.classList.remove("dialog-open");
      videoOpener?.focus({ preventScroll: true });
    });
  }

  // Both benchmark sections remain readable when JavaScript is unavailable.
  document.querySelectorAll("[data-tabs]").forEach((group) => {
    const tablist = group.querySelector("[role='tablist']");
    const tabs = [...tablist.querySelectorAll("[role='tab']")];
    const panels = [...group.querySelectorAll("[data-panel]")];
    const select = (tab, focus = false) => {
      tabs.forEach((item) => {
        const selected = item === tab;
        item.setAttribute("aria-selected", String(selected));
        item.tabIndex = selected ? 0 : -1;
      });
      panels.forEach((panel) => { panel.hidden = panel.id !== tab.dataset.tab; });
      if (focus) tab.focus();
    };
    panels.forEach((panel) => {
      panel.setAttribute("role", "tabpanel");
      panel.setAttribute("aria-labelledby", tabs.find((tab) => tab.dataset.tab === panel.id).id);
      panel.tabIndex = 0;
    });
    tabs.forEach((tab, index) => {
      tab.addEventListener("click", () => select(tab));
      tab.addEventListener("keydown", (event) => {
        let next;
        if (event.key === "ArrowRight") next = (index + 1) % tabs.length;
        if (event.key === "ArrowLeft") next = (index - 1 + tabs.length) % tabs.length;
        if (event.key === "Home") next = 0;
        if (event.key === "End") next = tabs.length - 1;
        if (next !== undefined) {
          event.preventDefault();
          select(tabs[next], true);
        }
      });
    });
    group.classList.add("tabs-enhanced");
    tablist.hidden = false;
    select(tabs[0]);
  });

  const dialog = document.querySelector(".figure-dialog");
  if (dialog && typeof dialog.showModal === "function") {
    let opener;
    document.querySelectorAll("[data-lightbox]").forEach((link) => {
      link.addEventListener("click", (event) => {
        if (event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
        event.preventDefault();
        opener = link;
        const image = link.querySelector("img");
        const enlarged = dialog.querySelector(".dialog-image");
        enlarged.src = link.href;
        enlarged.alt = image.alt;
        dialog.querySelector(".dialog-original-link").href = link.href;
        const caption = link.closest("figure")?.querySelector("figcaption")?.cloneNode(true);
        caption?.querySelector(".figure-scroll-note")?.remove();
        dialog.querySelector(".dialog-caption").textContent = caption?.textContent.trim() || image.alt;
        dialog.showModal();
        document.body.classList.add("dialog-open");
      });
    });
    dialog.querySelector(".dialog-close").addEventListener("click", () => dialog.close());
    dialog.addEventListener("click", (event) => {
      const bounds = dialog.getBoundingClientRect();
      if (event.target === dialog && (event.clientX < bounds.left || event.clientX > bounds.right || event.clientY < bounds.top || event.clientY > bounds.bottom)) dialog.close();
    });
    dialog.addEventListener("close", () => {
      document.body.classList.remove("dialog-open");
      opener?.focus({ preventScroll: true });
    });
  }

  const copyButton = document.querySelector("[data-copy-citation]");
  const copyStatus = document.querySelector(".copy-status");
  copyButton.hidden = false;
  let feedbackTimer;
  copyButton.addEventListener("click", async () => {
    const citation = document.querySelector("#bibtex").textContent.trim();
    let copied = false;
    if (navigator.clipboard && window.isSecureContext) {
      try {
        await navigator.clipboard.writeText(citation);
        copied = true;
      } catch { /* Fall back to selection-based copying. */ }
    }
    if (!copied) {
      const selection = window.getSelection();
      const range = document.createRange();
      range.selectNodeContents(document.querySelector("#bibtex"));
      selection.removeAllRanges();
      selection.addRange(range);
      try { copied = document.execCommand("copy"); } catch { copied = false; }
      if (copied) selection.removeAllRanges();
    }
    copyStatus.textContent = copied ? "Citation copied to clipboard." : "Citation selected. Press Ctrl+C (or ⌘C) to copy.";
    copyButton.querySelector("span").textContent = copied ? "Copied!" : "Copy citation";
    clearTimeout(feedbackTimer);
    feedbackTimer = setTimeout(() => {
      copyButton.querySelector("span").textContent = "Copy citation";
      copyStatus.textContent = "";
    }, 4000);
  });

  const navigation = [...document.querySelectorAll(".nav-links a")].map((link) => ({
    link,
    section: document.querySelector(link.hash)
  })).filter(({ section }) => section);
  let navigationFrame;
  const updateNavigation = () => {
    navigationFrame = undefined;
    const readingLine = document.querySelector(".site-header").offsetHeight + window.innerHeight * .2;
    let current;
    navigation.forEach(({ link, section }) => {
      if (section.getBoundingClientRect().top <= readingLine) current = link;
    });
    navigation.forEach(({ link }) => {
      const active = link === current;
      link.classList.toggle("is-active", active);
      if (active) link.setAttribute("aria-current", "location");
      else link.removeAttribute("aria-current");
    });
  };
  const scheduleNavigation = () => {
    if (navigationFrame === undefined) navigationFrame = requestAnimationFrame(updateNavigation);
  };
  window.addEventListener("scroll", scheduleNavigation, { passive: true });
  window.addEventListener("resize", scheduleNavigation);
  updateNavigation();
})();
