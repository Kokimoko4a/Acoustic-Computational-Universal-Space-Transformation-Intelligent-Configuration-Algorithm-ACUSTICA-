// cursor.js

// 1. Инжектиране на CSS стиловете автоматично
const style = document.createElement('style');
style.textContent = `
    body { cursor: none; } /* Скрива стандартната стрелка */
    a, button, input { cursor: none; } /* Скрива я и над линкове */

    .cursor-dot {
        width: 6px;
        height: 6px;
        background-color: #ff3e3e; /* var(--hot-red) */
        position: fixed;
        top: 0; left: 0;
        transform: translate(-50%, -50%);
        border-radius: 50%;
        z-index: 10000;
        pointer-events: none;
    }

    .cursor-outline {
        width: 30px;
        height: 30px;
        border: 2px solid #ff3e3e;
        position: fixed;
        top: 0; left: 0;
        transform: translate(-50%, -50%);
        border-radius: 50%;
        z-index: 9999;
        pointer-events: none;
        transition: width 0.2s, height 0.2s, background-color 0.2s;
    }

    /* Ефект при кликване */
    .cursor-active {
        width: 50px;
        height: 50px;
        background-color: rgba(255, 62, 62, 0.2);
    }
`;
document.head.appendChild(style);

// 2. Създаване на HTML елементите
const dot = document.createElement('div');
const outline = document.createElement('div');
dot.className = 'cursor-dot';
outline.className = 'cursor-outline';
document.body.appendChild(dot);
document.body.appendChild(outline);

// 3. Логика за движение
window.addEventListener('mousemove', (e) => {
    const posX = e.clientX;
    const posY = e.clientY;

    dot.style.left = `${posX}px`;
    dot.style.top = `${posY}px`;

    outline.animate({
        left: `${posX}px`,
        top: `${posY}px`
    }, { duration: 400, fill: "forwards" });
});

// 4. Ефект при клик (пулсация)
window.addEventListener('mousedown', () => outline.classList.add('cursor-active'));
window.addEventListener('mouseup', () => outline.classList.remove('cursor-active'));