function star_postion(n, colour) {
    return Array.from(
        { length: n },
        () =>
            `${Math.random() * 100 | 0}vw ${Math.random() * 100 | 0}vh 0 ${colour}`
    ).join(",")
}
document.querySelector(".sky").style.setProperty("--stars-obj", star_postion(20, "#fff3c4"))