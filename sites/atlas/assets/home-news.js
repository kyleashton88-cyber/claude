/* Homepage news block. No headline feed shipped with the upload, and the
   public news endpoint used during review is blocked from the browser.
   Show that plainly instead of inventing headlines or leaving "CONNECTING". */
(function () {
  var grid = document.getElementById("homeNewsGrid");
  if (!grid) return;
  grid.innerHTML = '<article class="home-news-fallback"><h3>Headlines are not in this build</h3><p>No sample headlines are substituted. The macro and intermarket page is the related module that was included.</p><p><a href="/macro-lab">Open Macro &amp; Intermarket →</a></p></article>';
})();
