/* Movies of the boosting-ladder article: canvas animations drawn in the style of the static figures
   (white ground, black axes, sans-serif labels, bold panel letters, Okabe-Ito colours). Data: data.json. */
(function () {
  "use strict";
  var COL = {ink: "#000000", grey: "#8c8c8c", sky: "#56B4E9", blue: "#0072B2", orange: "#E69F00",
             verm: "#D55E00", purple: "#CC79A7", rule: "#d9d9d9", red: "#b2182b", bluediv: "#2166ac"};
  var FONT = 'Helvetica, Arial, "Liberation Sans", sans-serif';
  var RM = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  function setup(cv) {
    var dpr = window.devicePixelRatio || 1, w = cv.clientWidth;
    if (!cv._h) cv._h = parseFloat(cv.getAttribute("height"));
    var h = cv._h;
    cv.style.height = h + "px"; cv.width = Math.round(w * dpr); cv.height = Math.round(h * dpr);
    var c = cv.getContext("2d"); c.setTransform(dpr, 0, 0, dpr, 0, 0);
    c.fillStyle = "#ffffff"; c.fillRect(0, 0, w, h);
    return {c: c, w: w, h: h};
  }

  /* one axes box inside a canvas; o = {x0,y0,w,h (fractions), xlim, ylim, xt, yt, xl, yl, logx, logy, letter, xf, yf} */
  function axes(S, o) {
    var c = S.c, L = S.w * o.x0 + 52, T = S.h * o.y0 + 16, W = S.w * o.w - 62, H = S.h * o.h - 52;
    var tx = o.logx ? Math.log10 : function (v) { return v; }, ty = o.logy ? Math.log10 : function (v) { return v; };
    var X = function (v) { return L + (tx(v) - tx(o.xlim[0])) / (tx(o.xlim[1]) - tx(o.xlim[0])) * W; };
    var Y = function (v) { return T + H - (ty(v) - ty(o.ylim[0])) / (ty(o.ylim[1]) - ty(o.ylim[0])) * H; };
    c.strokeStyle = COL.ink; c.lineWidth = 0.8; c.fillStyle = COL.ink; c.font = "11px " + FONT;
    c.beginPath(); c.moveTo(L, T); c.lineTo(L, T + H); c.lineTo(L + W, T + H); c.stroke();
    c.textAlign = "center"; c.textBaseline = "top";
    (o.xt || []).forEach(function (v) {
      c.beginPath(); c.moveTo(X(v), T + H); c.lineTo(X(v), T + H + 3); c.stroke();
      c.fillText(o.xf ? o.xf(v) : String(v), X(v), T + H + 5);
    });
    c.textAlign = "right"; c.textBaseline = "middle";
    (o.yt || []).forEach(function (v) {
      c.beginPath(); c.moveTo(L - 3, Y(v)); c.lineTo(L, Y(v)); c.stroke();
      c.fillText(o.yf ? o.yf(v) : String(v), L - 5, Y(v));
    });
    c.textAlign = "center"; c.textBaseline = "bottom";
    if (o.xl) c.fillText(o.xl, L + W / 2, T + H + 33);
    if (o.yl) { c.save(); c.translate(L - 40, T + H / 2); c.rotate(-Math.PI / 2); c.fillText(o.yl, 0, 0); c.restore(); }
    if (o.letter) { c.font = "bold 12px " + FONT; c.textAlign = "left"; c.textBaseline = "bottom"; c.fillText(o.letter, L - 50, T - 2); }
    return {c: c, X: X, Y: Y, L: L, T: T, W: W, H: H,
            clip: function () { c.save(); c.beginPath(); c.rect(L, T - 1, W, H + 2); c.clip(); },
            unclip: function () { c.restore(); }};
  }

  function line(A, xs, ys, color, width, dash, alpha) {
    var c = A.c, started = false;
    c.strokeStyle = color; c.lineWidth = width || 1; c.setLineDash(dash || []); c.globalAlpha = alpha == null ? 1 : alpha;
    c.beginPath();
    for (var i = 0; i < xs.length; i++) {
      if (ys[i] == null) continue;
      if (!started) { c.moveTo(A.X(xs[i]), A.Y(ys[i])); started = true; } else c.lineTo(A.X(xs[i]), A.Y(ys[i]));
    }
    c.stroke(); c.setLineDash([]); c.globalAlpha = 1;
  }
  function dot(A, x, y, color, r, hollow) {
    var c = A.c; c.beginPath(); c.arc(A.X(x), A.Y(y), r || 3, 0, 2 * Math.PI);
    if (hollow) { c.strokeStyle = color; c.lineWidth = 1; c.stroke(); } else { c.fillStyle = color; c.fill(); }
  }
  function note(S, text, x, y, align) {
    var c = S.c; c.font = "11px " + FONT; c.fillStyle = COL.ink; c.textAlign = align || "left"; c.textBaseline = "top"; c.fillText(text, x, y);
  }
  function range(n) { var a = []; for (var i = 0; i < n; i++) a.push(i); return a; }
  function maxAbs(rows) { var m = 0; rows.forEach(function (r) { r.forEach(function (v) { if (Math.abs(v) > m) m = Math.abs(v); }); }); return m; }

  /* a movie: n frames, draw(i), controls in fig .jn-movie-ctl */
  function movie(fig, n, fps, draw, loop) {
    var ctl = fig.querySelector(".jn-movie-ctl"), btn = ctl.querySelector("button"), rg = ctl.querySelector("input"),
        lab = ctl.querySelector("span"), st = {i: RM ? n - 1 : 0, play: false, visible: false, t: 0};
    rg.min = 0; rg.max = n - 1; rg.value = st.i;
    function show() { rg.value = st.i; lab.textContent = draw(st.i) || ""; btn.textContent = st.play ? "Pause" : "Play"; }
    btn.addEventListener("click", function () { if (!loop && st.i >= n - 1) st.i = 0; st.play = !st.play; show(); });
    rg.addEventListener("input", function () { st.i = +rg.value; st.play = false; show(); });
    if ("IntersectionObserver" in window) {
      new IntersectionObserver(function (es) {
        es.forEach(function (e) { st.visible = e.isIntersecting; if (e.isIntersecting && !RM && !st.started) { st.started = true; st.play = true; show(); } });
      }, {threshold: 0.35}).observe(fig);
    } else st.visible = true;
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
    window.addEventListener("resize", show);
    return st;
  }

  function hovImage(S, A, field, ref, vmax) {
    var nt = field.length, nx = field[0].length, img = S.c.createImageData(nx, nt);
    var pos = [178, 24, 43], neg = [33, 102, 172];
    for (var t = 0; t < nt; t++) for (var i = 0; i < nx; i++) {
      var v = (ref ? ref[t][i] - field[t][i] : field[t][i]) / vmax; v = Math.max(-1, Math.min(1, v));
      var tgt = v > 0 ? pos : neg, a = Math.abs(v), o = ((nt - 1 - t) * nx + i) * 4;
      for (var q = 0; q < 3; q++) img.data[o + q] = 255 + (tgt[q] - 255) * a;
      img.data[o + 3] = 255;
    }
    var off = document.createElement("canvas"); off.width = nx; off.height = nt; off.getContext("2d").putImageData(img, 0, 0);
    S.c.imageSmoothingEnabled = false; S.c.drawImage(off, A.L, A.T, A.W, A.H);
  }

  function start(D) {
    var NT = D.y.length, NX = D.y[0].length, XK = range(NX).map(function (i) { return i * D.dx_km; }), HRS = range(NT);
    var lim = Math.ceil(maxAbs(D.y)), yt = []; for (var v = -lim; v <= lim; v += Math.max(1, Math.round(lim / 3))) yt.push(v);
    var cx = [], cy = function (t) { var o = []; D.u[t].forEach(function (v) { o.push(v, v); }); return o; };
    D.u[0].forEach(function (_, j) { cx.push(j * 27, (j + 1) * 27); });

    var f1 = document.getElementById("movie-1");
    if (f1) movie(f1, NT, 6, function (t) {
      var cv = f1.querySelector("canvas"), S = setup(cv);
      var A = axes(S, {x0: 0, y0: 0, w: 0.56, h: 1, xlim: [0, 864], ylim: [-lim, lim], xt: [0, 200, 400, 600, 800], yt: yt, xl: "Distance (km)", yl: "Value", letter: "A"});
      A.clip(); line(A, cx, cy(t), COL.grey, 2.2); line(A, XK, D.y[t], COL.ink, 1.1); A.unclip();
      var P = D.pt, hi = Math.ceil(Math.max.apply(null, P.g.concat(P.M, P.u))), lo = Math.floor(Math.min.apply(null, P.u));
      var B = axes(S, {x0: 0.58, y0: 0, w: 0.42, h: 1, xlim: [0, 72], ylim: [lo, hi], xt: [0, 20, 40, 60], yt: [lo, 0, hi], xl: "Forecast hour", yl: "Value at " + D.point_km + " km", letter: "B"});
      var cut = function (a) { return a.map(function (v, i) { return i <= t ? v : null; }); };
      B.clip(); line(B, HRS, cut(P.u), COL.grey, 1); line(B, HRS, cut(P.g), COL.orange, 1.3); line(B, HRS, cut(P.M), COL.blue, 1.8); B.unclip();
      return "Hour " + t;
    }, true);

    var f2 = document.getElementById("movie-2");
    if (f2) movie(f2, NT, 6, function (t) {
      var cv = f2.querySelector("canvas"), S = setup(cv);
      var A = axes(S, {x0: 0, y0: 0, w: 1, h: 1, xlim: [0, 864], ylim: [-lim, lim], xt: [0, 200, 400, 600, 800], yt: yt, xl: "Distance (km)", yl: "Value"});
      A.clip(); var c = A.c; c.fillStyle = COL.verm; c.globalAlpha = 0.28; c.beginPath();
      XK.forEach(function (x, i) { var X = A.X(x), Yv = A.Y(D.y[t][i]); if (i) c.lineTo(X, Yv); else c.moveTo(X, Yv); });
      for (var i = NX - 1; i >= 0; i--) c.lineTo(A.X(XK[i]), A.Y(D.x0[t][i]));
      c.fill(); c.globalAlpha = 1;
      line(A, XK, D.y[t], COL.ink, 1.1); line(A, XK, D.x0[t], COL.blue, 1.8); A.unclip();
      return "Hour " + t;
    }, true);

    var f3 = document.getElementById("movie-3");
    if (f3) {
      var nu = String(D.order.choice.nu), rec = D.order.by_nu[nu] || D.order.by_nu[Object.keys(D.order.by_nu).filter(function (k) { return +k === D.order.choice.nu; })[0]];
      var NS = D.order.choice.n_stages, fields = [D.x0].concat(range(NS).map(function (i) { return D.comps[String(i + 1)]; }));
      movie(f3, fields.length, 1.2, function (k) {
        var cv = f3.querySelector("canvas"), S = setup(cv);
        var A = axes(S, {x0: 0, y0: 0, w: 0.5, h: 1, xlim: [0, 864], ylim: [-0.5, NT - 0.5], xt: [0, 250, 500, 750], yt: [0, 24, 48, 72], xl: "Distance (km)", yl: "Forecast hour", letter: "A"});
        hovImage(S, A, fields[k], D.y, 1.6);
        A.c.strokeStyle = COL.ink; A.c.lineWidth = 0.8; A.c.strokeRect(A.L, A.T, A.W, A.H);
        var keys = Object.keys(D.order.by_nu), all = [];
        keys.forEach(function (q) { all = all.concat(D.order.by_nu[q].val_rmse); });
        var B = axes(S, {x0: 0.52, y0: 0, w: 0.48, h: 1, xlim: [0, 30], ylim: [0.34, 0.58], xt: [0, 10, 20, 30], yt: [0.35, 0.45, 0.55], xl: "Rung", yl: "Validation RMSE", letter: "B", yf: function (v) { return v.toFixed(2); }});
        var cols = {}; keys.forEach(function (q) { cols[q] = (+q === 1) ? COL.verm : COL.blue; });
        B.clip();
        line(B, [0, 30], [D.s_rms_val, D.s_rms_val], COL.grey, 0.8, [2, 2]);
        line(B, [0].concat(rec.n_stages), [D.rmse0_val].concat(rec.val_rmse), COL.verm, 1.4);
        keys.forEach(function (q) { if (+q !== D.order.choice.nu) { var r = D.order.by_nu[q]; line(B, [0].concat(r.n_stages), [D.rmse0_val].concat(r.val_rmse), COL.blue, 1.2); } });
        var yk = k === 0 ? D.rmse0_val : rec.val_rmse[k - 1];
        dot(B, k, yk, COL.ink, 3.5);
        B.unclip();
        return (k === 0 ? "Rung 0 only" : "Rungs 0 to " + k) + ", validation RMSE " + yk.toFixed(3);
      }, true);
    }

    var f4 = document.getElementById("movie-4");
    if (f4) {
      var R = [["A", D.noise.truth, D.noise.truth_r1], ["B", D.noise.fixed.ex, D.noise.fixed.r1],
               ["C", D.noise.independent.ex, D.noise.independent.r1], ["D", D.noise.fitted.ex, D.noise.fitted.r1]];
      var rl = Math.ceil(maxAbs(R[0][1].concat(R[1][1], R[2][1], R[3][1])) * 10) / 10;
      movie(f4, NT, 3, function (t) {
        var cv = f4.querySelector("canvas"), S = setup(cv);
        R.forEach(function (r, j) {
          var A = axes(S, {x0: (j % 2) * 0.5, y0: Math.floor(j / 2) * 0.5, w: 0.5, h: 0.5, xlim: [0, 864], ylim: [-rl, rl], xt: [0, 400, 800], yt: [-1, 0, 1], xl: j > 1 ? "Distance (km)" : null, yl: "Value", letter: r[0]});
          A.clip();
          if (t > 0) line(A, XK, r[1][t - 1], COL.grey, 0.8, null, 0.8);
          line(A, XK, r[1][t], j === 0 ? COL.ink : COL.blue, 1);
          A.unclip();
          note(S, "R₁ = " + r[2].toFixed(2), A.L + A.W - 4, A.T, "right");
        });
        return "Hour " + t + "; gray: previous hour";
      }, true);
    }

    var fs = document.getElementById("movie-s1");
    if (fs) {
      var Bo = D.boost, nus = Object.keys(Bo.mse), bcols = [COL.verm, COL.orange, COL.blue, COL.purple];
      movie(fs, Bo.snaps.length, 1, function (k) {
        var cv = fs.querySelector("canvas"), S = setup(cv);
        var A = axes(S, {x0: 0, y0: 0, w: 0.5, h: 1, xlim: [0, 1], ylim: [-2.4, 2.4], xt: [0, 0.5, 1], yt: [-2, 0, 2], xl: "x", yl: "y", letter: "A"});
        A.clip(); var c = A.c; c.fillStyle = COL.grey;
        Bo.x.forEach(function (x, i) { c.fillRect(A.X(x) - 1, A.Y(Bo.y[i]) - 1, 2, 2); });
        line(A, Bo.grid, Bo.f, COL.ink, 1, [4, 3]); line(A, Bo.grid, Bo.snaps[k], COL.blue, 1.6); A.unclip();
        var B = axes(S, {x0: 0.52, y0: 0, w: 0.48, h: 1, xlim: [1, 3000], ylim: [0.08, 0.3], logx: true, xt: [1, 10, 100, 1000], yt: [0.1, 0.2, 0.3], xl: "Boosting round", yl: "MSE on new samples", letter: "B", yf: function (v) { return v.toFixed(1); }});
        var upto = Math.round(Bo.log_m.length * (k + 1) / Bo.snaps.length);
        B.clip(); line(B, [1, 3000], [Bo.noise, Bo.noise], COL.grey, 0.8, [2, 2]);
        nus.forEach(function (q, j) {
          line(B, Bo.log_m, Bo.mse[q].map(function (v, i) { return i < upto ? v : null; }), bcols[j], 1.2);
          if (Bo.best[q][0] <= Bo.log_m[upto - 1]) dot(B, Math.max(1, Bo.best[q][0]), Bo.best[q][1], bcols[j], 3);
        });
        B.unclip();
        return "Fit after " + Bo.snap_m[k] + " round" + (Bo.snap_m[k] > 1 ? "s" : "") + " with step size 0.1";
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
