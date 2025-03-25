import { GameEngine } from './core/GameEngine.js';

document.addEventListener('DOMContentLoaded', () => {
    const game = new GameEngine();

    // Setup restart button
    document.getElementById('restart-button').addEventListener('click', () => {
        game.restart();
    });
}); 