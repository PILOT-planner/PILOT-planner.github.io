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

  document.querySelectorAll("[data-video]").forEach((card) => {
    const src = config.videos?.[card.dataset.video];
    if (!validResource(src)) return;
    const media = card.querySelector(".task-media");
    const still = media.querySelector("img");
    const placeholder = media.querySelector(".video-placeholder");
    const video = document.createElement("video");
    video.controls = true;
    video.playsInline = true;
    video.preload = "metadata";
    video.poster = still.src;
    video.setAttribute("aria-label", `${card.querySelector("h3").textContent} robot demonstration`);
    video.src = src;
    still.hidden = true;
    placeholder.hidden = true;
    media.append(video);
    video.addEventListener("play", () => {
      document.querySelectorAll(".task-media video").forEach((other) => {
        if (other !== video) other.pause();
      });
    });
    video.addEventListener("error", () => {
      video.remove();
      still.hidden = false;
      placeholder.hidden = false;
      placeholder.querySelector("span").textContent = "Video unavailable";
    }, { once: true });
  });
  if (Object.values(config.videos || {}).some(validResource)) {
    document.querySelector(".media-note").textContent = "Poster images are video-predicted subgoals from the paper. Use the video controls to play available robot demonstrations.";
  }

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
