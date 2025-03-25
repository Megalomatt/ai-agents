export class UIManager {
    constructor() {
        this.scoreElement = document.getElementById('score');
        this.gameOverElement = document.getElementById('game-over');
        this.finalScoreElement = document.getElementById('final-score');
        this.restartButton = document.getElementById('restart-button');
    }

    updateScore(score) {
        this.scoreElement.textContent = `Score: ${score}`;
    }

    showGameOver(finalScore) {
        this.finalScoreElement.textContent = finalScore;
        this.gameOverElement.classList.remove('hidden');
    }

    reset() {
        this.updateScore(0);
        this.gameOverElement.classList.add('hidden');
    }
}