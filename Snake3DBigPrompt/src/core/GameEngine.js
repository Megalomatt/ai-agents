import * as THREE from 'three';
import { SceneManager } from './SceneManager.js';
import { Snake } from './Snake.js';
import { Food } from './Food.js';
import { InputHandler } from './InputHandler.js';
import { UIManager } from './UIManager.js';
import { GRID_SIZE, MOVE_INTERVAL } from '../utils/Constants.js';

export class GameEngine {
    constructor() {
        this.sceneManager = new SceneManager();
        this.snake = new Snake(this.sceneManager.scene);
        this.food = new Food(this.sceneManager.scene);
        this.inputHandler = new InputHandler();
        this.uiManager = new UIManager();

        this.score = 0;
        this.isGameOver = false;
        this.lastFrameTime = performance.now();

        // Bind restart button
        document.getElementById('restart-button').addEventListener('click', () => {
            this.restart();
        });

        this.init();
    }

    init() {
        this.food.spawn();
        requestAnimationFrame(this.animate.bind(this));
    }

    update(currentTime) {
        if (this.isGameOver) return;

        const deltaTime = Math.min(currentTime - this.lastFrameTime, 32); // Cap at ~30fps minimum
        this.lastFrameTime = currentTime;

        // Update snake movement
        const direction = this.inputHandler.getDirection();
        this.snake.changeDirection(direction);

        const validMove = this.snake.update(deltaTime);
        if (!validMove || this.snake.checkSelfCollision()) {
            this.gameOver();
            return;
        }

        // Check food collision
        if (this.snake.checkFoodCollision(this.food.position)) {
            this.score++;
            this.uiManager.updateScore(this.score);
            this.snake.grow();
            this.food.spawn();
        }
    }

    animate(currentTime) {
        requestAnimationFrame(this.animate.bind(this));
        this.update(currentTime);
        this.sceneManager.render();
    }

    gameOver() {
        this.isGameOver = true;
        this.uiManager.showGameOver(this.score);
    }

    restart() {
        this.score = 0;
        this.isGameOver = false;
        this.lastFrameTime = performance.now();
        this.snake.reset();
        this.food.spawn();
        this.uiManager.reset();
        this.inputHandler.reset();
    }
}