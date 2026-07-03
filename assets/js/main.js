// =============================================================================
//  main.js — small, dependency-free UI behaviour.
//  Handles: theme toggle, code "copy" buttons, image lightbox, mobile nav,
//  and table-of-contents scroll-spy. No frameworks, no build step.
// =============================================================================
(function () {
  "use strict";

  /* ---- Theme toggle (persists choice in localStorage) -------------------- */
  var root = document.documentElement;
  function setTheme(t) {
    root.setAttribute("data-theme", t);
    try { localStorage.setItem("theme", t); } catch (e) {}
  }
  var toggle = document.querySelector(".theme-toggle");
  if (toggle) {
    toggle.addEventListener("click", function () {
      var current = root.getAttribute("data-theme") === "light" ? "light" : "dark";
      setTheme(current === "light" ? "dark" : "light");
    });
  }

  /* ---- Copy buttons on every code block ---------------------------------- */
  var COPY_ICON =
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="9" width="13" height="13" rx="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg>';

  // A code block is either a Hugo .highlight wrapper or a bare <pre>.
  var blocks = document.querySelectorAll(".article-body .highlight, .article-body pre:not(.highlight pre), .terminal");
  blocks.forEach(function (block) {
    var pre = block.matches("pre") ? block : block.querySelector("pre");
    if (!pre) return;
    var btn = document.createElement("button");
    btn.type = "button";
    btn.className = "copy-btn";
    btn.setAttribute("aria-label", "Copy code to clipboard");
    btn.innerHTML = COPY_ICON + "<span>Copy</span>";
    block.appendChild(btn);

    btn.addEventListener("click", function () {
      var code = pre.querySelector("code") || pre;
      var text = code.innerText.replace(/\n$/, "");
      var done = function () {
        btn.classList.add("copied");
        btn.querySelector("span").textContent = "Copied!";
        setTimeout(function () {
          btn.classList.remove("copied");
          btn.querySelector("span").textContent = "Copy";
        }, 1600);
      };
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(done).catch(fallback);
      } else {
        fallback();
      }
      function fallback() {
        var ta = document.createElement("textarea");
        ta.value = text; ta.style.position = "fixed"; ta.style.opacity = "0";
        document.body.appendChild(ta); ta.select();
        try { document.execCommand("copy"); done(); } catch (e) {}
        document.body.removeChild(ta);
      }
    });
  });

  /* ---- Image lightbox (click any article image to zoom) ------------------ */
  var imgs = document.querySelectorAll(".article-body figure img, .article-body p > img");
  if (imgs.length) {
    var lb = document.createElement("div");
    lb.className = "lightbox";
    lb.innerHTML = '<button class="lb-close" aria-label="Close">&times;</button><img alt="">';
    document.body.appendChild(lb);
    var lbImg = lb.querySelector("img");
    function closeLb() { lb.classList.remove("open"); }
    lb.addEventListener("click", closeLb);
    imgs.forEach(function (img) {
      img.style.cursor = "zoom-in";
      img.addEventListener("click", function () {
        lbImg.src = img.src; lbImg.alt = img.alt || "";
        lb.classList.add("open");
      });
    });
    document.addEventListener("keydown", function (e) { if (e.key === "Escape") closeLb(); });
  }

  /* ---- Mobile nav toggle -------------------------------------------------- */
  var navToggle = document.querySelector(".nav-toggle");
  var nav = document.querySelector(".nav");
  if (navToggle && nav) {
    navToggle.addEventListener("click", function () {
      var open = nav.classList.toggle("open");
      navToggle.setAttribute("aria-expanded", open ? "true" : "false");
    });
  }

  /* ---- TOC scroll-spy (highlights the current section) ------------------- */
  var tocLinks = document.querySelectorAll(".toc-wrap nav a");
  if (tocLinks.length && "IntersectionObserver" in window) {
    var map = {};
    tocLinks.forEach(function (a) {
      var id = decodeURIComponent((a.getAttribute("href") || "").replace(/^#/, ""));
      if (id) map[id] = a;
    });
    var heads = Object.keys(map).map(function (id) { return document.getElementById(id); }).filter(Boolean);
    var current = null;
    var obs = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          if (current) current.classList.remove("active");
          current = map[entry.target.id];
          if (current) current.classList.add("active");
        }
      });
    }, { rootMargin: "-10% 0px -80% 0px", threshold: 0 });
    heads.forEach(function (h) { obs.observe(h); });
  }
})();
