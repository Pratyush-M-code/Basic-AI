function create_stars(n) {
    const stars = document.querySelector(".sky");

    for (let i = 0; i < n; i++) {
        const star = document.createElement("span");
        const size = Math.random() * 2.5 + 1;
        const duration = Math.random() * 5 + 10;
        const delay = Math.random() * 10 + 2;
        const x = Math.random() * 100;
        const y = Math.random() * 100;

        star.classList.add("star");
        star.style.width = `${size}px`;
        star.style.height = `${size}px`;
        star.style.left = `${x}vw`;
        star.style.top = `${y}vh`;
        star.style.animationDuration = `${duration}s`;
        star.style.animationDelay = `${delay}s`;

        stars.appendChild(star);
    }
}
create_stars(200);

function pixelateCorner(element, options = {}) {
    const css_values = getComputedStyle(element);
    const pixelStep = parseFloat(css_values.getPropertyValue("--ps"));
    const stepCount = parseInt(css_values.getPropertyValue("--steps"));

    let x = 0;
    let y = pixelStep * stepCount;
    const polygonPath = [[x, y]];/*basically the first [] defines the total path and each nested [] is a point*/
    let horizontal = true;

    for (let i = 0; i < stepCount * 2; i = i + 1) {
        if (horizontal) {
            x = x + pixelStep
        } else {
            y = y - pixelStep
        }
        polygonPath.push([x, y]);
        horizontal = !horizontal
    }

    const start = (val) => (val === 0 ? "0.06rem" : `${val * 0.06}rem`)
    const end = (val) => (val === 0 ? "100%" : `calc(100% - ${val * 0.06}rem)`)
    /*top-t + left-l + corner*/
    const tlcorner = [...polygonPath].map(([X, Y]) => `${start(X)} ${start(Y)}`);
    const trcorner = [...polygonPath].reverse().map(([X, Y]) => `${end(X)} ${start(Y)}`);
    const brcorner = [...polygonPath].map(([X, Y]) => `${end(X)} ${end(Y)}`);
    const blcorner = [...polygonPath].reverse().map(([X, Y]) => `${start(X)} ${end(Y)}`);
    const allPoints = [
        ...tlcorner,
        ...trcorner,
        ...brcorner,
        ...blcorner,
    ];

    element.style.clipPath = `polygon(${allPoints.join(', ')})`;

}

document.querySelectorAll('.pixel-corners').forEach((element) => pixelateCorner(element));

const allimagebtns = document.querySelectorAll('.image-btn');
const allaugbtns = document.querySelectorAll('.aug-btn');

function updateBtn(Btn) {
    if (Btn.classList.contains("active")) {
        Btn.classList.remove("active");
    }
    else {
        if (Btn.classList.contains("image-btn")) {
            allimagebtns.forEach((btn) => {
                btn.classList.remove("active");
            });

        }
        if (Btn.classList.contains("aug-btn")) {
            allaugbtns.forEach((btn) => {
                btn.classList.remove("active");
            });
        }
        Btn.classList.add("active");
    }
    console.log([...document.querySelectorAll(".active")].map(b => b.id));
}

const placeholder = document.getElementById("images");
function updateImages() {
    const activeBtns = [...document.querySelectorAll(".active")].map(b => b.id);
    const [image, augmentation] = activeBtns;
    let aug = + augmentation.replace("Factor-", "").replace("-btn", "");
    let img = image.replace("-btn", "");

    placeholder.innerHTML = "";

    const og = document.createElement("img");
    og.src = `Elements/${img}/Original.jpg`;
    og.alt = `${img} Original`;
    og.setAttribute("width", "150vw");
    og.setAttribute("height", "150vh");
    placeholder.appendChild(og);

    for (let i = 1; i <= aug; i++) {
        const augmentedImage = document.createElement("img");
        augmentedImage.src = `Elements/${img}/Original.jpg.${i}.jpg`;
        augmentedImage.alt = `${img} ${i}`;
        augmentedImage.setAttribute("width", "150vw");
        augmentedImage.setAttribute("height", "150vh");
        placeholder.appendChild(augmentedImage);
    }
}


allaugbtns.forEach(btn => {
    btn.onclick = () => {
        updateBtn(btn);
        updateImages();
    }
});
allimagebtns.forEach(btn => {
    btn.onclick = () => {
        updateBtn(btn);
        updateImages();
    }
});


