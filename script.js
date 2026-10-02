function create_stars(n) {
    const stars = document.querySelector(".sky");

    for (let i = 0; i < n; i++) {
        const star = document.createElement("span");
        const size = Math.random() * 2 + 1;
        const duration = Math.random() * 5 + 5;
        const delay = Math.random() * 5;
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
create_stars(100);