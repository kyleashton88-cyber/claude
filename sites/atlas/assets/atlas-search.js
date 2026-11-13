(function () {
  var root = document.querySelector("[data-atlas-search-page]");
  if (!root || typeof Fuse === "undefined") return;
  var input = root.querySelector("[data-search-q]");
  var out = root.querySelector("[data-search-results]");
  var meta = root.querySelector("[data-search-meta]");
  fetch("/data/search-index.json").then(function (r) { return r.json(); }).then(function (data) {
    var items = data.entries || [];
    var fuse = new Fuse(items, { keys: ["title", "text", "kind"], threshold: 0.35, ignoreLocation: true, minMatchCharLength: 2 });
    function show(list, note) {
      meta.textContent = note;
      out.innerHTML = "";
      if (!list.length) {
        var p = document.createElement("p");
        p.textContent = "No matches. Try a shorter word, or open the glossary.";
        out.appendChild(p);
        return;
      }
      list.slice(0, 40).forEach(function (hit) {
        var item = hit.item || hit;
        var a = document.createElement("a");
        a.className = "search-hit";
        a.href = item.url;
        var b = document.createElement("b");
        b.textContent = item.title;
        var s = document.createElement("span");
        s.textContent = (item.kind || "page") + " · " + (item.text || "").slice(0, 180);
        a.append(b, s);
        out.appendChild(a);
      });
    }
    function run() {
      var q = input.value.trim();
      var url = new URL(location.href);
      if (q) url.searchParams.set("q", q); else url.searchParams.delete("q");
      history.replaceState(null, "", url);
      if (!q) show(items.map(function (item) { return { item: item }; }), items.length + " entries. Type to filter.");
      else show(fuse.search(q), "Matches for “" + q + "”.");
    }
    var params = new URLSearchParams(location.search);
    if (params.get("q")) input.value = params.get("q");
    input.addEventListener("input", run);
    run();
  }).catch(function () { meta.textContent = "The search index did not load."; });
})();
