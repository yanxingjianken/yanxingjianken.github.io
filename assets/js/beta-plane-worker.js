/* Web Worker running the beta-plane model (assets/js/beta-plane-solver.js) and sending display fields.
 * Messages in:  {cmd: 'init', Nx, Ny, params}  {cmd: 'params', params}  {cmd: 'run', on}  {cmd: 'reset', urms, kpeak}
 *               {cmd: 'impulse', list}  {cmd: 'frame', hovY}  {cmd: 'speed', daysPerSec}
 * Messages out: {type: 'frame', t, Nx, Ny, zeta, psi, u, v, ubar, ujet, hov (row of psi or null), spec (every ~0.5 day), dt, cfl}
 */
'use strict';
importScripts('beta-plane-solver.js' + self.location.search);
var bp = null, running = true, speed = 1.5, lastWall = 0, hovNext = 0, specNext = 0, HOV_DT = 0.25;

var target = null;
function advance() {
  if (!bp || !running) return;
  var now = Date.now(), wall = lastWall ? Math.min(0.1, (now - lastWall) / 1000) : 0.03; lastWall = now;
  if (target === null || target < bp.t) target = bp.t;
  target = Math.min(target + speed * wall, bp.t + 0.5);   /* model time owed; capped so a slow device does not pile up a backlog */
  var t0 = Date.now();
  while (bp.t + 0.5 * bp.dt < target && Date.now() - t0 < 40) {
    bp.step();
    if (!isFinite(bp.zr[1])) { postMessage({type: 'blowup', t: bp.t}); bp.reset(); break; }
  }
}
setInterval(advance, 15);

self.onmessage = function (ev) {
  var m = ev.data;
  if (m.cmd === 'init') { bp = new self.BetaPlane({Nx: m.Nx, Ny: m.Ny, params: m.params}); bp.reset(); hovNext = 0; specNext = 0; lastWall = 0; target = null; }
  else if (!bp) return;
  else if (m.cmd === 'params') bp.setParams(m.params);
  else if (m.cmd === 'run') { running = !!m.on; lastWall = 0; target = null; }
  else if (m.cmd === 'speed') speed = m.daysPerSec;
  else if (m.cmd === 'reset') { bp.reset(m.urms, m.kpeak); hovNext = 0; specNext = 0; lastWall = 0; target = null; }
  else if (m.cmd === 'impulse') bp.addImpulses(m.list);
  else if (m.cmd === 'frame') {
    var n = bp.Nx * bp.Ny, zeta = new Float32Array(n), psi = new Float32Array(n), ub = new Float32Array(bp.Ny);
    bp.fields(zeta, psi); bp.ubar(ub);
    var out = {type: 'frame', t: bp.t, Nx: bp.Nx, Ny: bp.Ny, Lx: bp.Lx, Ly: bp.Ly, zeta: zeta, psi: psi, u: new Float32Array(bp.u), v: new Float32Array(bp.v),
               ubar: ub, ujet: Float32Array.from(bp.jetUy), dt: bp.dt, cfl: bp.cfl, hov: null, spec: null};
    if (bp.t >= hovNext) {   /* psi minus its zonal mean along the Hovmoller latitude row */
      var j = Math.max(0, Math.min(bp.Ny - 1, Math.round(m.hovY / bp.dy))), row = new Float32Array(bp.Nx), s = 0, i;
      for (i = 0; i < bp.Nx; i++) { row[i] = psi[j * bp.Nx + i]; s += row[i]; }
      for (i = 0; i < bp.Nx; i++) row[i] -= s / bp.Nx;
      out.hov = {t: bp.t, row: row}; hovNext = bp.t + HOV_DT;
    }
    if (bp.t >= specNext) { out.spec = bp.spectrum(); specNext = bp.t + 0.5; }
    postMessage(out, [zeta.buffer, psi.buffer, out.u.buffer, out.v.buffer, ub.buffer, out.ujet.buffer]);
  }
};
