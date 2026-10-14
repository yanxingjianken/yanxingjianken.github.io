/* Movies of the successive-correction article, drawn on canvas in the style of the static figures (white ground,
   black axes, sans-serif labels, bold capital panel letters, Okabe-Ito colours, the figures' diverging colour scale).
   movie-orders (Movie 1): the order loop (n = 1 ... N) of the corrected member mean.
   movie-hours (Movie 2): the hour loop (t = 0 ... 72) through the chain, the field along x at each hour.
   Data: data.json (arrays as base64 little-endian integers with a scale). Controls: play/pause and a slider; a movie
   starts when it scrolls into view and, with reduced motion requested, shows its last frame without playing. */
(function () {
  "use strict";
  var COL = {ink: "#000000", grey: "#8c8c8c", light: "#c4c4c4", sky: "#56B4E9", blue: "#0072B2", orange: "#E69F00",
             verm: "#D55E00"};
  var FONT = 'Helvetica, Arial, "Liberation Sans", "Nimbus Sans", sans-serif';
  var RM = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  function decode(b64, bytes) {
    var s = atob(b64), n = s.length, u = new Uint8Array(n);
    for (var i = 0; i < n; i++) u[i] = s.charCodeAt(i);
    return bytes === 1 ? new Int8Array(u.buffer) : new Int16Array(u.buffer);
  }
  /* rows of length nx from a flat typed array, times scale */
  function rows(a, nx, scale, offset, count) {
    var out = [];
    for (var r = 0; r < count; r++) {
      var row = new Float32Array(nx), o = offset + r * nx;
      for (var i = 0; i < nx; i++) row[i] = a[o + i] * scale;
      out.push(row);
    }
    return out;
  }

  function setup(cv, h) {
    var dpr = window.devicePixelRatio || 1, w = cv.clientWidth;
    cv.style.height = h + "px"; cv.width = Math.round(w * dpr); cv.height = Math.round(h * dpr);
    var c = cv.getContext("2d"); c.setTransform(dpr, 0, 0, dpr, 0, 0);
    c.fillStyle = "#ffffff"; c.fillRect(0, 0, w, h);
    return {c: c, w: w, h: h};
  }

  /* text with _{sub} and ^{sup} parts */
  function rich(c, s, x, y, size, align) {
    var parts = s.split(/(_\{[^}]*\}|\^\{[^}]*\})/).filter(function (p) { return p; }), w = 0, pieces = [];
    parts.forEach(function (p) {
      var sub = p.indexOf("_{") === 0, sup = p.indexOf("^{") === 0, t = (sub || sup) ? p.slice(2, -1) : p;
      var fs = (sub || sup) ? Math.round(size * 0.72) : size;
      c.font = fs + "px " + FONT;
      pieces.push({t: t, fs: fs, dy: sub ? size * 0.28 : (sup ? -size * 0.38 : 0), w: c.measureText(t).width});
      w += pieces[pieces.length - 1].w;
    });
    var x0 = align === "right" ? x - w : (align === "center" ? x - w / 2 : x);
    c.textAlign = "left"; c.textBaseline = "alphabetic";
    pieces.forEach(function (p) { c.font = p.fs + "px " + FONT; c.fillText(p.t, x0, y + p.dy); x0 += p.w; });
    return w;
  }

  /* axes box in pixels: o = {L, T, W, H, xlim, ylim, xt, yt, xl, yl, letter, xticklabels} */
  function axes(S, o) {
    var c = S.c, L = o.L, T = o.T, W = o.W, H = o.H;
    var X = function (v) { return L + (v - o.xlim[0]) / (o.xlim[1] - o.xlim[0]) * W; };
    var Y = function (v) { return T + H - (v - o.ylim[0]) / (o.ylim[1] - o.ylim[0]) * H; };
    c.strokeStyle = COL.ink; c.lineWidth = 0.8; c.fillStyle = COL.ink; c.font = "11px " + FONT;
    c.beginPath(); c.moveTo(L, T); c.lineTo(L, T + H); c.lineTo(L + W, T + H); c.stroke();
    c.textAlign = "center"; c.textBaseline = "top";
    (o.xt || []).forEach(function (v) {
      c.beginPath(); c.moveTo(X(v), T + H); c.lineTo(X(v), T + H + 3); c.stroke();
      if (o.xticklabels !== false) c.fillText(String(v), X(v), T + H + 5);
    });
    c.textAlign = "right"; c.textBaseline = "middle";
    (o.yt || []).forEach(function (v) {
      c.beginPath(); c.moveTo(L - 3, Y(v)); c.lineTo(L, Y(v)); c.stroke();
      c.fillText(String(v), L - 5, Y(v));
    });
    c.textAlign = "center"; c.textBaseline = "bottom";
    if (o.xl) c.fillText(o.xl, L + W / 2, T + H + 32);
    if (o.yl) { c.save(); c.translate(L - 30, T + H / 2); c.rotate(-Math.PI / 2); c.fillText(o.yl, 0, 0); c.restore(); }
    if (o.letter) { c.font = "bold 12px " + FONT; c.textAlign = "left"; c.textBaseline = "alphabetic"; c.fillText(o.letter, L - 40, T - 4); }
    return {c: c, X: X, Y: Y, L: L, T: T, W: W, H: H,
            clip: function () { c.save(); c.beginPath(); c.rect(L, T - 1, W, H + 2); c.clip(); },
            unclip: function () { c.restore(); }};
  }

  function line(A, xs, ys, color, width, dash) {
    var c = A.c;
    c.strokeStyle = color; c.lineWidth = width || 1; c.setLineDash(dash || []);
    c.beginPath();
    for (var i = 0; i < xs.length; i++) { if (i) c.lineTo(A.X(xs[i]), A.Y(ys[i])); else c.moveTo(A.X(xs[i]), A.Y(ys[i])); }
    c.stroke(); c.setLineDash([]);
  }

  /* a key: short line samples with rich-text labels, laid out left to right, wrapping at maxW */
  function key(c, items, x, y, maxW) {
    var cx = x, cy = y;
    items.forEach(function (it) {
      c.font = "11px " + FONT;
      var probe = it[0].replace(/[_^]\{([^}]*)\}/g, "$1"), w = 22 + c.measureText(probe).width + 14;
      if (cx > x && cx + w > x + maxW) { cx = x; cy += 15; }
      c.strokeStyle = it[1]; c.lineWidth = it[2]; c.setLineDash(it[3] || []);
      c.beginPath(); c.moveTo(cx, cy - 4); c.lineTo(cx + 18, cy - 4); c.stroke(); c.setLineDash([]);
      c.fillStyle = COL.ink; cx += 22 + rich(c, it[0], cx + 22, cy, 11) + 14;
    });
    return cy;
  }

  function movie(fig, n, fps, draw, loop) {
    var ctl = fig.querySelector(".jn-movie-ctl"), btn = ctl.querySelector("button"), rg = ctl.querySelector("input"),
        lab = ctl.querySelector("span"), st = {i: RM ? n - 1 : 0, play: false, visible: false, started: false};
    rg.min = 0; rg.max = n - 1; rg.step = 1; rg.value = st.i;
    function show() { rg.value = st.i; lab.textContent = draw(st.i) || ""; btn.textContent = st.play ? "Pause" : "Play"; }
    btn.addEventListener("click", function () { if (!loop && st.i >= n - 1) st.i = 0; st.play = !st.play; show(); });
    rg.addEventListener("input", function () { st.i = +rg.value; st.play = false; show(); });
    if ("IntersectionObserver" in window) {
      new IntersectionObserver(function (es) {
        es.forEach(function (e) {
          st.visible = e.isIntersecting;
          if (e.isIntersecting && !RM && !st.started) { st.started = true; st.play = true; show(); }
        });
      }, {threshold: 0.3}).observe(fig);
    } else { st.visible = true; }
    var last = 0;
    function tick(ts) {
      if (st.play && st.visible && ts - last > 1000 / fps) {
        last = ts; st.i += 1;
        if (st.i >= n) { if (loop) st.i = 0; else { st.i = n - 1; st.play = false; } }
        show();
      }
      requestAnimationFrame(tick);
    }
    show(); requestAnimationFrame(tick);
    var rt = null;
    window.addEventListener("resize", function () { clearTimeout(rt); rt = setTimeout(show, 120); });
  }

  function start(D) {
    var NX = D.nx, NT = D.nt, K = D.K, NN = D.N, s16 = D.scale, XK = [];
    for (var i = 0; i < NX; i++) XK.push(i * D.dx_km);
    var dec = function (k) { return decode(D[k], 2); };
    var truth = rows(dec("truth"), NX, s16, 0, NT), xbar = rows(dec("xbar"), NX, s16, 0, NT),
        xN = rows(dec("xN"), NX, s16, 0, NT), Xa = dec("X"), Ya = dec("Y");
    var X = [], Y = [];
    for (var k = 0; k < K; k++) { X.push(rows(Xa, NX, s16, k * NT * NX, NT)); Y.push(rows(Ya, NX, s16, k * NT * NX, NT)); }
    var yl = D.ylim, yt = D.yticks, NS = "x̄^{(" + NN + ")}";

    /* Movie 2: the hour loop */
    var f1 = document.getElementById("movie-hours");
    if (f1) movie(f1, NT, 4, function (t) {
      var cv = f1.querySelector("canvas"), narrow = cv.clientWidth < 560, head = 34, ph = narrow ? 112 : 124;
      var S = setup(cv, 3 * (head + ph + 16) + 34), L = 46, Wd = S.w - L - 8;
      var specs = [
        {title: "Order 0 and split: members x_{k,t} and their mean x̄_{t}",
         keys: [["truth y", COL.ink, 1.3], ["members x_{k,t}", COL.sky, 1], ["mean x̄_{t}", COL.blue, 1.8]],
         draw: function (A) { for (var k = 0; k < K; k++) line(A, XK, X[k][t], COL.sky, 0.7); line(A, XK, xbar[t], COL.blue, 1.8); }},
        {title: "Orders 1 to " + NN + ": the corrected mean " + NS + "_{t}",
         keys: [["truth y", COL.ink, 1.3], ["x̄_{t}", COL.grey, 1.2], [NS + "_{t}", COL.blue, 1.8]],
         draw: function (A) { line(A, XK, xbar[t], COL.grey, 1.2); line(A, XK, xN[t], COL.blue, 1.8); }},
        {title: "Perturbation scaling: output members y_{k,t}",
         keys: [["truth y", COL.ink, 1.3], ["members y_{k,t}", COL.sky, 1], [NS + "_{t}", COL.blue, 1.8]],
         draw: function (A) { for (var k = 0; k < K; k++) line(A, XK, Y[k][t], COL.sky, 0.7); line(A, XK, xN[t], COL.blue, 1.8); }}];
      var top = 4;
      specs.forEach(function (sp, j) {
        var c = S.c; c.fillStyle = COL.ink; c.font = "bold 12px " + FONT; c.textAlign = "left"; c.textBaseline = "alphabetic";
        c.fillText("ABC"[j], 2, top + 13);
        rich(c, sp.title, 18, top + 13, 11.5);
        key(c, sp.keys, 18, top + 29, S.w - 22);
        var A = axes(S, {L: L, T: top + head + 6, W: Wd, H: ph, xlim: [0, NX * D.dx_km], ylim: yl, xt: [0, 200, 400, 600, 800],
                         yt: yt, xticklabels: j === 2, xl: j === 2 ? "position (km)" : null, yl: "value"});
        A.clip(); sp.draw(A); line(A, XK, truth[t], COL.ink, 1.3); A.unclip();
        top += head + ph + 16;
      });
      return "Hour " + t + " of " + (NT - 1);
    }, true);

    /* Movie 1: the order loop, n = 1 ... N */
    var f2 = document.getElementById("movie-orders");
    if (f2) {
      var E8 = decode(D.stage_err, 1), es = D.err_scale, S1 = rows(decode(D.stage_1d, 2), NX, s16, 0, NN), lut = D.diff_lut,
          tr1 = truth[D.hour_1d];
      var img = function (n) {
        var im = document.createElement("canvas"); im.width = NX; im.height = NT;
        var ctx = im.getContext("2d"), id = ctx.createImageData(NX, NT), o = n * NT * NX;
        for (var t = 0; t < NT; t++) for (var i = 0; i < NX; i++) {
          var v = E8[o + t * NX + i] * es / D.dmax, q = Math.max(0, Math.min(255, Math.round((v + 1) / 2 * 255)));
          var p = ((NT - 1 - t) * NX + i) * 4, col = lut[q];
          id.data[p] = col[0]; id.data[p + 1] = col[1]; id.data[p + 2] = col[2]; id.data[p + 3] = 255;
        }
        ctx.putImageData(id, 0, 0); return im;
      };
      var cache = {};
      movie(f2, NN, 1.5, function (n) {
        var cv = f2.querySelector("canvas"), narrow = cv.clientWidth < 560, S = setup(cv, narrow ? 560 : 300), c = S.c;
        var A, B;
        if (narrow) {
          A = axes(S, {L: 46, T: 26, W: S.w - 120, H: 230, xlim: [0, NX * D.dx_km], ylim: [-0.5, NT - 0.5], xt: [0, 400, 800], yt: [0, 24, 48, 72], xl: "position (km)", yl: "hour", letter: "A"});
          B = axes(S, {L: 46, T: 340, W: S.w - 56, H: 150, xlim: [0, NX * D.dx_km], ylim: yl, xt: [0, 200, 400, 600, 800], yt: yt, xl: "position (km)", yl: "value", letter: "B"});
        } else {
          A = axes(S, {L: 46, T: 26, W: S.w * 0.42 - 84, H: 220, xlim: [0, NX * D.dx_km], ylim: [-0.5, NT - 0.5], xt: [0, 400, 800], yt: [0, 24, 48, 72], xl: "position (km)", yl: "hour", letter: "A"});
          B = axes(S, {L: S.w * 0.42 + 78, T: 26, W: S.w * 0.58 - 88, H: 220, xlim: [0, NX * D.dx_km], ylim: yl, xt: [0, 200, 400, 600, 800], yt: yt, xl: "position (km)", yl: "value", letter: "B"});
        }
        if (!cache[n]) cache[n] = img(n);
        c.imageSmoothingEnabled = false; c.drawImage(cache[n], A.L, A.T, A.W, A.H);
        c.strokeStyle = COL.ink; c.lineWidth = 0.8; c.strokeRect(A.L, A.T, A.W, A.H);
        c.fillStyle = COL.ink; c.beginPath(); var yh = A.Y(D.hour_1d);
        c.moveTo(A.L - 1, yh); c.lineTo(A.L - 7, yh - 3.5); c.lineTo(A.L - 7, yh + 3.5); c.fill();
        /* colour bar */
        var cbx = A.L + A.W + 10, cbw = 9;
        for (var q = 0; q < 256; q++) { var col = lut[q]; c.fillStyle = "rgb(" + col[0] + "," + col[1] + "," + col[2] + ")"; c.fillRect(cbx, A.T + A.H - (q + 1) * A.H / 256, cbw, A.H / 256 + 0.6); }
        c.strokeRect(cbx, A.T, cbw, A.H); c.fillStyle = COL.ink; c.font = "10px " + FONT; c.textAlign = "left"; c.textBaseline = "middle";
        [-D.dmax_tick, 0, D.dmax_tick].forEach(function (v) { c.fillText(String(v), cbx + cbw + 3, A.T + A.H / 2 - v / D.dmax * A.H / 2); });
        c.textAlign = "left"; c.textBaseline = "alphabetic"; c.font = "11px " + FONT;
        rich(c, "error x̄^{(" + (n + 1) + ")} − y", A.L, A.T - 8, 11);
        B.clip();
        if (n > 0) line(B, XK, S1[n - 1], COL.grey, 1.1);
        line(B, XK, S1[n], COL.blue, 1.8); line(B, XK, tr1, COL.ink, 1.3); B.unclip();
        var items = [["truth y", COL.ink, 1.3], ["x̄^{(" + (n + 1) + ")}", COL.blue, 1.8]];
        if (n > 0) items.push(["x̄^{(" + n + ")}", COL.grey, 1.1]);
        key(c, items, B.L + 4, B.T + 12, B.W - 8);
        c.font = "11px " + FONT; c.textAlign = "right"; c.fillStyle = COL.ink; c.textBaseline = "alphabetic";
        c.fillText("hour " + D.hour_1d, B.L + B.W, B.T - 8);
        return "Order n = " + (n + 1) + (n === 0 ? " (order 1, before the loop)" : "") + "; RMSE of this run " + D.stage_rmse[n].toFixed(3);
      }, true);
    }
  }

  function boot() {
    var root = document.querySelector("[data-movies]");
    if (!root) return;
    fetch(root.getAttribute("data-movies")).then(function (r) { return r.json(); }).then(start)
      .catch(function () { document.querySelectorAll(".jn-movie-ctl span").forEach(function (s) { s.textContent = "Movie data could not be loaded."; }); });
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", boot); else boot();
})();
