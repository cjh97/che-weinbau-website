// CH engineering – small progressive enhancements. Sets no cookies, stores nothing.
(function () {
  document.documentElement.classList.add("js");

  // Mobile navigation
  var toggle = document.querySelector("[data-nav-toggle]");
  if (toggle) {
    toggle.addEventListener("click", function () {
      var open = document.body.classList.toggle("nav-open");
      toggle.setAttribute("aria-expanded", open ? "true" : "false");
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

  // Reveal on scroll
  var targets = document.querySelectorAll(".feature, .product-card, .news-card, .module, .split-body, .spec-group, .contact-card, .intro > *, .story-inner > *");
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) { en.target.classList.add("in"); io.unobserve(en.target); }
      });
    }, { rootMargin: "0px 0px -8% 0px" });
    targets.forEach(function (el) { el.classList.add("reveal"); io.observe(el); });
  }

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
