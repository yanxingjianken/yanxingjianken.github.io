/* Doubly periodic beta-plane barotropic vorticity model, pseudo-spectral.
 *
 *   dzeta/dt + J(psi, zeta) + beta dpsi/dx = F_jet + F_stir + F_mouse - mu zeta - nu del^8 zeta,   zeta = del^2 psi
 *
 * Units: length 1000 km, time 1 day (velocity 1 unit = 11.574 m/s, vorticity 1 unit = 1.157e-5 s-1).
 * Domain Lx x Ly (default 20 x 10, i.e. 20 000 km x 10 000 km); the y axis is labelled 0-90 deg N (111 km per degree).
 * Spatial derivatives and the Poisson inversion are spectral (exact for a doubly periodic domain); the Jacobian is
 * evaluated on the grid and dealiased with the 2/3 rule.  Time stepping: third-order Adams-Bashforth for advection,
 * beta and forcing, with friction and hyperviscosity applied as an exact decay factor.  A CFL check halves the step
 * (and restarts the Adams-Bashforth history) when the flow gets fast.
 *
 * Forcing:
 *   jet   - the zonal-mean vorticity relaxes (time scale tauJet) to that of a Gaussian jet U(y) of peak speed U0,
 *           half-width w and centre yJet (periodised in y, domain mean removed);
 *   stir  - G(y) * sum_{m-1..m+1} Re[a_m(t) exp(i k_m x)], G Gaussian of half-width wStir around yStir, a_m complex
 *           red noise with correlation time tauStir;
 *   mouse - "push": a velocity impulse with a Gaussian footprint (its vorticity is a dipole); "vortex": a Gaussian
 *           vortex (cyclone > 0, anticyclone < 0 in the Northern Hemisphere).
 * Used by assets/js/beta-plane-worker.js; also loadable in Node for tests (module.exports).
 */
