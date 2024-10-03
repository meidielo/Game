let canvas = document.getElementById('gameCanvas');
let ctx = canvas.getContext('2d');
let dragging = false;
let draggedSymbol = null;
let symbols = [
    { symbol: '5', x: 50, y: 50, width: 40, height: 40 },
    { symbol: '+', x: 150, y: 50, width: 40, height: 40 },
    { symbol: '7', x: 250, y: 50, width: 40, height: 40 }
];
let dropZone = { x: 400, y: 300, width: 100, height: 50 };

// Draw the symbols on the canvas
function drawSymbols() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    // Draw each symbol
    symbols.forEach(symbol => {
        ctx.fillStyle = 'black';
        ctx.fillRect(symbol.x, symbol.y, symbol.width, symbol.height);
        ctx.fillStyle = 'white';
        ctx.font = '30px Arial';
        ctx.fillText(symbol.symbol, symbol.x + 10, symbol.y + 30);
    });

    // Draw the drop zone
    ctx.strokeStyle = 'black';
    ctx.strokeRect(dropZone.x, dropZone.y, dropZone.width, dropZone.height);
    ctx.fillText('Drop Here', dropZone.x + 10, dropZone.y + 35);
}

// Check if the mouse is inside the symbol
function isMouseInSymbol(symbol, mouseX, mouseY) {
    return mouseX > symbol.x && mouseX < symbol.x + symbol.width &&
           mouseY > symbol.y && mouseY < symbol.y + symbol.height;
}

// Handle mouse down event (start dragging)
canvas.addEventListener('mousedown', function(event) {
    let mouseX = event.offsetX;
    let mouseY = event.offsetY;

    // Check if mouse is on any symbol
    symbols.forEach(symbol => {
        if (isMouseInSymbol(symbol, mouseX, mouseY)) {
            dragging = true;
            draggedSymbol = symbol;
        }
    });
});

// Handle mouse up event (drop symbol)
canvas.addEventListener('mouseup', function(event) {
    if (dragging && draggedSymbol) {
        let mouseX = event.offsetX;
        let mouseY = event.offsetY;

        // Check if the symbol was dropped inside the drop zone
        if (mouseX > dropZone.x && mouseX < dropZone.x + dropZone.width &&
            mouseY > dropZone.y && mouseY < dropZone.y + dropZone.height) {
            console.log(`${draggedSymbol.symbol} dropped in the correct spot!`);
            // You can add logic here to handle the successful drop
        }

        dragging = false;
        draggedSymbol = null;
    }
});

// Handle mouse move event (dragging)
canvas.addEventListener('mousemove', function(event) {
    if (dragging && draggedSymbol) {
        let mouseX = event.offsetX;
        let mouseY = event.offsetY;

        // Update symbol's position
        draggedSymbol.x = mouseX - draggedSymbol.width / 2;
        draggedSymbol.y = mouseY - draggedSymbol.height / 2;

        drawSymbols(); // Redraw symbols with updated positions
    }
});

document.addEventListener('DOMContentLoaded', function () {
    const draggables = document.querySelectorAll('.draggable');
    const dropzones = document.querySelectorAll('.dropzone');

    draggables.forEach(draggable => {
        draggable.addEventListener('dragstart', dragStart);
    });

    dropzones.forEach(dropzone => {
        dropzone.addEventListener('dragover', dragOver);
        dropzone.addEventListener('drop', drop);
    });

    function dragStart(e) {
        e.dataTransfer.setData('text', e.target.id);
    }

    function dragOver(e) {
        e.preventDefault();
    }

    function drop(e) {
        e.preventDefault();
        const data = e.dataTransfer.getData('text');
        const draggable = document.getElementById(data);
        e.target.innerHTML = draggable.innerHTML;
        checkAnswer();
    }

    // Check if the answer is correct after dropping
    function checkAnswer() {
        const operator = document.getElementById('operator').innerText;
        const result = document.getElementById('result').innerText;
        const correctAnswer = eval(`5 ${operator} 7`);

        if (correctAnswer == result) {
            alert('Correct!');
        } else {
            alert('Incorrect, try again!');
            loseLife();
        }
    }

    // Manage the life system
    let lives = 3;
    function loseLife() {
        if (lives > 0) {
            document.getElementById('life' + lives).style.visibility = 'hidden';
            lives--;
        }
        if (lives === 0) {
            alert('Game Over');
        }
    }
});

// Initial draw
drawSymbols();