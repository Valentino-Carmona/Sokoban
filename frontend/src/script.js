const boardElement = document.getElementById('game-board');
const levelDisplay = document.getElementById('level-display');
const winMessage = document.getElementById('win-message');
const finishMessage = document.getElementById('finish-message');

const IMAGE_MAP = {
    '#': 'img/wall.gif',
    '$': 'img/box.gif',
    ' ': 'img/ground.gif',
    '.': 'img/goal.gif',
    '@': 'img/player.gif',
    '*': ['img/goal.gif', 'img/box.gif'], // CAJA_EN_PUNTO
    '+': ['img/goal.gif', 'img/player.gif'] // PJ_EN_PUNTO
};

let isProcessing = false;

async function startGame() {
    const response = await fetch('/api/start', { method: 'POST' });
    const data = await response.json();
    if (data.error) {
        console.error(data.error);
        return;
    }
    updateUI(data);
}

async function sendMove(accion) {
    if (isProcessing) return;
    isProcessing = true;

    try {
        const response = await fetch('/api/move', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ accion })
        });
        const data = await response.json();
        updateUI(data);
    } catch (e) {
        console.error(e);
    } finally {
        isProcessing = false;
    }
}

function updateUI(data) {
    levelDisplay.textContent = data.nivel;
    
    if (data.completado) {
        finishMessage.classList.remove('hidden');
        winMessage.classList.add('hidden');
    } else if (data.ganado) {
        winMessage.classList.remove('hidden');
        // El backend ya pasó al siguiente nivel internamente,
        // pero mostramos un mensajito breve
        setTimeout(() => {
            winMessage.classList.add('hidden');
        }, 2000);
    } else {
        winMessage.classList.add('hidden');
        finishMessage.classList.add('hidden');
    }

    renderGrid(data.grilla);
}

function renderGrid(grilla) {
    boardElement.innerHTML = '';
    
    grilla.forEach(row => {
        const rowDiv = document.createElement('div');
        rowDiv.className = 'row';
        
        row.forEach(cellChar => {
            const cellDiv = document.createElement('div');
            cellDiv.className = 'cell';
            
            // Siempre dibujar el suelo como base (opcional, pero ayuda a que no haya huecos)
            const groundImg = document.createElement('img');
            groundImg.src = 'img/ground.gif';
            cellDiv.appendChild(groundImg);

            const imgData = IMAGE_MAP[cellChar];
            
            if (imgData) {
                if (Array.isArray(imgData)) {
                    // Múltiples imágenes apiladas (ej: objetivo + caja)
                    imgData.forEach(src => {
                        const img = document.createElement('img');
                        img.src = src;
                        cellDiv.appendChild(img);
                    });
                } else if (cellChar !== ' ') {
                    const img = document.createElement('img');
                    img.src = imgData;
                    cellDiv.appendChild(img);
                }
            }
            
            rowDiv.appendChild(cellDiv);
        });
        
        boardElement.appendChild(rowDiv);
    });
}

// Event Listeners para teclado
window.addEventListener('keydown', (e) => {
    // Evitar scroll con flechas
    if(["Space","ArrowUp","ArrowDown","ArrowLeft","ArrowRight"].indexOf(e.code) > -1) {
        e.preventDefault();
    }

    switch(e.key.toLowerCase()) {
        case 'arrowup':
        case 'w':
            sendMove('NORTE');
            break;
        case 'arrowdown':
        case 's':
            sendMove('SUR');
            break;
        case 'arrowleft':
        case 'a':
            sendMove('OESTE');
            break;
        case 'arrowright':
        case 'd':
            sendMove('ESTE');
            break;
        case 'r':
            sendMove('REINICIAR');
            break;
        case '1':
            sendMove('DESHACER');
            break;
        case '2':
            sendMove('REHACER');
            break;
        case '3':
            sendMove('BACKTRACKING');
            break;
        case 'escape':
            // En web, 'salir' podría recargar la página o cerrar, pero por ahora solo avisamos
            console.log('SALIR presionado (Escape)');
            break;
    }
});

// Iniciar juego al cargar
startGame();
