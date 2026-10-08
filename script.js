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

