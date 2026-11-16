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

  // Phones: lock the hero height to the first screen size so it doesn't jump while Safari's toolbars resize
  var lastW = window.innerWidth;
  function setHeroH(force) {
    if (force || window.innerWidth !== lastW) {
      lastW = window.innerWidth;
      document.documentElement.style.setProperty("--hero-h", window.innerHeight + "px");
    }
  }
  setHeroH(true);
  window.addEventListener("resize", function () { setHeroH(false); });
  window.addEventListener("orientationchange", function () { setTimeout(function () { setHeroH(true); }, 300); });

  // Slope story: a small real-3D scene on a canvas. Machine, vines and grapes are 3D objects;
  // the ground tilts to 75 %, returns to flat, then the camera orbits 90° while terraces rise.
  var slope = document.querySelector("[data-slope]");
  if (slope) {
    var cv = slope.querySelector("[data-scene]"), g = cv.getContext("2d"),
        sn = slope.querySelector("[data-slope-num]"), sl = slope.querySelector("[data-slope-label]"),
        readEl = slope.querySelector(".slope-read"), labels = slope.getAttribute("data-labels").split("|");
    var ramp = function (p, a, b) { var k = Math.min(1, Math.max(0, (p - a) / (b - a))); return k * k * (3 - 2 * k); };
        var LOGO = [[[-2.58,97.12],[-2.7,97.01],[-3.38,97.01],[-3.49,96.89],[-3.95,96.89],[-4.06,96.78],[-4.86,96.67],[-4.97,96.55],[-6.22,96.21],[-6.56,95.98],[-6.79,95.98],[-8.38,95.19],[-10.66,93.6],[-12.82,91.32],[-14.52,88.59],[-14.52,88.37],[-14.98,87.57],[-14.98,87.34],[-15.43,86.21],[-15.43,85.87],[-15.55,85.75],[-15.55,85.41],[-15.77,84.84],[-15.77,84.27],[-15.89,84.16],[-15.89,83.25],[-16.0,83.14],[-16.0,80.64],[-15.89,80.52],[-15.89,79.61],[-15.77,79.5],[-15.66,78.48],[-15.55,78.36],[-15.55,78.02],[-15.43,77.91],[-15.43,77.57],[-15.32,77.45],[-15.09,76.54],[-13.95,74.16],[-13.73,73.93],[-13.16,72.9],[-12.13,71.77],[-12.13,71.65],[-10.2,69.83],[-8.16,68.47],[-7.02,67.9],[-6.79,67.9],[-6.45,67.67],[-6.22,67.67],[-5.88,67.45],[-5.65,67.45],[-5.2,67.22],[-4.86,67.22],[-4.74,67.11],[-4.4,67.11],[-3.83,66.88],[-3.38,66.88],[-3.27,66.76],[-2.58,66.76],[-2.47,66.65],[1.05,66.65],[1.17,66.76],[2.42,66.88],[2.53,66.99],[2.87,66.99],[2.99,67.11],[3.33,67.11],[3.44,67.22],[3.78,67.22],[3.9,67.33],[4.47,67.45],[4.81,67.67],[5.03,67.67],[5.6,68.02],[5.83,68.02],[6.51,68.36],[6.74,68.58],[7.31,68.81],[8.9,69.95],[9.58,70.63],[9.7,70.63],[11.17,72.22],[12.31,73.81],[13.22,75.63],[6.85,75.63],[5.37,74.16],[4.24,73.36],[2.87,72.68],[2.65,72.68],[1.85,72.34],[0.83,72.22],[0.71,72.11],[-0.31,72.11],[-0.42,71.99],[-2.13,72.11],[-2.24,72.22],[-2.81,72.22],[-2.93,72.34],[-3.27,72.34],[-3.38,72.45],[-4.29,72.68],[-5.65,73.36],[-7.47,74.72],[-8.84,76.32],[-9.86,78.13],[-9.86,78.36],[-10.2,79.16],[-10.32,79.95],[-10.43,80.07],[-10.43,80.64],[-10.54,80.75],[-10.54,83.02],[-10.43,83.14],[-10.32,84.27],[-10.2,84.39],[-9.86,85.64],[-9.29,86.78],[-8.16,88.37],[-7.13,89.39],[-5.88,90.3],[-4.86,90.87],[-4.63,90.87],[-3.72,91.32],[-3.38,91.32],[-2.81,91.55],[-2.36,91.55],[-2.24,91.66],[-1.45,91.66],[-1.33,91.78],[0.83,91.66],[0.94,91.55],[1.85,91.44],[1.96,91.32],[2.87,91.1],[3.21,90.87],[3.44,90.87],[5.26,89.73],[5.83,89.16],[5.94,89.16],[6.63,88.37],[13.11,88.37],[13.11,88.48],[11.97,90.53],[10.72,92.01],[10.72,92.12],[8.79,93.94],[6.97,95.19],[4.81,96.21],[4.58,96.21],[3.44,96.67],[2.65,96.78],[2.53,96.89],[1.28,97.01],[1.17,97.12],[-0.2,97.12],[-0.31,97.24]],[[22.54,97.35],[22.54,84.84],[22.43,84.73],[6.51,84.73],[6.4,84.61],[6.4,79.73],[22.43,79.73],[22.54,79.61],[22.54,66.76],[28.0,66.76],[28.0,97.35]]];
var BG = "#17191b", WH = "#ffffff", R = 25, H = 150, D = 2200;

    // ---- model -------------------------------------------------------------
    var machine = [], vineT = [], grapeT = [];
    function box(out, x0, x1, y0, y1, z0, z1, fill) {
      var p = [[x0,y0,z0],[x1,y0,z0],[x1,y1,z0],[x0,y1,z0],[x0,y0,z1],[x1,y0,z1],[x1,y1,z1],[x0,y1,z1]];
      [[4,5,6,7],[1,0,3,2],[5,1,2,6],[0,4,7,3],[7,6,2,3],[0,1,5,4]].forEach(function (f) {
        out.push({ t: "f", p: f.map(function (i) { return p[i]; }), fill: fill || BG, stroke: WH, cull: 1 });
      });
    }
    // prism: a side profile (x,y – counter-clockwise seen from the valley side) extruded across the machine
    // round the corners of a profile; returns points flagged soft where they belong to a corner arc
    function roundPf(pf, r) {
      var out = [], n = pf.length, j, k;
      for (j = 0; j < n; j++) {
        var A = pf[(j + n - 1) % n], B = pf[j], C = pf[(j + 1) % n],
            la = Math.hypot(A[0] - B[0], A[1] - B[1]), lc = Math.hypot(C[0] - B[0], C[1] - B[1]),
            d = Math.min(r, la * 0.45, lc * 0.45),
            p1 = [B[0] + (A[0] - B[0]) / la * d, B[1] + (A[1] - B[1]) / la * d],
            p2 = [B[0] + (C[0] - B[0]) / lc * d, B[1] + (C[1] - B[1]) / lc * d];
        for (k = 0; k <= 5; k++) {
          var u = k / 5, a = (1 - u) * (1 - u), b = 2 * u * (1 - u), c = u * u;
          out.push([a * p1[0] + b * B[0] + c * p2[0], a * p1[1] + b * B[1] + c * p2[1], k < 5]);
        }
      }
      return out;
    }
    function prism(out, pf0, z0, z1, fill, r) {
      var pf = roundPf(pf0, r === undefined ? 7 : r), n = pf.length, j;
      out.push({ t: "f", p: pf.map(function (q) { return [q[0], q[1], z1]; }), fill: fill || BG, stroke: WH, cull: 1 });
      out.push({ t: "f", p: pf.slice().reverse().map(function (q) { return [q[0], q[1], z0]; }), fill: fill || BG, stroke: WH, cull: 1 });
      for (j = 0; j < n; j++) {
        var u = pf[j], v = pf[(j + 1) % n];
        out.push({ t: "f", p: [[u[0],u[1],z0],[v[0],v[1],z0],[v[0],v[1],z1],[u[0],u[1],z1]], fill: fill || BG, stroke: WH, cull: 1, soft: u[2] });
      }
    }
    function rbox(out, x0, x1, y0, y1, z0, z1, r) { prism(out, [[x0,y0],[x1,y0],[x1,y1],[x0,y1]], z0, z1, null, r); }
    var trackPf = [[-25,0],[100,0],[112,8],[112,20],[100,28],[-25,28],[-37,20],[-37,8]];
    var trPts = roundPf(trackPf, 9), trLen = [0], trL, trN;
    trPts.forEach(function (q, n) { var w = trPts[(n + 1) % trPts.length]; trLen.push(trLen[n] + Math.hypot(w[0] - q[0], w[1] - q[1])); });
    trL = trLen[trLen.length - 1]; trN = Math.round(trL / 11);
    prism(machine, trackPf, -75, -55, null, 9);
    var nt = machine.length; prism(machine, trackPf, -25, -5, null, 9);
    for (; nt < machine.length; nt++) machine[nt].bias = 12;                                     // near track sits in front of the body                       // crawler tracks, rounded ends
    // silhouette after the MSH side drawing: cab with raked front, engine section, column, tall harvesting head
    var bodyPf = [[151,151],[78,151],[52,85],[45,85],[45,107],[-8,107],[-8,23],[100,23],[118,16],[159,59],[159,77],[144,90],[159,140]];
    prism(machine, bodyPf, -72, -8, null, 7);                                                      // body and cab, one piece
    box(machine, 36, 40, 107, 150, -20, -16);                                                      // exhaust
    box(machine, -34, -9, 40, 114, -14, -2);                                                       // conveyor column
    machine.push({ t: "l", p: [[-15,44,-1.9],[-15,110,-1.9]], lw: 1.2, bias: 25 }, { t: "l", p: [[-22,44,-1.9],[-22,110,-1.9]], lw: 1.2, bias: 25 });
    var headPf = [[-135,26],[-126,18],[-35,18],[-35,124],[-135,124]];
    prism(machine, headPf, R - 30, R - 13, null, 8); prism(machine, headPf, R + 13, R + 30, null, 8);  // harvesting head, either side of the row
    prism(machine, [[-135,124],[-35,124],[-35,126],[-14,126],[-3,119],[-3,114],[26,114],[26,154],[-135,154]], R - 32, R + 32, null, 6);  // head top, reaching over the column
    machine.push({ t: "f", p: roundPf([[64,96],[138,96],[150,136],[146,144],[83,144]], 6).map(function (q) { return [q[0], q[1], -7.5]; }), fill: "#2e3033", stroke: WH, bias: 20, glass: 1 });
    machine.push({ t: "f", p: [[-126,18,R-13],[-35,18,R-13],[-35,12,R-2],[-126,12,R-2]], fill: "#6b4a3a", stroke: WH });
    machine.push({ t: "f", p: [[-126,18,R+13],[-35,18,R+13],[-35,12,R+2],[-126,12,R+2]], fill: "#6b4a3a", stroke: WH });
    var i, k;
    // CH mark, traced from the company logo (C and H as filled shapes on the engine section)
    LOGO.forEach(function (pf) { machine.push({ t: "f", p: pf.map(function (q) { return [18 + (q[0] - 6) * 0.8, 72 + (q[1] - 82) * 0.8, -7.5]; }), fill: WH, stroke: WH, lw: 0.5, bias: 25 }); });
    for (i = 0; i < 3; i++) {                                                                  // hoses down the outside of the head
      var hs = [];
      for (k = 0; k <= 10; k++) hs.push([-66 - i * 9 - 34 * Math.pow(k / 10, 1.6), 150 - 118 * (k / 10), R + 31 + 5 * Math.sin(Math.PI * k / 10)]);
      machine.push({ t: "l", p: hs, lw: 3.5, bias: 28 });
    }
    for (i = 0; i < 5; i++) {
      machine.push({ t: "l", p: [[-118, 110 - i * 20, R - 13], [-118, 105 - i * 20, R - 7], [-118, 107 - i * 20, R - 2]], lw: 1.4 });
      machine.push({ t: "l", p: [[-118, 100 - i * 20, R + 13], [-118, 95 - i * 20, R + 7], [-118, 97 - i * 20, R + 2]], lw: 1.4 });
    }
    var hose = [];
    for (i = 0; i <= 16; i++) { k = i / 16; hose.push([-90 + 110 * k, 154 + 40 * Math.sin(Math.PI * k) - 47 * k, R - (R + 40) * k]); }
    machine.push({ t: "l", p: hose, lw: 4.5, bias: 10 });
    machine.push({ t: "c", p: [[-18, 14, -4.5]], r: 9, stroke: WH, bias: 25 }, { t: "c", p: [[94, 14, -4.5]], r: 9, stroke: WH, bias: 25 });

    // one vine: stem, leaves, two grape clusters (relative to its foot)
    vineT.push({ t: "l", p: [[0,0,0],[0,92,0]], lw: 1.2, col: "rgba(255,255,255,.45)" });
    [[-9,24,3],[9,33,-3],[-10,44,-4],[10,54,4],[-9,64,3],[9,74,-3],[-4,85,2]].forEach(function (c, n) {
      var s = n % 2 ? 1 : -1;
      vineT.push({ t: "f", p: [[c[0]-8,c[1]-3*s,c[2]],[c[0],c[1]+4.5,c[2]+2.5*s],[c[0]+8,c[1]+3*s,c[2]],[c[0],c[1]-4.5,c[2]-2.5*s]], fill: "#3a4630", stroke: "#9dbb6a", lw: 1 });
    });
    [[-7,44,5],[8,26,-5]].forEach(function (c) {
      [[-5,0,0],[0,0,2],[5,0,0],[-2.5,-4.6,1],[2.5,-4.6,-1],[0,-9.2,0]].forEach(function (o) {
        grapeT.push({ t: "c", p: [[c[0]+o[0],c[1]+o[1],c[2]+o[2]]], r: 3, fill: "#d8c66e" });
      });
    });
    var rows = [{ z: R, lvl: 0, lane: 1 }, { z: R - 180, lvl: 1 }, { z: R + 180, lvl: -1 }];
    var XA = -1000, XB = 2600, zs = [-1500, -290, -110, 70, 250, 700];

    // ---- render ------------------------------------------------------------
    var curP = 0, curPh = 0, photo = slope.querySelector("[data-slope-photo]");
    function render(p, ts) {
      var dpr = Math.min(2, window.devicePixelRatio || 1), w = cv.clientWidth, h = cv.clientHeight;
      if (!w || !h) return;
      if (cv.width !== Math.round(w * dpr) || cv.height !== Math.round(h * dpr)) { cv.width = Math.round(w * dpr); cv.height = Math.round(h * dpr); }
      g.setTransform(dpr, 0, 0, dpr, 0, 0); g.clearRect(0, 0, w, h); g.lineJoin = "round"; g.lineCap = "round";
      var pct = 75 * (ramp(p, 0.03, 0.27) - ramp(p, 0.33, 0.5)), t = ramp(p, 0.56, 0.8), hh = ramp(p, 0.52, 0.74);
      var a = Math.atan(pct / 100), ca = Math.cos(a), sa = Math.sin(a), psi = t * Math.PI / 2, cy = Math.cos(psi), sy = Math.sin(psi),
          phi = (5 + 7 * t) * Math.PI / 180, cp = Math.cos(phi), sp = Math.sin(phi);
      var S = Math.min(h / 560, w / 430), CX = w * 0.5 - (w > 900 ? w * 0.04 * (1 - t) : 0), CY = h * 0.5;
      var off = (ts / 1000 * 34) % 80, toff = 0;
      // final approach: the camera settles where the machine stands in the photo (2000 × 1333, object-fit: cover)
      var q = ramp(p, 0.82, 0.97);
      if (q > 0) {
        var S0 = S, CX0 = CX, CY0 = CY; S = 1; CX = 0; CY = 0;
        var gb = P(-40, 0, -9, 0), gt = P(-40, 140, -9, 0), isc = Math.max(w / 2000, h / 1333),
            St = 370 * isc / (gb[1] - gt[1]), gx = (w - 2000 * isc) / 2 + 1040 * isc, gy = (h - 1333 * isc) / 2 + 919 * isc;
        S = S0 + (St - S0) * q; CX = CX0 + (gx - St * gb[0] - CX0) * q; CY = CY0 + (gy - St * gb[1] - CY0) * q;
      }
      function P(x, y, z, lvl) {
        y += (lvl || 0) * H * hh;
        var x1 = x * ca - y * sa, y1 = x * sa + y * ca - 55;
        var x2 = x1 * cy + z * sy, z2 = -x1 * sy + z * cy;
        var y3 = y1 * cp - z2 * sp, z3 = y1 * sp + z2 * cp, dz = D - z3;
        if (dz < 260) return null;
        var f = D / dz;
        return [CX + x2 * f * S, CY - y3 * f * S, z3, f];
      }
      var prims = [];
      function add(pr, ox, oz, lvl, alpha) {
        var q = [], d = 0, n = pr.p.length, j, pt;
        for (j = 0; j < n; j++) { pt = P(pr.p[j][0] + ox, pr.p[j][1], pr.p[j][2] + oz, pr.p[j][3] !== undefined ? pr.p[j][3] : lvl); if (!pt) return; q.push(pt); d += pt[2]; }
        if (pr.cull) { var ar = 0; for (j = 0; j < n; j++) { var u = q[j], v = q[(j + 1) % n]; ar += u[0] * v[1] - v[0] * u[1]; } if (ar >= 0) return; }
        prims.push({ pr: pr, q: q, d: d / n + (pr.bias || 0), a: alpha });
      }
      function draw(list) {
        list.sort(function (m, n) { return m.d - n.d; });
        list.forEach(function (o) {
          var pr = o.pr, q = o.q, j;
          g.globalAlpha = o.a;
          if (pr.t === "c") {
            g.beginPath(); g.arc(q[0][0], q[0][1], pr.r * q[0][3] * S, 0, 6.2832);
            if (pr.fill) { g.fillStyle = pr.fill; g.fill(); } if (pr.stroke) { g.strokeStyle = pr.stroke; g.lineWidth = 1.5; g.stroke(); }
            return;
          }
          g.beginPath(); g.moveTo(q[0][0], q[0][1]); for (j = 1; j < q.length; j++) g.lineTo(q[j][0], q[j][1]);
          if (pr.t === "f" && pr.soft) {
            g.closePath(); g.fillStyle = pr.fill; g.fill(); g.strokeStyle = pr.fill; g.lineWidth = 0.6; g.stroke();
            g.beginPath(); g.moveTo(q[0][0], q[0][1]); g.lineTo(q[1][0], q[1][1]); g.moveTo(q[2][0], q[2][1]); g.lineTo(q[3][0], q[3][1]);
            g.strokeStyle = pr.stroke; g.lineWidth = 1.5; g.stroke();
          }
          else if (pr.t === "f" && pr.glass) {
            // tinted glass: soft gradient, two diagonal reflections, thin bright rim
            var x0 = 1e9, y0 = 1e9, x1 = -1e9, y1 = -1e9;
            q.forEach(function (v) { x0 = Math.min(x0, v[0]); y0 = Math.min(y0, v[1]); x1 = Math.max(x1, v[0]); y1 = Math.max(y1, v[1]); });
            var gw = x1 - x0, gh = y1 - y0, gr = g.createLinearGradient(x0, y0, x1, y1);
            gr.addColorStop(0, "#4a4f55"); gr.addColorStop(0.45, "#2c2f33"); gr.addColorStop(1, "#1d1f22");
            g.closePath(); g.save(); g.fillStyle = gr; g.fill(); g.clip();
            g.fillStyle = "rgba(255,255,255,.13)";
            g.beginPath(); g.moveTo(x0 + gw * .18, y1); g.lineTo(x0 + gw * .42, y1); g.lineTo(x0 + gw * .82, y0); g.lineTo(x0 + gw * .58, y0); g.fill();
            g.fillStyle = "rgba(255,255,255,.07)";
            g.beginPath(); g.moveTo(x0 + gw * .5, y1); g.lineTo(x0 + gw * .58, y1); g.lineTo(x0 + gw * .98, y0); g.lineTo(x0 + gw * .9, y0); g.fill();
            g.restore();
            g.beginPath(); g.moveTo(q[0][0], q[0][1]); for (j = 1; j < q.length; j++) g.lineTo(q[j][0], q[j][1]); g.closePath();
            g.strokeStyle = "rgba(255,255,255,.85)"; g.lineWidth = 1.2; g.stroke();
          }
          else if (pr.t === "f") { g.closePath(); g.fillStyle = pr.fill; g.fill(); g.strokeStyle = pr.stroke; g.lineWidth = pr.lw || 1.5; g.stroke(); }
          else { g.strokeStyle = pr.col || WH; g.lineWidth = pr.lw || 1.5; g.stroke(); }
        });
      }
      // ground: terraces (flat while hh = 0)
      var j, lv;
      for (j = 0; j < 5; j++) {
        lv = 2 - j;
        add({ t: "f", p: [[XA,0,zs[j]],[XB,0,zs[j]],[XB,0,zs[j+1]],[XA,0,zs[j+1]]], fill: "#222426", stroke: "rgba(255,255,255," + (j === 2 ? 0.55 : 0.22) + ")", lw: 1 }, 0, 0, lv, 1);
        if (j < 4) add({ t: "f", p: [[XA,0,zs[j+1],lv-1],[XB,0,zs[j+1],lv-1],[XB,0,zs[j+1],lv],[XA,0,zs[j+1],lv]], fill: "#1c1e20", stroke: "rgba(255,255,255,.4)", lw: 1 }, 0, 0, 0, 1);
      }
      draw(prims); prims = [];
      // vines and grapes
      rows.forEach(function (rw) {
        var al = rw.lane ? 1 : hh; if (al < 0.03) return;
        add({ t: "l", p: [[XA,40,0],[1500,40,0]], lw: 1, col: "rgba(255,255,255,.3)" }, 0, rw.z, rw.lvl, al);
        add({ t: "l", p: [[XA,78,0],[1500,78,0]], lw: 1, col: "rgba(255,255,255,.3)" }, 0, rw.z, rw.lvl, al);
        for (var n = 0; n < 31; n++) {
          var vx = -960 + n * 80 + off, m;
          for (m = 0; m < vineT.length; m++) add(vineT[m], vx, rw.z, rw.lvl, al);
          if (!rw.lane || vx < -140) for (m = 0; m < grapeT.length; m++) add(grapeT[m], vx, rw.z, rw.lvl, al);
        }
      });
      // machine + moving track tread
      machine.forEach(function (pr) { add(pr, 0, 0, 0, 1); });
      // cleats run round the track outline: across the tread, plus short marks on the valley-side face
      var facing = function (nx, ny, nz) {
        var x1 = nx * ca - ny * sa, y1 = nx * sa + ny * ca, z2 = -x1 * sy + nz * cy;
        return y1 * sp + z2 * cp > 0.03;
      };
      var sideOn = facing(0, 0, 1), run = ts / 1000 * 34;
      for (j = 0; j < trN; j++) {
        var sdist = (j * trL / trN + run) % trL, e = 0;
        while (e < trLen.length - 1 && trLen[e + 1] <= sdist) e++;
        var A = trPts[e], B = trPts[(e + 1) % trPts.length], segL = trLen[e + 1] - trLen[e], u = (sdist - trLen[e]) / segL,
            px = A[0] + (B[0] - A[0]) * u, py = A[1] + (B[1] - A[1]) * u, nx = (B[1] - A[1]) / segL, ny = -(B[0] - A[0]) / segL;
        if (sideOn) add({ t: "l", p: [[px, py, -4.6], [px - nx * 6, py - ny * 6, -4.6]], lw: 1.2, bias: 16 }, 0, 0, 0, 1);
        if (facing(nx, ny, 0) && !(ny > 0.9 && px > -30)) {
          add({ t: "l", p: [[px + nx * 0.4, py + ny * 0.4, -25], [px + nx * 0.4, py + ny * 0.4, -5]], lw: 1.2, bias: 16 }, 0, 0, 0, 1);
          add({ t: "l", p: [[px + nx * 0.4, py + ny * 0.4, -75], [px + nx * 0.4, py + ny * 0.4, -55]], lw: 1.2, bias: 2 }, 0, 0, 0, 1);
        }
      }
      draw(prims); g.globalAlpha = 1;
      // readout
      readEl.style.opacity = Math.min(1, Math.abs(2 * t - 1) * 1.6).toFixed(3);
      if (t < 0.5) { sn.textContent = Math.round(pct) + " %"; sl.textContent = labels[pct < 20 ? 0 : pct < 55 ? 1 : 2]; }
      else { sn.textContent = "1"; sl.textContent = labels[3]; }
    }
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
      slope.classList.add("is-static"); render(0.9, 0);
      window.addEventListener("resize", function () { render(0.9, 0); });
    } else {
      var onSlope = function () {
        // the last stretch of the section is the dissolve from the drawn scene into the photo
        var r = slope.getBoundingClientRect(), vh = window.innerHeight, span = r.height - vh, sc = -r.top, scene = span - vh * 0.9;
        curP = scene > 0 ? Math.min(1, Math.max(0, sc / scene)) : 1;
        curPh = ramp(sc, scene - vh * 0.15, scene + vh * 0.5);
        if (photo) { photo.style.setProperty("--ph", curPh.toFixed(3)); photo.style.setProperty("--pt", ramp(sc, scene + vh * 0.3, scene + vh * 0.65).toFixed(3)); }
      };
      var loop = function (ts) {
        var r = slope.getBoundingClientRect();
        if (r.bottom > 0 && r.top < window.innerHeight && curPh < 1) render(curP, ts);
        requestAnimationFrame(loop);
      };
      window.addEventListener("scroll", onSlope, { passive: true }); window.addEventListener("resize", onSlope);
      onSlope(); requestAnimationFrame(loop);
    }
  }

  // Photo that opens to full width as it scrolls into view
  var ex = document.querySelector("[data-expand]");
  if (ex) {
    var frame = ex.querySelector(".expand-frame");
    var onEx = function () {
      var r = frame.getBoundingClientRect(), vh = window.innerHeight;
      var k = Math.min(1, Math.max(0, (vh - r.top) / (vh * 1.05)));
      frame.style.setProperty("--k", (k * k * (3 - 2 * k)).toFixed(3));
    };
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) frame.style.setProperty("--k", 1);
    else { window.addEventListener("scroll", onEx, { passive: true }); window.addEventListener("resize", onEx); onEx(); }
  }

  // Home hero dims towards the dark scene as you scroll away from it
  var heroHome = document.querySelector(".hero-home");
  if (heroHome && document.querySelector("[data-slope]")) {
    var dimHero = function () {
      var k = Math.min(1, Math.max(0, window.scrollY / (heroHome.offsetHeight * 0.85)));
      heroHome.style.setProperty("--dim", (k * k * (3 - 2 * k)).toFixed(3));
    };
    window.addEventListener("scroll", dimHero, { passive: true }); dimHero();
  }

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
  var marks = document.querySelectorAll(".worldmap .mk.has-story");
  function showStory(id) {
    document.querySelectorAll(".worldmap .story").forEach(function (st) { st.hidden = st.getAttribute("data-story") !== id; });
    document.querySelectorAll(".worldmap .mk, .worldmap .rg").forEach(function (m) { m.classList.toggle("active", m.getAttribute("data-loc") === id); });
  }
  marks.forEach(function (m) {
    var id = m.getAttribute("data-loc");
    m.addEventListener("click", function () { showStory(id); });
    m.addEventListener("keydown", function (ev) { if (ev.key === "Enter" || ev.key === " ") { ev.preventDefault(); showStory(id); } });
  });
  // region list <-> map markers: hovering either highlights both; entries with a story open it
  document.querySelectorAll(".worldmap [data-loc]").forEach(function (el) {
    var id = el.getAttribute("data-loc");
    var hl = function (on) { document.querySelectorAll('.worldmap [data-loc="' + id + '"]').forEach(function (x) { x.classList.toggle("hl", on); }); };
    el.addEventListener("mouseenter", function () { hl(true); }); el.addEventListener("mouseleave", function () { hl(false); });
    el.addEventListener("focus", function () { hl(true); }); el.addEventListener("blur", function () { hl(false); });
    if (el.classList.contains("rg") && el.classList.contains("has-story")) el.addEventListener("click", function () { showStory(id); });
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