(function (root) {
  'use strict';

  /* ---------------------------------------------------------------- 1-D complex FFT plans (radix 2) */
  function makePlan(n) {
    var bits = Math.round(Math.log2(n)); if ((1 << bits) !== n) throw new Error('FFT size must be a power of 2: ' + n);
    var rev = new Uint32Array(n);
    for (var i = 0; i < n; i++) { var r = 0, x = i; for (var b = 0; b < bits; b++) { r = (r << 1) | (x & 1); x >>= 1; } rev[i] = r; }
    var cs = new Float64Array(n / 2), sn = new Float64Array(n / 2);
    for (var k = 0; k < n / 2; k++) { cs[k] = Math.cos(2 * Math.PI * k / n); sn[k] = Math.sin(2 * Math.PI * k / n); }
    return {n: n, rev: rev, cs: cs, sn: sn};
  }
  /* in place on re/im[off + s*idx], idx = 0..n-1 (s = stride); sign -1 forward, +1 inverse (unnormalised) */
  function fft1(p, re, im, off, s, sign) {
    var n = p.n, rev = p.rev, cs = p.cs, sn = p.sn, i, j, t;
    for (i = 0; i < n; i++) { j = rev[i]; if (j > i) { var a = off + s * i, b = off + s * j; t = re[a]; re[a] = re[b]; re[b] = t; t = im[a]; im[a] = im[b]; im[b] = t; } }
    for (var size = 2; size <= n; size <<= 1) {
      var half = size >> 1, step = n / size;
      for (var start = 0; start < n; start += size) {
        for (var k = 0; k < half; k++) {
          var wr = cs[k * step], wi = sign * sn[k * step];
          var ia = off + s * (start + k), ib = off + s * (start + k + half);
          var xr = re[ib] * wr - im[ib] * wi, xi = re[ib] * wi + im[ib] * wr;
          re[ib] = re[ia] - xr; im[ib] = im[ia] - xi; re[ia] += xr; im[ia] += xi;
        }
      }
    }
  }

  function BetaPlane(opt) {
    opt = opt || {};
    this.Nx = opt.Nx || 256; this.Ny = opt.Ny || 128; this.Lx = opt.Lx || 20; this.Ly = opt.Ly || 10;
    var Nx = this.Nx, Ny = this.Ny, n = Nx * Ny;
    this.px = makePlan(Nx); this.py = makePlan(Ny);
    this.colR = new Float64Array(Ny); this.colI = new Float64Array(Ny);
    this.kx = new Float64Array(Nx); this.ky = new Float64Array(Ny);
    for (var i = 0; i < Nx; i++) this.kx[i] = 2 * Math.PI / this.Lx * (i <= Nx / 2 ? i : i - Nx);
    for (var j = 0; j < Ny; j++) this.ky[j] = 2 * Math.PI / this.Ly * (j <= Ny / 2 ? j : j - Ny);
    this.K2 = new Float64Array(n); this.mask = new Uint8Array(n);
    var ix = Nx / 3, jy = Ny / 3;
    for (j = 0; j < Ny; j++) for (i = 0; i < Nx; i++) {
      var q = j * Nx + i, ii = i <= Nx / 2 ? i : Nx - i, jj = j <= Ny / 2 ? j : Ny - j;
      this.K2[q] = this.kx[i] * this.kx[i] + this.ky[j] * this.ky[j];
      this.mask[q] = (ii < ix && jj < jy && q !== 0) ? 1 : 0;
    }
    this.dx = this.Lx / Nx; this.dy = this.Ly / Ny;
    var names = ['zr', 'zi', 'Ar', 'Ai', 'Br', 'Bi', 'Jr', 'Ji', 'N0r', 'N0i', 'N1r', 'N1i', 'N2r', 'N2i', 'Mr', 'Mi', 'E'];
    for (var a = 0; a < names.length; a++) this[names[a]] = new Float64Array(n);
    this.u = new Float32Array(n); this.v = new Float32Array(n);
    this.p = {beta: 1.40, jetOn: true, yJet: 5, wJet: 1.0, U0: 2.6, tauJet: 4, stirOn: true, yStir: 5, wStir: 0.8, mStir: 6, Astir: 1.5, tauStir: 2,
              tauFric: 10, hypo: 20};
    if (opt.params) for (var key in opt.params) this.p[key] = opt.params[key];
    this.t = 0; this.dt0 = opt.dt || 0.6 * this.dx / 5; this.dt = this.dt0; this.nab = 0; this.cfl = 0; this.umax = 0;
    this.stirA = []; this.seed = 12345; this.pending = [];
    this.updateForcing(); this.updateDamping();
  }
  var BP = BetaPlane.prototype;

  BP.rand = function () { this.seed = (this.seed * 1664525 + 1013904223) >>> 0; return this.seed / 4294967296; };
  BP.gauss = function () { var u = Math.max(1e-12, this.rand()), v = this.rand(); return Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * v); };

  BP.fft2 = function (re, im, sign) {
    var Nx = this.Nx, Ny = this.Ny, j, i;
    for (j = 0; j < Ny; j++) fft1(this.px, re, im, j * Nx, 1, sign);
    var cr = this.colR, ci = this.colI;
    for (i = 0; i < Nx; i++) {
      for (j = 0; j < Ny; j++) { cr[j] = re[j * Nx + i]; ci[j] = im[j * Nx + i]; }
      fft1(this.py, cr, ci, 0, 1, sign);
      for (j = 0; j < Ny; j++) { re[j * Nx + i] = cr[j]; im[j * Nx + i] = ci[j]; }
    }
  };

  /* periodic Gaussian in y (three images) */
  BP.pg = function (y, y0, w) { var s = 0; for (var m = -1; m <= 1; m++) { var d = (y - y0 + m * this.Ly) / w; s += Math.exp(-d * d); } return s; };
  BP.pgd = function (y, y0, w) { var s = 0; for (var m = -1; m <= 1; m++) { var d = (y - y0 + m * this.Ly) / w; s += -2 * d / w * Math.exp(-d * d); } return s; };

  /* zonal-mean target vorticity of the jet and the meridional structure of the stirring, as 1-D spectra (scaled by Nx) */
  BP.updateForcing = function () {
    var Ny = this.Ny, Nx = this.Nx, p = this.p, j, q;
    this.jetUy = new Float64Array(Ny); var zj = new Float64Array(Ny), mean = 0;
    for (j = 0; j < Ny; j++) { var y = j * this.dy; this.jetUy[j] = p.U0 * this.pg(y, p.yJet, p.wJet); mean += this.jetUy[j] / Ny; zj[j] = -p.U0 * this.pgd(y, p.yJet, p.wJet); }
    for (j = 0; j < Ny; j++) this.jetUy[j] -= mean;
    var gr = new Float64Array(Ny), gi = new Float64Array(Ny), sr = new Float64Array(Ny), si = new Float64Array(Ny);
    for (j = 0; j < Ny; j++) { gr[j] = zj[j]; sr[j] = this.pg(j * this.dy, p.yStir, p.wStir); }
    fft1(this.py, gr, gi, 0, 1, -1); fft1(this.py, sr, si, 0, 1, -1);
    this.jetHr = new Float64Array(Ny); this.jetHi = new Float64Array(Ny); this.stHr = new Float64Array(Ny); this.stHi = new Float64Array(Ny);
    for (j = 0; j < Ny; j++) { q = j * Nx; var ok = this.mask[q] || j === 0; this.jetHr[j] = ok && j ? gr[j] * Nx : 0; this.jetHi[j] = ok && j ? gi[j] * Nx : 0; this.stHr[j] = sr[j] * Nx; this.stHi[j] = si[j] * Nx; }
    var ms = []; for (var m = Math.max(1, p.mStir - 1); m <= p.mStir + 1; m++) if (m < Nx / 3) ms.push(m);
    this.stirM = ms; while (this.stirA.length < ms.length) this.stirA.push([this.gauss() / Math.SQRT2, this.gauss() / Math.SQRT2]);
    this.stirA.length = ms.length;
  };
  BP.updateDamping = function () {
    var p = this.p, n = this.Nx * this.Ny, kmax = Math.min(Math.PI / this.dx, Math.PI / this.dy) * 2 / 3;
    var nu = p.hypo / Math.pow(kmax * kmax, 4), mu = p.tauFric > 0 ? 1 / p.tauFric : 0;
    for (var q = 0; q < n; q++) this.E[q] = Math.exp(-this.dt * (mu + nu * Math.pow(this.K2[q], 4)));
  };
  BP.setParams = function (o) { var f = false; for (var k in o) { if (this.p[k] !== o[k]) { this.p[k] = o[k]; f = true; } } if (f) { this.updateForcing(); this.updateDamping(); } };

  /* tendency N(zeta-hat) into (Nr, Ni); also leaves u, v on the grid */
  BP.tendency = function (Nr, Ni) {
    var Nx = this.Nx, Ny = this.Ny, n = Nx * Ny, kx = this.kx, ky = this.ky, K2 = this.K2, zr = this.zr, zi = this.zi;
    var Ar = this.Ar, Ai = this.Ai, Br = this.Br, Bi = this.Bi, Jr = this.Jr, Ji = this.Ji, mask = this.mask, beta = this.p.beta, i, j, q;
    for (j = 0; j < Ny; j++) for (i = 0; i < Nx; i++) {
      q = j * Nx + i; var k = kx[i], l = ky[j];
      if (!mask[q]) { Ar[q] = Ai[q] = Br[q] = Bi[q] = 0; continue; }
      var pr = -zr[q] / K2[q], pi = -zi[q] / K2[q];
      var ur = l * pi, ui = -l * pr, vr = -k * pi, vi = k * pr;        /* u = -dpsi/dy, v = dpsi/dx */
      Ar[q] = ur - vi; Ai[q] = ui + vr;                                   /* u + i v */
      var zxr = -k * zi[q], zxi = k * zr[q], zyr = -l * zi[q], zyi = l * zr[q];
      Br[q] = zxr - zyi; Bi[q] = zxi + zyr;                               /* zeta_x + i zeta_y */
    }
    this.fft2(Ar, Ai, 1); this.fft2(Br, Bi, 1);
    var s = 1 / n, um = 0, u = this.u, v = this.v;
    for (q = 0; q < n; q++) {
      var uu = Ar[q] * s, vv = Ai[q] * s; u[q] = uu; v[q] = vv;
      var sp = uu * uu + vv * vv; if (sp > um) um = sp;
      Jr[q] = uu * Br[q] * s + vv * Bi[q] * s; Ji[q] = 0;
    }
    this.umax = Math.sqrt(um);
    this.fft2(Jr, Ji, -1);
    var p = this.p, tj = p.jetOn && p.tauJet > 0 ? 1 / p.tauJet : 0;
    for (j = 0; j < Ny; j++) for (i = 0; i < Nx; i++) {
      q = j * Nx + i;
      if (!mask[q]) { Nr[q] = Ni[q] = 0; continue; }
      var psr = -zr[q] / K2[q], psi = -zi[q] / K2[q];
      Nr[q] = -Jr[q] + beta * kx[i] * psi; Ni[q] = -Ji[q] - beta * kx[i] * psr;   /* -J - beta v,  v-hat = i k psi-hat */
    }
    if (tj) for (j = 1; j < Ny; j++) { q = j * Nx; if (!mask[q]) continue; Nr[q] += (this.jetHr[j] - zr[q]) * tj; Ni[q] += (this.jetHi[j] - zi[q]) * tj; }
    if (p.stirOn && p.Astir > 0) {
      for (var a = 0; a < this.stirM.length; a++) {
        var m = this.stirM[a], ar = this.stirA[a][0] * p.Astir / 2, ai = this.stirA[a][1] * p.Astir / 2;
        for (j = 0; j < Ny; j++) {
          var gr = this.stHr[j], gi = this.stHi[j];
          q = j * Nx + m; if (mask[q]) { Nr[q] += ar * gr - ai * gi; Ni[q] += ar * gi + ai * gr; }
          q = j * Nx + (Nx - m); if (mask[q]) { Nr[q] += ar * gr + ai * gi; Ni[q] += ar * gi - ai * gr; }   /* conj(a) * G-hat */
        }
      }
    }
  };

  /* mouse forcing: list of {type: 'push'|'vortex', x, y, ux, uy, sign} applied as increments of zeta */
  BP.addImpulses = function (list) { for (var a = 0; a < list.length; a++) this.pending.push(list[a]); };
  BP.applyPending = function () {
    if (!this.pending.length) return;
    var Nx = this.Nx, Ny = this.Ny, n = Nx * Ny, Mr = this.Mr, Mi = this.Mi, Lx = this.Lx, Ly = this.Ly, dx = this.dx, dy = this.dy;
    for (var q = 0; q < n; q++) { Mr[q] = 0; Mi[q] = 0; }
    for (var a = 0; a < this.pending.length; a++) {
      var e = this.pending[a], r0 = e.r || (e.type === 'vortex' ? 0.55 : 0.4), R = 3 * r0;
      var i0 = Math.floor((e.x - R) / dx), i1 = Math.ceil((e.x + R) / dx), j0 = Math.floor((e.y - R) / dy), j1 = Math.ceil((e.y + R) / dy);
      for (var jj = j0; jj <= j1; jj++) for (var ii = i0; ii <= i1; ii++) {
        var X = ii * dx - e.x, Y = jj * dy - e.y, g = Math.exp(-(X * X + Y * Y) / (r0 * r0));
        var qq = (((jj % Ny) + Ny) % Ny) * Nx + (((ii % Nx) + Nx) % Nx);
        if (e.type === 'vortex') Mr[qq] += e.sign * e.z0 * g;
        else Mr[qq] += (-2 / (r0 * r0)) * g * (e.uy * X - e.ux * Y);
      }
    }
    this.pending = [];
    this.fft2(Mr, Mi, -1);
    for (q = 0; q < n; q++) if (this.mask[q]) { this.zr[q] += Mr[q]; this.zi[q] += Mi[q]; }
  };

  BP.stepStir = function (dt) {
    var p = this.p, c = Math.exp(-dt / p.tauStir), s = Math.sqrt((1 - c * c) / 2);
    for (var a = 0; a < this.stirA.length; a++) { this.stirA[a][0] = c * this.stirA[a][0] + s * this.gauss(); this.stirA[a][1] = c * this.stirA[a][1] + s * this.gauss(); }
  };

  BP.step = function () {
    this.applyPending();
    var n = this.Nx * this.Ny, t;
    t = this.N2r; this.N2r = this.N1r; this.N1r = this.N0r; this.N0r = t;
    t = this.N2i; this.N2i = this.N1i; this.N1i = this.N0i; this.N0i = t;
    this.tendency(this.N0r, this.N0i);
    this.cfl = this.umax * this.dt / Math.min(this.dx, this.dy);
    if (this.cfl > 0.7) { this.dt *= 0.5; this.nab = 0; this.updateDamping(); }
    else if (this.cfl < 0.25 && this.dt < this.dt0 && this.nab >= 3) { this.dt = Math.min(this.dt0, this.dt * 2); this.nab = 0; this.updateDamping(); }
    var dt = this.dt, c0, c1, c2;
    if (this.nab === 0) { c0 = 1; c1 = 0; c2 = 0; } else if (this.nab === 1) { c0 = 1.5; c1 = -0.5; c2 = 0; } else { c0 = 23 / 12; c1 = -16 / 12; c2 = 5 / 12; }
    var zr = this.zr, zi = this.zi, E = this.E, a0 = this.N0r, b0 = this.N0i, a1 = this.N1r, b1 = this.N1i, a2 = this.N2r, b2 = this.N2i;
    for (var q = 0; q < n; q++) {
      zr[q] = E[q] * (zr[q] + dt * (c0 * a0[q] + c1 * a1[q] + c2 * a2[q]));
      zi[q] = E[q] * (zi[q] + dt * (c0 * b0[q] + c1 * b1[q] + c2 * b2[q]));
    }
    this.nab = Math.min(3, this.nab + 1);
    this.stepStir(dt);
    this.t += dt;
  };

  /* initial state: the jet (if on) plus random vorticity with rms speed urms (velocity units) peaked at wavenumber kpeak */
  BP.reset = function (urms, kpeak) {
    var Nx = this.Nx, Ny = this.Ny, n = Nx * Ny, zr = this.zr, zi = this.zi, q;
    for (q = 0; q < n; q++) { zr[q] = 0; zi[q] = 0; }
    var amp = urms == null ? 0.1 : urms, kp = kpeak || 3;
    if (amp > 0) {
      var Mr = this.Mr, Mi = this.Mi;
      for (q = 0; q < n; q++) { Mr[q] = this.gauss(); Mi[q] = 0; }
      this.fft2(Mr, Mi, -1);
      for (q = 0; q < n; q++) { var K = Math.sqrt(this.K2[q]), f = this.mask[q] ? Math.exp(-Math.pow((K - kp) / (0.5 * kp), 2)) : 0; zr[q] = Mr[q] * f; zi[q] = Mi[q] * f; }
      var e = this.energy(), c = e > 0 ? Math.sqrt(0.5 * amp * amp / e) : 0;   /* domain-mean kinetic energy = urms^2 / 2 */
      for (q = 0; q < n; q++) { zr[q] *= c; zi[q] *= c; }
    }
    if (this.p.jetOn) for (var j = 1; j < Ny; j++) { q = j * Nx; zr[q] += this.jetHr[j]; zi[q] += this.jetHi[j]; }
    this.t = 0; this.dt = this.dt0; this.nab = 0; this.pending = []; this.updateDamping();
  };

  /* grids for display: zeta and psi (one inverse FFT), plus the last u, v */
  BP.fields = function (zeta, psi) {
    var n = this.Nx * this.Ny, Ar = this.Ar, Ai = this.Ai, zr = this.zr, zi = this.zi, K2 = this.K2, mask = this.mask;
    for (var q = 0; q < n; q++) {
      if (!mask[q]) { Ar[q] = Ai[q] = 0; continue; }
      var pr = -zr[q] / K2[q], pi = -zi[q] / K2[q];
      Ar[q] = zr[q] - pi; Ai[q] = zi[q] + pr;   /* zeta + i psi */
    }
    this.fft2(Ar, Ai, 1);
    var s = 1 / n;
    for (q = 0; q < n; q++) { zeta[q] = Ar[q] * s; psi[q] = Ai[q] * s; }
  };
  /* zonal-mean u(y) from the last tendency evaluation */
  BP.ubar = function (out) {
    var Nx = this.Nx, Ny = this.Ny, u = this.u;
    for (var j = 0; j < Ny; j++) { var s = 0; for (var i = 0; i < Nx; i++) s += u[j * Nx + i]; out[j] = s / Nx; }
  };
  /* kinetic-energy spectrum in shells of width 2 pi / Ly; returns {k, E} (E per unit wavenumber, (velocity unit)^2 * length unit) */
  BP.spectrum = function () {
    var Nx = this.Nx, Ny = this.Ny, n = Nx * Ny, dk = 2 * Math.PI / this.Ly, nb = Math.floor(Math.min(Nx / 3 * 2 * Math.PI / this.Lx, Ny / 3 * dk) / dk);
    var E = new Float64Array(nb + 1), zr = this.zr, zi = this.zi, K2 = this.K2, mask = this.mask, s = 1 / (n * n);
    for (var q = 0; q < n; q++) { if (!mask[q]) continue; var b = Math.round(Math.sqrt(K2[q]) / dk); if (b > nb) continue; E[b] += 0.5 * (zr[q] * zr[q] + zi[q] * zi[q]) / K2[q] * s / dk; }
    var k = []; for (var bb = 0; bb <= nb; bb++) k.push(bb * dk);
    return {k: k, E: Array.from(E)};
  };
  BP.energy = function () {
    var n = this.Nx * this.Ny, zr = this.zr, zi = this.zi, K2 = this.K2, mask = this.mask, e = 0;
    for (var q = 0; q < n; q++) if (mask[q]) e += 0.5 * (zr[q] * zr[q] + zi[q] * zi[q]) / K2[q];
    return e / (n * n);
  };

  root.BetaPlane = BetaPlane;
  if (typeof module !== 'undefined' && module.exports) module.exports = {BetaPlane: BetaPlane, makePlan: makePlan, fft1: fft1};
})(typeof self !== 'undefined' ? self : this);