const COLORS = {
    Overall: '#ffffff', Comet: '#ff9f43', Galaxy: '#8fd0ff',
    Nebula: '#c58bff', Planet: '#7fe0c8', Stars: '#ffd85a'
};
const MAX_FACTOR = 15;
const WIDTH = 640, HEIGHT = 360;
const LEFT = 56, RIGHT = 24, TOP = 20, BOTTOM = 56;
const PLOT_W = WIDTH - LEFT - RIGHT;
const PLOT_H = HEIGHT - TOP - BOTTOM;

const data = {};
let selected = null;

async function loadData() {
    const response = await fetch('results.csv');
    const text = await response.text();
    const rows = text.trim().split('\n').slice(1);

    for (const row of rows) {
        const [factor, name, mean, min, max] = row.split(',');
        if (!data[name]) data[name] = {};
        data[name][factor] = {
            mean: Number(mean),
            min: min ? Number(min) : null,
            max: max ? Number(max) : null
        };
    }
}

function x(factor) { return LEFT + factor * PLOT_W / MAX_FACTOR; }
function y(score) { return TOP + PLOT_H * (1 - score / 100); }


function drawGrid() {
    let svg = '';
    for (const score of [0, 25, 50, 75, 100]) {
        svg += `<line x1="${LEFT}" x2="${WIDTH - RIGHT}" y1="${y(score)}" y2="${y(score)}" stroke="#4a5cc0" stroke-opacity="0.35"/>`;
        svg += `<text x="${LEFT - 8}" y="${y(score) + 4}" text-anchor="end" fill="#93a0d0" font-size="12">${score}</text>`;
    }
    for (let f = 0; f <= MAX_FACTOR; f++) {
        svg += `<text x="${x(f)}" y="${HEIGHT - 32}" text-anchor="middle" fill="#d7def5" font-size="12">${f}</text>`;
    }
    svg += `<text x="${LEFT + PLOT_W / 2}" y="${HEIGHT - 10}" text-anchor="middle" fill="#93a0d0" font-size="13">Augmentation factor</text>`;
    return svg;
}

function drawLine(name) {
    const color = COLORS[name];
    const faded = selected !== null && selected !== name;
    const opacity = faded ? 0.15 : 1;
    const dash = name === 'Overall' ? '8 6' : 'none';

    let points = '';
    let squares = '';
    for (let f = 0; f <= MAX_FACTOR; f++) {
        const result = data[name][f];
        if (!result) continue
        points += `${x(f)},${y(result.mean)} `;
        squares += `<rect x="${x(f) - 4}" y="${y(result.mean) - 4}" width="8" height="8" fill="${color}"/>`;
    }

    return `<g opacity="${opacity}">
    <polyline points="${points}" fill="none" stroke="${color}" stroke-width="3" stroke-dasharray="${dash}"/>
    ${squares}
  </g>`;
}

function drawRange(name) {
    let svg = '';
    for (let f = 0; f <= MAX_FACTOR; f++) {
        const result = data[name][f];
        if (!result || result.min === null) continue;
        svg += `<line x1="${x(f)}" x2="${x(f)}" y1="${y(result.max)}" y2="${y(result.min)}" stroke="#fff" stroke-width="2"/>`;
        svg += `<line x1="${x(f) - 5}" x2="${x(f) + 5}" y1="${y(result.max)}" y2="${y(result.max)}" stroke="#fff" stroke-width="2"/>`;
        svg += `<line x1="${x(f) - 5}" x2="${x(f) + 5}" y1="${y(result.min)}" y2="${y(result.min)}" stroke="#fff" stroke-width="2"/>`;
    }
    return svg;
}

function drawChart() {
    const names = Object.keys(data).filter(name => name !== selected);
    if (selected) names.push(selected);

    let svg = drawGrid();
    for (const name of names) svg += drawLine(name);
    if (selected) svg += drawRange(selected);

    document.getElementById('chart').innerHTML = svg;

    document.getElementById('note').textContent = selected
        ? `${selected}: white bars show the lowest to highest run. Click again to reset.`
        : 'Pick a class to fade the others and see its spread.';

    for (const button of document.querySelectorAll('#buttons button')) {
        button.setAttribute('aria-pressed', button.textContent === selected);
    }
}

//<button class="pixel-corners btn aug-btn" style="--ps:5;--steps:1;" id="Factor-15-btn">Factor 15</button>
function createButtons() {
    for (const name of Object.keys(data)) {
        const button = document.createElement('button');
        button.type = 'button';
        button.className = 'pixel-corners btn';
        button.style = '--ps:5;--steps:1;'
        button.textContent = name;
        button.onclick = function () {
            selected = (selected === name) ? null : name;    // clicking again resets
            drawChart();
        };
        document.getElementById('buttons').appendChild(button);
    }
}

loadData().then(function () {
    createButtons();
    drawChart();
});