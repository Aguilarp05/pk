/* Modo Disney: se activa al encontrar los 6 Hidden Mickeys (o escribiendo "disney"); Esc lo quita.
   Trae un fondo con el castillo, las linternas de Enredados, la casa de Up y las esferas de
   memoria de Intensamente, colores y letras de cuento, y cambia el desfile por personajes de Disney. */
(function () {
    var root = document.documentElement;
    var page = document.querySelector(".page");
    var runners = document.querySelector(".runners");
    if (!page) return;

    var PALETTE = { "--card": "#fbfaff", "--ink": "#1d1b3a", "--muted": "#5f5a8a", "--line": "#e3def5", "--accent": "#3f6ad8", "--accent-soft": "#dfe6fb" };
    var link = document.createElement("link");
    link.rel = "stylesheet";
    link.href = "https://fonts.googleapis.com/css2?family=Cinzel+Decorative:wght@700&family=Nunito:wght@400;600;700&display=swap";
    document.head.appendChild(link);

    // ---------------- escena de fondo (1600 x 900, se recorta para llenar la pantalla) ----------------
    function rnd(seed) { return function () { seed = (seed * 16807) % 2147483647; return (seed - 1) / 2147483646; }; }
    var r = rnd(25);
    function stars(n) {
        var out = "";
        for (var i = 0; i < n; i++) {
            out += '<circle cx="' + (r() * 1600).toFixed(0) + '" cy="' + (r() * 620).toFixed(0) + '" r="' + (0.6 + r() * 1.6).toFixed(1) + '" fill="#fff" opacity="' + (0.3 + r() * 0.7).toFixed(2) + '"/>';
        }
        return out;
    }
    function burst(x, y, rad, colors, delay) {
        var s = '<g class="firework-burst" style="animation-delay:' + delay + 's"><g transform="translate(' + x + ' ' + y + ')">';
        for (var i = 0; i < 16; i++) {
            var a = i * Math.PI / 8, c = colors[i % colors.length];
            s += '<line x1="' + (Math.cos(a) * rad * .25).toFixed(1) + '" y1="' + (Math.sin(a) * rad * .25).toFixed(1) + '" x2="' + (Math.cos(a) * rad).toFixed(1) + '" y2="' + (Math.sin(a) * rad).toFixed(1) + '" stroke="' + c + '" stroke-width="2.4" stroke-linecap="round"/>';
            s += '<circle cx="' + (Math.cos(a) * rad * 1.12).toFixed(1) + '" cy="' + (Math.sin(a) * rad * 1.12).toFixed(1) + '" r="3" fill="' + c + '"/>';
        }
        return s + '</g></g>';
    }
    function tower(x, w, top, base, roof) {
        return '<rect x="' + x + '" y="' + top + '" width="' + w + '" height="' + (base - top) + '" fill="#e9e6f7"/>' +
            '<path d="M' + (x - 6) + ' ' + top + ' L' + (x + w / 2) + ' ' + (top - roof) + ' L' + (x + w + 6) + ' ' + top + 'Z" fill="#5a7bd8"/>' +
            '<path d="M' + (x + w / 2) + ' ' + (top - roof) + ' V' + (top - roof - 22) + ' l14 5 l-14 5" fill="#f2b823" stroke="#f2b823" stroke-width="1.5"/>' +
            '<rect x="' + (x + w / 2 - 4) + '" y="' + (top + 18) + '" width="8" height="14" rx="4" fill="#ffd98a"/>';
    }
    var castle = '<g>' +
        tower(60, 44, 520, 760, 70) + tower(330, 44, 520, 760, 70) +
        tower(120, 56, 430, 760, 90) + tower(260, 56, 430, 760, 90) +
        tower(186, 64, 330, 760, 120) +
        '<rect x="90" y="600" width="280" height="160" fill="#e9e6f7"/>' +
        '<path d="M205 760 v-60 a25 25 0 0 1 50 0 v60Z" fill="#3a3f7a"/>' +
        [110, 150, 290, 330].map(function (x) { return '<rect x="' + x + '" y="640" width="12" height="20" rx="6" fill="#ffd98a"/>'; }).join("") +
        '<path d="M90 600 ' + Array.apply(null, Array(14)).map(function (_, i) { return "h10 v-10 h10 v10"; }).join(" ") + '" fill="#e9e6f7"/>' +
        '</g>';
    // estantes de recuerdos de Intensamente
    var ORB = ["#ffd23f", "#4a8cff", "#ef4444", "#a26bff", "#4cc36b", "#ff8a2b", "#2fd4c4", "#ff6fa8", "#4b4aa8"];
    var shelves = "";
    for (var row = 0; row < 3; row++) {
        var y = 420 + row * 90;
        shelves += '<rect x="1230" y="' + (y + 22) + '" width="330" height="8" rx="3" fill="#8a6bd1" opacity=".8"/>';
        for (var k = 0; k < 9; k++) {
            var c = ORB[Math.floor(r() * ORB.length)];
            shelves += '<circle cx="' + (1250 + k * 36) + '" cy="' + y + '" r="14" fill="' + c + '" opacity=".95"/>' +
                '<circle cx="' + (1245 + k * 36) + '" cy="' + (y - 5) + '" r="4" fill="#fff" opacity=".7"/>' +
                '<circle cx="' + (1250 + k * 36) + '" cy="' + y + '" r="22" fill="' + c + '" opacity=".15"/>';
        }
    }
    var reflection = '<g transform="translate(0 1520) scale(1 -1)" opacity=".18">' + castle + '</g>';
    var boat = '<g transform="translate(1320 800)"><path d="M0 0 H110 L92 26 H18Z" fill="#6b4a2a"/><rect x="30" y="-26" width="12" height="26" rx="5" fill="#b69cf0"/>' +
        '<circle cx="36" cy="-32" r="8" fill="#f3caa0"/><path d="M28 -34 q8 -14 16 0 q10 30 30 34" fill="none" stroke="#ffd23f" stroke-width="5" stroke-linecap="round"/>' +
        '<rect x="66" y="-24" width="12" height="24" rx="5" fill="#3f6a8a"/><circle cx="72" cy="-30" r="8" fill="#f3caa0"/><path d="M64 -34 q8 -8 16 0" fill="#5a3a22"/>' +
        '<rect x="50" y="-40" width="10" height="13" rx="3" fill="#ffc46b"/><circle cx="55" cy="-34" r="18" fill="#ffc46b" opacity=".25"/></g>';
    function lilyPad(x, y, rx, flower) {
        var ry = rx * .36;
        return '<path d="M' + x + ' ' + y + ' L' + (x + rx) + ' ' + (y - ry * .4) + ' A' + rx + ' ' + ry + ' 0 1 1 ' + (x + rx) + ' ' + (y + ry * .4) + 'Z" fill="#5cc267" stroke="#2c7a38" stroke-width="2"/>' +
            '<path d="M' + (x - rx * .6) + ' ' + y + ' Q' + x + ' ' + (y - ry * .5) + ' ' + (x + rx * .5) + ' ' + y + '" fill="none" stroke="#6cc04a" stroke-width="1.2" opacity=".7"/>' +
            (flower ? '<g transform="translate(' + (x - rx * .45) + ' ' + (y - 4) + ')">' +
                '<ellipse cx="-6" cy="-3" rx="6" ry="3" fill="#ffb3d1" transform="rotate(-30)"/><ellipse cx="6" cy="-3" rx="6" ry="3" fill="#ffb3d1" transform="rotate(30)"/>' +
                '<ellipse cx="0" cy="-6" rx="3" ry="7" fill="#ffd1e3"/><circle cx="0" cy="-2" r="2.5" fill="#ffd23f"/></g>' : '');
    }
    function frog(extra) {
        return '<ellipse cx="-12" cy="6" rx="7" ry="4" fill="#5aa83c" stroke="#1f5f2a" stroke-width="1.2"/><ellipse cx="12" cy="6" rx="7" ry="4" fill="#5aa83c" stroke="#1f5f2a" stroke-width="1.2"/>' +
            '<ellipse cx="0" cy="0" rx="16" ry="11" fill="#6cc04a" stroke="#1f5f2a" stroke-width="1.5"/><ellipse cx="0" cy="3" rx="10" ry="6" fill="#c9ef9a"/>' +
            '<circle cx="-7" cy="-10" r="5.5" fill="#6cc04a" stroke="#1f5f2a" stroke-width="1.5"/><circle cx="7" cy="-10" r="5.5" fill="#6cc04a" stroke="#1f5f2a" stroke-width="1.5"/>' +
            '<circle cx="-7" cy="-10" r="3.6" fill="#fff"/><circle cx="7" cy="-10" r="3.6" fill="#fff"/><circle cx="-6.2" cy="-10" r="1.9" fill="#1a1418"/><circle cx="7.8" cy="-10" r="1.9" fill="#1a1418"/>' +
            '<path d="M-6 -2 q6 4 12 0" fill="none" stroke="#1f5f2a" stroke-width="1.3" stroke-linecap="round"/>' + extra;
    }
    var bayou = lilyPad(70, 842, 44, true) + lilyPad(190, 874, 38, false) + lilyPad(300, 836, 46, true) + lilyPad(420, 872, 34, true) +
        lilyPad(1210, 874, 36, true) + lilyPad(1500, 858, 42, false) + lilyPad(1420, 890, 30, true) +
        // Tiana (con su florecita) y Naveen (con su coronita)
        '<g transform="translate(78 826)">' + frog('<g transform="translate(0 -17)"><ellipse cx="-4" cy="0" rx="4" ry="2" fill="#ffb3d1" transform="rotate(-30)"/><ellipse cx="4" cy="0" rx="4" ry="2" fill="#ffb3d1" transform="rotate(30)"/><circle r="1.8" fill="#ffd23f"/></g>') + '</g>' +
        '<g class="naveen"><g transform="translate(300 820) scale(-1 1)">' + frog('<path d="M-6 -16 l2 -6 l4 4 l4 -4 l2 6Z" fill="#f2b823" stroke="#b8860b" stroke-width="1"/>') + '</g></g>' +
        '<text class="frog-heart" x="138" y="800" font-size="20" text-anchor="middle">💚</text>' +
        // Evangeline, la estrella más brillante
        '<g class="evangeline"><circle cx="560" cy="70" r="26" fill="#fff6c8" opacity=".25"/><path d="M560 52 L564 66 L578 70 L564 74 L560 88 L556 74 L542 70 L556 66Z" fill="#fffbe6"/></g>';

    var scene = '<svg class="disney-scene" viewBox="0 0 1600 900" preserveAspectRatio="xMidYMax slice" aria-hidden="true"><defs>' +
        '<linearGradient id="dnSky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0a0f3a"/><stop offset=".45" stop-color="#2b2a7c"/><stop offset=".72" stop-color="#8a5aa8"/><stop offset=".8" stop-color="#f0a6b8"/></linearGradient>' +
        '<linearGradient id="dnLake" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2b2f78"/><stop offset="1" stop-color="#0d1238"/></linearGradient>' +
        '<linearGradient id="dnDust" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".3" stop-color="#fff3b0"/><stop offset="1" stop-color="#fff" stop-opacity=".2"/></linearGradient>' +
        '</defs><rect width="1600" height="900" fill="url(#dnSky)"/>' + stars(160) +
        burst(120, 170, 70, ["#ff9bd2", "#fff", "#9ec5ff"], 0) + burst(420, 120, 55, ["#ffd98a", "#fff", "#ff9bd2"], 1.1) +
        burst(1320, 150, 80, ["#9ec5ff", "#c9b6ff", "#fff"], .6) + burst(1500, 300, 55, ["#ffd98a", "#ff9bd2"], 1.9) +
        '<path class="pixie-arc" pathLength="1" d="M220 300 C 500 -60, 1150 -40, 1580 260" fill="none" stroke="url(#dnDust)" stroke-width="5" stroke-linecap="round" stroke-dasharray="1"/>' +
        '<rect y="760" width="1600" height="140" fill="url(#dnLake)"/>' + reflection + castle + shelves + boat + bayou +
        '</svg>';

    // ---------------- capa de fondo con elementos animados ----------------
    var layer = document.createElement("div");
    layer.className = "disney-bg";
    layer.setAttribute("aria-hidden", "true");
    var html = scene;
    for (var i = 0; i < 26; i++) {
        html += '<span class="lantern" style="left:' + (Math.random() * 100).toFixed(1) + '%;--t:' + (18 + Math.random() * 16).toFixed(1) + 's;--d:-' + (Math.random() * 30).toFixed(1) +
            's;--s:' + (0.6 + Math.random() * 0.8).toFixed(2) + ';--sway:' + ((Math.random() * 2 - 1) * 50).toFixed(0) + 'px;--y:' + (Math.random() * 90).toFixed(0) + '%"></span>';
    }
    html += '<div class="up-house"><svg viewBox="0 0 140 230">' + upBalloons() +
        '<g stroke="#3a2a2a" stroke-width="1.5" stroke-linejoin="round"><rect x="38" y="150" width="64" height="52" fill="#f2c1a0"/><path d="M30 152 L70 118 L110 152Z" fill="#6a4c93"/>' +
        '<rect x="80" y="116" width="10" height="24" fill="#8a5a3a"/><rect x="46" y="164" width="16" height="16" fill="#9ec5ff"/><rect x="76" y="164" width="16" height="16" fill="#9ec5ff"/>' +
        '<rect x="30" y="200" width="80" height="8" fill="#f7e3a6"/><path d="M62 150 L70 136 L78 150Z" fill="#f7e3a6"/></g></svg></div>';
    [["Alegría", "#ffd23f"], ["Tristeza", "#4a8cff"], ["Furia", "#ef4444"], ["Temor", "#a26bff"], ["Desagrado", "#4cc36b"],
     ["Ansiedad", "#ff8a2b"], ["Envidia", "#2fd4c4"], ["Vergüenza", "#ff6fa8"], ["Ennui", "#4b4aa8"]].forEach(function (o, i) {
        html += '<span class="memory-orb" data-emo="' + o[0] + '" style="--c:' + o[1] + ';right:' + (2.5 + (i % 3) * 4.5) + '%;top:' + (10 + Math.floor(i / 3) * 9 + (i % 3) * 2.5) + '%;--d:-' + (i * .5) + 's"></span>';
    });
    layer.innerHTML = html;
    document.body.insertBefore(layer, page);

    function upBalloons() {
        var cols = ["#ff6b6b", "#ffd23f", "#4a8cff", "#4cc36b", "#ff9bd2", "#a26bff", "#ffa94d", "#66d9e8"];
        var g = "", rr = rnd(7);
        for (var i = 0; i < 44; i++) {
            var x = 20 + rr() * 100, y = 14 + rr() * 80;
            g += '<line x1="' + x.toFixed(0) + '" y1="' + y.toFixed(0) + '" x2="85" y2="118" stroke="#fff" stroke-width=".5" opacity=".6"/>';
        }
        for (var j = 0; j < 44; j++) {
            var bx = 20 + rr() * 100, by = 14 + rr() * 80;
            g += '<ellipse cx="' + bx.toFixed(0) + '" cy="' + by.toFixed(0) + '" rx="11" ry="13" fill="' + cols[j % cols.length] + '"/>';
        }
        return g;
    }

    // tocar una esfera de memoria muestra la emoción
    layer.addEventListener("click", function (e) {
        var orb = e.target.closest(".memory-orb");
        if (!orb) return;
        var label = document.createElement("div");
        label.className = "orb-label";
        label.textContent = orb.getAttribute("data-emo");
        var b = orb.getBoundingClientRect();
        label.style.left = (b.left + b.width / 2) + "px";
        label.style.top = (b.top - 10) + "px";
        document.body.appendChild(label);
        var a = label.animate([
            { transform: "translate(-50%, -80%)", opacity: 0 },
            { transform: "translate(-50%, -100%)", opacity: 1, offset: .2 },
            { transform: "translate(-50%, -100%)", opacity: 1, offset: .8 },
            { transform: "translate(-50%, -130%)", opacity: 0 }
        ], { duration: 1800 });
        a.onfinish = function () { label.remove(); };
    });

    // ---------------- personajes de Disney para el desfile ----------------
    var OUT = 'stroke="#1a1418" stroke-width="1.6" stroke-linejoin="round"';
    var actors = [
        // Mickey
        '<div class="actor disney-actor mickey-d" data-dur="7000"><svg viewBox="0 0 100 130"><g ' + OUT + '>' +
        '<path d="M36 96 q-18 6 -22 -10" fill="none" stroke="#111" stroke-width="2"/>' +
        '<g class="leg-a"><rect x="40" y="100" width="7" height="12" fill="#111"/><ellipse cx="45" cy="116" rx="11" ry="6" fill="#f2c230"/></g>' +
        '<g class="leg-b"><rect x="54" y="100" width="7" height="12" fill="#111"/><ellipse cx="60" cy="116" rx="11" ry="6" fill="#f2c230"/></g>' +
        '<path d="M42 80 L30 92" stroke="#111" stroke-width="5" stroke-linecap="round"/><circle cx="29" cy="94" r="5.5" fill="#fff"/>' +
        '<ellipse cx="52" cy="82" rx="14" ry="12" fill="#111"/><path d="M37 86 H67 L69 102 H35Z" fill="#d62828"/>' +
        '<circle cx="34" cy="26" r="13" fill="#111"/><circle cx="74" cy="24" r="13" fill="#111"/><circle cx="54" cy="50" r="20" fill="#111"/>' +
        '<path d="M40 52 Q38 36 48 38 Q52 45 57 38 Q70 36 70 53 Q71 67 57 69 Q42 69 40 52Z" fill="#f3caa0"/>' +
        '<path d="M62 80 L74 88" stroke="#111" stroke-width="5" stroke-linecap="round"/><circle cx="76" cy="89" r="5.5" fill="#fff"/></g>' +
        '<ellipse cx="46" cy="92" rx="2.2" ry="3.2" fill="#fff"/><ellipse cx="58" cy="92" rx="2.2" ry="3.2" fill="#fff"/>' +
        '<ellipse cx="53" cy="48" rx="2.6" ry="5" fill="#111"/><ellipse cx="62" cy="48" rx="2.6" ry="5" fill="#111"/>' +
        '<ellipse cx="67" cy="57" rx="4.5" ry="3.2" fill="#111"/><path d="M53 62 q8 7 16 -2" fill="#8a2a2a" stroke="#111" stroke-width="1.3"/></svg></div>',
        // Stitch
        '<div class="actor disney-actor stitch" data-dur="7000"><svg viewBox="0 0 110 120"><g ' + OUT + '>' +
        '<g class="leg-a"><ellipse cx="46" cy="106" rx="7" ry="9" fill="#4a78c9"/></g><g class="leg-b"><ellipse cx="64" cy="106" rx="7" ry="9" fill="#4a78c9"/></g>' +
        '<ellipse cx="34" cy="86" rx="5" ry="10" transform="rotate(30 34 86)" fill="#4a78c9"/>' +
        '<ellipse cx="55" cy="88" rx="17" ry="15" fill="#4a78c9"/><ellipse cx="55" cy="91" rx="10" ry="10" fill="#9dc3f0"/>' +
        '<ellipse cx="76" cy="86" rx="5" ry="10" transform="rotate(-30 76 86)" fill="#4a78c9"/>' +
        '<path d="M36 44 L6 12 L16 32 L4 38 L32 54Z" fill="#4a78c9"/><path d="M33 44 L14 22 L20 36 L30 48Z" fill="#e89ab8" stroke="none"/>' +
        '<path d="M74 42 L104 8 L96 30 L108 36 L78 54Z" fill="#4a78c9"/><path d="M77 42 L96 20 L92 34 L81 46Z" fill="#e89ab8" stroke="none"/>' +
        '<ellipse cx="55" cy="54" rx="26" ry="21" fill="#4a78c9"/></g>' +
        '<ellipse cx="45" cy="50" rx="9" ry="9" fill="#2c4f93"/><ellipse cx="66" cy="50" rx="9" ry="9" fill="#2c4f93"/>' +
        '<ellipse cx="45" cy="50" rx="6.5" ry="7.5" fill="#111"/><ellipse cx="66" cy="50" rx="6.5" ry="7.5" fill="#111"/>' +
        '<circle cx="47" cy="47" r="2" fill="#fff"/><circle cx="68" cy="47" r="2" fill="#fff"/>' +
        '<ellipse cx="56" cy="61" rx="7.5" ry="4.5" fill="#1f3a70"/>' +
        '<path d="M42 66 q14 10 28 0" fill="#fff" stroke="#1a1418" stroke-width="1.4"/></svg></div>',
        // Buzz Lightyear volando
        '<div class="actor disney-actor buzz" data-dur="6000"><span class="buzz-shout">¡Al infinito y más allá!</span><svg viewBox="0 0 150 90"><g ' + OUT + '>' +
        '<path d="M60 56 L14 58 L12 66 L60 66Z" fill="#fff"/><path d="M24 57 v9" stroke="#4cc36b" stroke-width="4"/><path d="M8 56 h10 v12 h-10Z" fill="#6a3fa0"/>' +
        '<path d="M60 62 L20 72 L22 80 L62 70Z" fill="#fff"/><path d="M10 70 l10 -2 l3 12 l-10 2Z" fill="#6a3fa0"/>' +
        '<path d="M70 40 L28 16 L32 26 L70 48Z" fill="#fff"/><path d="M28 16 L32 26 L40 24Z" fill="#d62828"/><path d="M44 26 L66 40" stroke="#4cc36b" stroke-width="3"/>' +
        '<rect x="56" y="38" width="46" height="30" rx="10" fill="#fff"/><rect x="66" y="42" width="24" height="18" rx="4" fill="#4cc36b"/>' +
        '<circle cx="72" cy="48" r="2.5" fill="#d62828"/><circle cx="80" cy="48" r="2.5" fill="#4a8cff"/><rect x="70" y="54" width="16" height="3" fill="#6a3fa0"/>' +
        '<path d="M100 48 L136 50" stroke="#fff" stroke-width="10" stroke-linecap="round"/><path d="M100 48 L136 50" stroke="#1a1418" stroke-width="1" fill="none"/>' +
        '<circle cx="140" cy="50" r="6" fill="#6a3fa0"/>' +
        '<circle cx="112" cy="36" r="13" fill="#6a3fa0"/><circle cx="114" cy="38" r="9" fill="#f1c8a0"/>' +
        '<circle cx="112" cy="36" r="20" fill="#cfe9ff" fill-opacity=".3"/></g>' +
        '<circle cx="118" cy="36" r="1.6" fill="#1a1418"/><path d="M115 43 q3 2 6 0" fill="none" stroke="#1a1418" stroke-width="1.2"/>' +
        '<path d="M100 22 q10 -4 20 2" fill="none" stroke="#fff" stroke-width="2" opacity=".8"/></svg></div>',
        // Olaf con su nubecita
        '<div class="actor disney-actor olaf" data-dur="9000"><svg viewBox="0 -30 100 160">' +
        '<g fill="#fff" opacity=".9"><circle cx="40" cy="-14" r="10"/><circle cx="54" cy="-18" r="13"/><circle cx="68" cy="-13" r="9"/></g>' +
        '<g fill="#dff1ff"><circle class="flake" cx="42" cy="-2" r="1.8"/><circle class="flake" cx="52" cy="0" r="1.8"/><circle class="flake" cx="62" cy="-3" r="1.8"/><circle class="flake" cx="48" cy="6" r="1.5"/><circle class="flake" cx="58" cy="4" r="1.5"/></g>' +
        '<g ' + OUT + '>' +
        '<path d="M52 18 v-12 M52 12 l-6 -6 M52 12 l6 -7 M58 20 l6 -10" stroke="#5a3a22" stroke-width="2" fill="none" stroke-linecap="round"/>' +
        '<g class="leg-a"><ellipse cx="42" cy="122" rx="8" ry="5" fill="#fff"/></g><g class="leg-b"><ellipse cx="60" cy="122" rx="8" ry="5" fill="#fff"/></g>' +
        '<ellipse cx="51" cy="106" rx="22" ry="16" fill="#fff"/>' +
        '<path d="M34 80 L14 70 M22 74 l-6 -8 M22 74 l-8 2" stroke="#5a3a22" stroke-width="2.4" fill="none" stroke-linecap="round"/>' +
        '<path d="M68 80 L88 70 M80 74 l6 -8 M80 74 l8 2" stroke="#5a3a22" stroke-width="2.4" fill="none" stroke-linecap="round"/>' +
        '<ellipse cx="51" cy="82" rx="16" ry="13" fill="#fff"/>' +
        '<path d="M36 50 Q34 20 54 20 Q72 22 70 48 Q74 62 60 66 Q44 68 38 60Z" fill="#fff"/></g>' +
        '<circle cx="51" cy="78" r="2.4" fill="#222"/><circle cx="51" cy="86" r="2.4" fill="#222"/><circle cx="51" cy="106" r="2.6" fill="#222"/>' +
        '<ellipse cx="50" cy="38" rx="2.4" ry="3.6" fill="#222"/><ellipse cx="61" cy="38" rx="2.4" ry="3.6" fill="#222"/>' +
        '<path d="M46 31 l7 -2 M58 30 l7 1" stroke="#222" stroke-width="1.6" stroke-linecap="round"/>' +
        '<path d="M56 44 L78 47 L56 50Z" fill="#f28c28"/><path d="M44 54 q12 12 24 0 Z" fill="#6b2a2a" stroke="#222" stroke-width="1.2"/><rect x="54" y="54" width="5" height="4" fill="#fff"/></svg></div>',
        // Nemo y Dory
        '<div class="actor disney-actor fish" data-dur="8000"><div class="bubbles"><span></span><span></span><span></span></div>' +
        '<svg class="dory" viewBox="0 0 110 60"><g ' + OUT + '>' +
        '<path class="tail" d="M22 30 L2 12 L8 30 L2 48Z" fill="#ffd23f"/><path d="M50 14 L60 2 L68 14Z" fill="#ffd23f"/>' +
        '<ellipse cx="56" cy="30" rx="36" ry="19" fill="#2b6de8"/></g>' +
        '<path d="M30 22 Q52 12 70 24 Q58 26 52 36 Q40 30 30 22Z" fill="#10204a"/><path d="M58 42 l10 10 l4 -8Z" fill="#ffd23f" stroke="#1a1418" stroke-width="1.2"/>' +
        '<circle cx="80" cy="24" r="7" fill="#fff" stroke="#1a1418" stroke-width="1.2"/><circle cx="82" cy="24" r="4" fill="#6a3fa0"/><circle cx="83" cy="23" r="1.6" fill="#111"/>' +
        '<path d="M86 36 q4 3 6 0" fill="none" stroke="#1a1418" stroke-width="1.3"/></svg>' +
        '<svg class="nemo" viewBox="0 0 70 44"><g ' + OUT + '>' +
        '<path class="tail" d="M14 22 L2 8 L4 22 L2 36Z" fill="#f28c28"/><ellipse cx="36" cy="22" rx="22" ry="14" fill="#f28c28"/>' +
        '<path d="M24 9 q-4 13 0 26 M24 9 q4 13 0 26" fill="#fff"/><path d="M40 8 q-4 14 0 28 M40 8 q5 14 0 28" fill="#fff"/><path d="M52 12 q-3 10 0 20 q4 -10 0 -20" fill="#fff"/>' +
        '<path d="M30 34 l-4 8 l8 -4Z" fill="#f28c28"/></g>' +
        '<circle cx="50" cy="18" r="5" fill="#fff" stroke="#1a1418" stroke-width="1.2"/><circle cx="51.5" cy="18" r="2.6" fill="#111"/></svg></div>',
        // Alegría con una esfera de memoria
        '<div class="actor disney-actor joy" data-dur="7000"><svg viewBox="0 -12 100 142"><g ' + OUT + '>' +
        '<g class="leg-a"><rect x="42" y="102" width="5" height="14" fill="#ffe066"/><ellipse cx="45" cy="118" rx="6" ry="3" fill="#6bb6ff"/></g>' +
        '<g class="leg-b"><rect x="54" y="102" width="5" height="14" fill="#ffe066"/><ellipse cx="57" cy="118" rx="6" ry="3" fill="#6bb6ff"/></g>' +
        '<path d="M40 80 L26 58" stroke="#ffe066" stroke-width="5" stroke-linecap="round"/><path d="M62 80 L74 58" stroke="#ffe066" stroke-width="5" stroke-linecap="round"/>' +
        '<path d="M38 74 H64 L72 104 H30Z" fill="#b8e04a"/>' +
        '<ellipse cx="51" cy="50" rx="17" ry="18" fill="#ffe066"/>' +
        '<path d="M34 50 L30 34 L40 38 L40 26 L50 34 L56 24 L60 34 L70 30 L68 42 L72 50 Q62 36 51 40 Q40 36 34 50Z" fill="#3a7bd5"/></g>' +
        '<circle class="memory" cx="50" cy="6" r="13" fill="#ffd23f" stroke="#fff" stroke-width="1.5"/><circle cx="46" cy="2" r="4" fill="#fff" opacity=".7"/>' +
        '<ellipse cx="46" cy="52" rx="2.6" ry="3.4" fill="#2a6b3a"/><ellipse cx="57" cy="52" rx="2.6" ry="3.4" fill="#2a6b3a"/>' +
        '<path d="M44 60 q7 7 14 0" fill="#fff" stroke="#1a1418" stroke-width="1.3"/>' +
        '<circle cx="36" cy="88" r="2" fill="#fff"/><circle cx="52" cy="94" r="2" fill="#fff"/><circle cx="62" cy="86" r="2" fill="#fff"/></svg></div>'
    ];
    if (runners) runners.insertAdjacentHTML("beforeend", actors.join(""));

    // gorro de mago de Mickey (Fantasía) sobre el nombre
    var h1 = document.querySelector("header h1");
    if (h1) h1.insertAdjacentHTML("afterbegin",
        '<svg class="sorcerer-hat" viewBox="0 0 80 90" aria-hidden="true">' +
        '<path d="M8 78 Q30 66 70 74 Q58 46 50 22 Q46 8 58 2 Q36 4 34 26 Q24 52 8 78Z" fill="#2a4fb8" stroke="#16296b" stroke-width="2" stroke-linejoin="round"/>' +
        '<path d="M34 26 Q24 52 8 78 Q14 76 20 74 Q30 50 38 30Z" fill="#fff" opacity=".12"/>' +
        '<path d="M44 44 a9 9 0 1 0 9 12 a7 7 0 1 1 -9 -12Z" fill="#fff3b0"/>' +
        '<path class="hat-star" d="M30 60 l2 5 l5 1 l-4 3 l1 5 l-4 -3 l-4 3 l1 -5 l-4 -3 l5 -1Z" fill="#fff3b0"/>' +
        '<path class="hat-star" d="M50 22 l1.5 3.5 l3.5 .5 l-2.8 2.2 l.8 3.6 l-3 -2 l-3 2 l.8 -3.6 l-2.8 -2.2 l3.5 -.5Z" fill="#fff3b0"/>' +
        '<path class="hat-star" d="M60 64 l1.2 2.8 l2.8 .4 l-2.2 1.8 l.6 2.8 l-2.4 -1.6 l-2.4 1.6 l.6 -2.8 l-2.2 -1.8 l2.8 -.4Z" fill="#fff3b0"/>' +
        '</svg>');

    // ---------------- prender / apagar ----------------
    var on = false;
    function set(v) {
        if (v === on) return;
        on = v;
        if (v && window.__setEra) window.__setEra(null);
        if (v && window.__vangogh) window.__vangogh(false);
        if (v && window.__sonora) window.__sonora(false);
        Object.keys(PALETTE).forEach(function (k) {
            if (v) root.style.setProperty(k, PALETTE[k]); else root.style.removeProperty(k);
        });
        root.classList.toggle("disney", v);
        if (v) {
            // reiniciar el arco de polvo de hadas para que se vuelva a dibujar
            var arc = layer.querySelector(".pixie-arc");
            arc.style.animation = "none";
            void arc.getBoundingClientRect();
            arc.style.animation = "";
            setTimeout(function () { if (on && window.__runParade) window.__runParade(); }, 2500);
        }
    }
    window.__disney = set;

    var typed = "";
    document.addEventListener("keydown", function (e) {
        if (e.key === "Escape" && on) { set(false); return; }
        if (e.key.length !== 1) return;
        typed = (typed + e.key.toLowerCase()).slice(-6);
        if (typed === "disney") set(!on);
    });

    if (window.__disneyPending) set(true);
})();
