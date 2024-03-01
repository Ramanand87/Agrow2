const boxes = document.querySelectorAll('.scheme');

boxes.forEach((box, index) => {
    box.style.animationDelay = `${index * 0.5}s`;
});