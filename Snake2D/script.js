const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');
const scoreElement = document.getElementById('score');
const finalScoreElement = document.getElementById('finalScore');
const gameOverElement = document.getElementById('gameOver');
const restartButton = document.getElementById('restartButton');

// Set canvas size
canvas.width = 400;
canvas.height = 400;

// Game constants
const gridSize = 20;
const tileCount = canvas.width / gridSize;
const tileSize = canvas.width / tileCount;

// Game variables
let snake = [
    { x: 10, y: 10 }
];
let food = { x: 15, y: 15 };
let dx = 0;
let dy = 0;
let score = 0;
let gameLoop;
let gameSpeed = 100;

// Initialize game
function init() {
    snake = [{ x: 10, y: 10 }];
    food = generateFood();
    // Start moving right by default
    dx = 1;
    dy = 0;
    score = 0;
    scoreElement.textContent = score;
    gameOverElement.style.display = 'none';
    if (gameLoop) clearInterval(gameLoop);

    // Add console logs for debugging
    console.log('Game initialized');
    console.log('Canvas dimensions:', canvas.width, 'x', canvas.height);
    console.log('Initial snake position:', snake[0]);
    console.log('Initial food position:', food);

    gameLoop = setInterval(update, gameSpeed);
}

// Generate random food position
function generateFood() {
    let newFood;
    do {
        newFood = {
            x: Math.floor(Math.random() * tileCount),
            y: Math.floor(Math.random() * tileCount)
        };
    } while (snake.some(segment => segment.x === newFood.x && segment.y === newFood.y));
    return newFood;
}

// Update game state
function update() {
    // Move snake
    const head = { x: snake[0].x + dx, y: snake[0].y + dy };

    // Debug logging
    console.log('Snake moving:', dx, dy);
    console.log('Head position:', head);

    // Check for wall collision
    if (head.x < 0 || head.x >= tileCount || head.y < 0 || head.y >= tileCount) {
        console.log('Wall collision detected');
        gameOver();
        return;
    }

    // Check for self collision
    if (snake.some(segment => segment.x === head.x && segment.y === head.y)) {
        gameOver();
        return;
    }

    snake.unshift(head);

    // Check for food collision
    if (head.x === food.x && head.y === food.y) {
        score += 10;
        scoreElement.textContent = score;
        food = generateFood();
    } else {
        snake.pop();
    }

    draw();
}

// Draw game state
function draw() {
    // Clear canvas
    ctx.fillStyle = '#000';
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    // Draw snake
    ctx.fillStyle = '#4CAF50';
    snake.forEach((segment, index) => {
        if (index === 0) {
            // Draw head with a different color
            ctx.fillStyle = '#45a049';
        } else {
            ctx.fillStyle = '#4CAF50';
        }
        ctx.fillRect(segment.x * tileSize, segment.y * tileSize, tileSize - 2, tileSize - 2);
    });

    // Draw food
    ctx.fillStyle = '#ff4444';
    ctx.fillRect(food.x * tileSize, food.y * tileSize, tileSize - 2, tileSize - 2);
}

// Handle game over
function gameOver() {
    clearInterval(gameLoop);
    gameOverElement.style.display = 'block';
    finalScoreElement.textContent = score;
}

// Event listeners
document.addEventListener('keydown', (e) => {
    switch (e.key) {
        case 'ArrowUp':
            if (dy === 0) {
                dx = 0;
                dy = -1;
            }
            break;
        case 'ArrowDown':
            if (dy === 0) {
                dx = 0;
                dy = 1;
            }
            break;
        case 'ArrowLeft':
            if (dx === 0) {
                dx = -1;
                dy = 0;
            }
            break;
        case 'ArrowRight':
            if (dx === 0) {
                dx = 1;
                dy = 0;
            }
            break;
    }
});

restartButton.addEventListener('click', init);

// Start the game
init();