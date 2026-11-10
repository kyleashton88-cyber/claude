(function () {
  var nav = document.querySelector("[data-grid-primary-nav]");
  var openBtn = document.querySelector("[data-grid-nav-toggle]");
  var closeBtn = document.querySelector("[data-grid-nav-close]");
  function scrollToHash() {
    if (!location.hash || location.hash.length < 2) return;
    var el = document.getElementById(decodeURIComponent(location.hash.slice(1)));
    if (!el) return;
    var root = document.documentElement;
    var prev = root.style.scrollBehavior;
    root.style.scrollBehavior = "auto";
    var y = el.getBoundingClientRect().top + window.scrollY - 88;
    window.scrollTo(0, Math.max(0, y));
    root.style.scrollBehavior = prev;
  }
  window.addEventListener("load", function () {
    scrollToHash();
    setTimeout(scrollToHash, 400);
  });
  if (!nav || !openBtn) return;
  function setOpen(on) {
    nav.classList.toggle("is-open", on);
    openBtn.setAttribute("aria-expanded", on ? "true" : "false");
    openBtn.setAttribute("aria-label", on ? "Close navigation" : "Open navigation");
  }
  openBtn.addEventListener("click", function () { setOpen(!nav.classList.contains("is-open")); });
  if (closeBtn) closeBtn.addEventListener("click", function () { setOpen(false); });
  nav.querySelectorAll("a").forEach(function (a) { a.addEventListener("click", function () { setOpen(false); }); });
  document.addEventListener("keydown", function (e) { if (e.key === "Escape") setOpen(false); });
})();
