(function () {
  var dd = document.querySelector("[data-drawdown-curve]");
  if (dd) {
    var svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
    svg.setAttribute("viewBox", "0 0 640 240");
    svg.setAttribute("class", "atlas-svg");
    svg.setAttribute("role", "img");
    svg.setAttribute("aria-label", "Hypothetical recovery curve. A 50 percent drawdown needs a 100 percent gain on what remains.");
    var d = "";
    for (var i = 1; i <= 80; i++) {
      var loss = i / 100;
      var need = loss / (1 - loss) * 100;
      var x = 40 + (i / 80) * 560;
      var y = 210 - Math.min(need, 400) / 400 * 170;
      d += (i === 1 ? "M" : "L") + x.toFixed(1) + " " + y.toFixed(1);
    }
    svg.innerHTML = '<text x="16" y="22" fill="#ffd06f" font-size="13">Hypothetical. recovery = 1/(1-d)-1</text><path d="' + d + '" fill="none" stroke="#52e4ff" stroke-width="3"/>';
    dd.appendChild(svg);
  }
  var fan = document.querySelector("[data-monte-carlo]");
  if (fan) {
    var svg2 = document.createElementNS("http://www.w3.org/2000/svg", "svg");
    svg2.setAttribute("viewBox", "0 0 640 220");
    svg2.setAttribute("class", "atlas-svg");
    svg2.setAttribute("role", "img");
    svg2.setAttribute("aria-label", "Hypothetical reshuffles of the same five R results. The ending sum matches. The path does not.");
    var sample = [-1, -1, 2, -1, 3];
    function rnd(seed) { var s = seed; return function () { s = (s * 16807) % 2147483647; return (s - 1) / 2147483646; }; }
    for (var p = 0; p < 18; p++) {
      var rand = rnd(1000 + p * 19);
      var bag = sample.slice();
      for (var i = bag.length - 1; i > 0; i--) {
        var j = Math.floor(rand() * (i + 1));
        var tmp = bag[i]; bag[i] = bag[j]; bag[j] = tmp;
      }
      var eq = 0, path = "M40 160";
      bag.forEach(function (v, k) {
        eq += v;
        path += " L" + (40 + ((k + 1) / bag.length) * 560).toFixed(1) + " " + (160 - eq * 22).toFixed(1);
      });
      var pathEl = document.createElementNS("http://www.w3.org/2000/svg", "path");
      pathEl.setAttribute("d", path);
      pathEl.setAttribute("fill", "none");
      pathEl.setAttribute("stroke", p === 0 ? "#f5bf5d" : "rgba(82,228,255,.55)");
      pathEl.setAttribute("stroke-width", "1.6");
      svg2.appendChild(pathEl);
    }
    var label = document.createElementNS("http://www.w3.org/2000/svg", "text");
    label.setAttribute("x", "16"); label.setAttribute("y", "22"); label.setAttribute("fill", "#ffd06f"); label.setAttribute("font-size", "13");
    label.textContent = "Hypothetical reshuffle of -1, -1, +2, -1, +3";
    svg2.appendChild(label);
    fan.appendChild(svg2);
  }
})();
