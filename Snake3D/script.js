import * as THREE from 'three';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

// Game elements
const scoreElement = document.getElementById('score');
const finalScoreElement = document.getElementById('finalScore');
const gameOverElement = document.getElementById('gameOver');
const restartButton = document.getElementById('restartButton');

// Three.js setup
const scene = new THREE.Scene();
scene.background = new THREE.Color(0x87CEEB); // Sky blue background

const camera = new THREE.PerspectiveCamera(75, 800 / 600, 0.1, 1000);
const renderer = new THREE.WebGLRenderer({
    antialias: true,
    alpha: true
});
renderer.setSize(800, 600);
renderer.setPixelRatio(window.devicePixelRatio);
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
document.getElementById('gameCanvas').appendChild(renderer.domElement);

// Lighting
const ambientLight = new THREE.AmbientLight(0xffffff, 0.6);
scene.add(ambientLight);

const directionalLight = new THREE.DirectionalLight(0xffffff, 1);
directionalLight.position.set(20, 30, 20);
directionalLight.castShadow = true;
directionalLight.shadow.camera.near = 1;
directionalLight.shadow.camera.far = 100;
directionalLight.shadow.camera.left = -50;
directionalLight.shadow.camera.right = 50;
directionalLight.shadow.camera.top = 50;
directionalLight.shadow.camera.bottom = -50;
directionalLight.shadow.mapSize.width = 2048;
directionalLight.shadow.mapSize.height = 2048;
scene.add(directionalLight);

// Camera controls
const controls = new OrbitControls(camera, renderer.domElement);
controls.enableDamping = true;
controls.dampingFactor = 0.05;
controls.maxDistance = 50;
controls.minDistance = 10;
camera.position.set(15, 15, 15);
controls.target.set(0, 0, 0);
controls.update();

// Game constants
const GRID_SIZE = 20;
const CUBE_SIZE = 1;
const GAME_SPEED = 200;

// Create game board
const boardGeometry = new THREE.BoxGeometry(GRID_SIZE, 1, GRID_SIZE);
const boardMaterial = new THREE.MeshPhongMaterial({
    color: 0x2c3e50,
    transparent: true,
    opacity: 0.8
});
const board = new THREE.Mesh(boardGeometry, boardMaterial);
board.position.y = -0.5;
board.receiveShadow = true;
scene.add(board);

// Create grid lines
const gridHelper = new THREE.GridHelper(GRID_SIZE, GRID_SIZE, 0x000000, 0x444444);
gridHelper.position.y = 0.01;
scene.add(gridHelper);

// Game variables
let snake = [];
let food = null;
let direction = new THREE.Vector3(1, 0, 0);
let score = 0;
let gameLoop;

// Create snake segment
function createSnakeSegment(position) {
    const geometry = new THREE.BoxGeometry(CUBE_SIZE * 0.9, CUBE_SIZE * 0.9, CUBE_SIZE * 0.9);
    const material = new THREE.MeshPhongMaterial({
        color: 0x4CAF50,
        specular: 0x009900,
        shininess: 30
    });
    const segment = new THREE.Mesh(geometry, material);
    segment.position.copy(position);
    segment.castShadow = true;
    segment.receiveShadow = true;
    scene.add(segment);
    return segment;
}

// Create food
function createFood() {
    if (food) {
        scene.remove(food);
    }
    const geometry = new THREE.SphereGeometry(CUBE_SIZE * 0.4, 16, 16);
    const material = new THREE.MeshPhongMaterial({
        color: 0xff4444,
        specular: 0xff0000,
        shininess: 50
    });
    food = new THREE.Mesh(geometry, material);

    // Random position
    let position;
    do {
        position = new THREE.Vector3(
            Math.floor(Math.random() * (GRID_SIZE - 2) - (GRID_SIZE - 2) / 2),
            0.5,
            Math.floor(Math.random() * (GRID_SIZE - 2) - (GRID_SIZE - 2) / 2)
        );
    } while (snake.some(segment =>
        segment.position.x === position.x &&
        segment.position.z === position.z
    ));

    food.position.copy(position);
    food.castShadow = true;
    food.receiveShadow = true;
    scene.add(food);
}

// Initialize game
function init() {
    // Clear previous game
    snake.forEach(segment => scene.remove(segment));
    snake = [];
    if (food) scene.remove(food);

    // Reset score
    score = 0;
    scoreElement.textContent = score;
    gameOverElement.style.display = 'none';

    // Create initial snake
    const startPos = new THREE.Vector3(-GRID_SIZE / 4, 0.5, 0);
    snake.push(createSnakeSegment(startPos));

    // Set initial direction
    direction.set(1, 0, 0);

    // Create food
    createFood();

    // Start game loop
    if (gameLoop) clearInterval(gameLoop);
    gameLoop = setInterval(update, GAME_SPEED);
}

// Update game state
function update() {
    // Calculate new head position
    const head = snake[0];
    const newPosition = head.position.clone().add(direction);

    // Check wall collision
    if (
        Math.abs(newPosition.x) > GRID_SIZE / 2 - CUBE_SIZE / 2 ||
        Math.abs(newPosition.z) > GRID_SIZE / 2 - CUBE_SIZE / 2
    ) {
        gameOver();
        return;
    }

    // Check self collision
    if (snake.some(segment =>
        segment.position.x === newPosition.x &&
        segment.position.z === newPosition.z
    )) {
        gameOver();
        return;
    }

    // Create new head
    const newHead = createSnakeSegment(newPosition);
    snake.unshift(newHead);

    // Check food collision
    if (
        Math.abs(newPosition.x - food.position.x) < CUBE_SIZE / 2 &&
        Math.abs(newPosition.z - food.position.z) < CUBE_SIZE / 2
    ) {
        score += 10;
        scoreElement.textContent = score;
        createFood();
    } else {
        const tail = snake.pop();
        scene.remove(tail);
    }
}

// Handle game over
function gameOver() {
    clearInterval(gameLoop);
    gameOverElement.style.display = 'block';
    finalScoreElement.textContent = score;
}

// Event listeners
document.addEventListener('keydown', (e) => {
    const oldDirection = direction.clone();

    switch (e.key) {
        case 'ArrowUp':
            if (direction.z === 0) {
                direction.set(0, 0, -1);
            }
            break;
        case 'ArrowDown':
            if (direction.z === 0) {
                direction.set(0, 0, 1);
            }
            break;
        case 'ArrowLeft':
            if (direction.x === 0) {
                direction.set(-1, 0, 0);
            }
            break;
        case 'ArrowRight':
            if (direction.x === 0) {
                direction.set(1, 0, 0);
            }
            break;
    }
});

restartButton.addEventListener('click', init);

// Animation loop
function animate() {
    requestAnimationFrame(animate);
    controls.update();

    // Add subtle rotation to food
    if (food) {
        food.rotation.y += 0.02;
    }

    renderer.render(scene, camera);
}

// Handle window resize
window.addEventListener('resize', () => {
    const width = 800;
    const height = 600;
    camera.aspect = width / height;
    camera.updateProjectionMatrix();
    renderer.setSize(width, height);
});

// Start the game
init();
animate();