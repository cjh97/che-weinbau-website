// CH engineering – small progressive enhancements. Sets no cookies, stores nothing.
(function () {
  // Header: transparent over the hero photo, solid once the page scrolls
  var header = document.querySelector("[data-header]");
  var heroEl = document.querySelector(".hero");
  function onScroll() {
    if (!header) return;
    // stay transparent while the hero photo is behind the header, turn white after it
    var limit = heroEl ? heroEl.getBoundingClientRect().bottom + window.scrollY - header.offsetHeight : 40;
    var over = heroEl ? heroEl.querySelector(".hero-content").getBoundingClientRect().bottom + window.scrollY - header.offsetHeight : limit;
    header.classList.toggle("scrolled", window.scrollY > Math.min(limit, Math.max(over, 40)));
  }
  var lastY = window.scrollY;
  window.addEventListener("scroll", function () {
    var y = window.scrollY;
    if (header && !document.body.classList.contains("nav-open")) {
      header.classList.toggle("hide", y > lastY && y > 60);
    }
    lastY = y;
  }, { passive: true });
  window.addEventListener("scroll", onScroll, { passive: true });
  window.addEventListener("resize", onScroll);
  onScroll();

  // Mobile navigation
  var toggle = document.querySelector("[data-nav-toggle]");
  if (toggle) {
    toggle.addEventListener("click", function () {
      var open = document.body.classList.toggle("nav-open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
      document.documentElement.style.overflow = open ? "hidden" : "";
    });
  }

  // Analytics events (Plausible, cookieless): count phone / email clicks as enquiries
  document.addEventListener("click", function (ev) {
    var a = ev.target.closest && ev.target.closest("a[href^='tel:'], a[href^='mailto:']");
    if (a && window.plausible) {
      window.plausible("Contact", { props: { type: a.href.indexOf("tel:") === 0 ? "phone" : "email", page: location.pathname } });
    }
  });

  // Hide trade-fair banners after their end date
  var today = new Date().toISOString().slice(0, 10);
  document.querySelectorAll("[data-event-end]").forEach(function (el) {
    if (el.getAttribute("data-event-end") < today) el.remove();
  });

  // Map: clicking a marker with a story shows its card
  var marks = document.querySelectorAll(".worldmap .has-story");
  function showStory(id) {
    document.querySelectorAll(".worldmap .story").forEach(function (st) { st.hidden = st.getAttribute("data-story") !== id; });
    document.querySelectorAll(".worldmap .mk").forEach(function (m) { m.classList.toggle("active", m.getAttribute("data-loc") === id); });
  }
  marks.forEach(function (m) {
    var id = m.getAttribute("data-loc");
    m.addEventListener("click", function () { showStory(id); });
    m.addEventListener("keydown", function (ev) { if (ev.key === "Enter" || ev.key === " ") { ev.preventDefault(); showStory(id); } });
  });
  var home = document.querySelector(".worldmap .mk-home.has-story") || marks[0];
  if (home) showStory(home.getAttribute("data-loc"));

  // Lightbox for galleries
  var lb = document.querySelector("[data-lightbox]");
  var links = Array.prototype.slice.call(document.querySelectorAll("[data-lb]"));
  if (lb && links.length) {
    var imgEl = lb.querySelector("img"), idx = 0;
    function show(i) {
      idx = (i + links.length) % links.length;
      imgEl.src = links[idx].getAttribute("href");
      imgEl.alt = (links[idx].querySelector("img") || {}).alt || "";
      lb.hidden = false;
      document.body.style.overflow = "hidden";
    }
    function hide() { lb.hidden = true; document.body.style.overflow = ""; }
    links.forEach(function (a, i) {
      a.addEventListener("click", function (ev) { ev.preventDefault(); show(i); });
    });
    lb.querySelector(".lb-close").addEventListener("click", hide);
    lb.querySelector(".lb-prev").addEventListener("click", function () { show(idx - 1); });
    lb.querySelector(".lb-next").addEventListener("click", function () { show(idx + 1); });
    lb.addEventListener("click", function (ev) { if (ev.target === lb) hide(); });
    document.addEventListener("keydown", function (ev) {
      if (lb.hidden) return;
      if (ev.key === "Escape") hide();
      if (ev.key === "ArrowLeft") show(idx - 1);
      if (ev.key === "ArrowRight") show(idx + 1);
    });
  }
})();
