import * as THREE from 'three';
import { KEYS } from '../utils/Constants.js';

export class InputHandler {
    constructor() {
        this.currentDirection = new THREE.Vector3(1, 0, 0);
        this.queuedDirection = null;
        this.init();
    }

    init() {
        document.addEventListener('keydown', this.handleKeyDown.bind(this));
    }

    handleKeyDown(event) {
        const key = event.key;
        let newDirection = null;

        if (KEYS.UP.includes(key)) {
            newDirection = new THREE.Vector3(0, 0, -1);
        } else if (KEYS.DOWN.includes(key)) {
            newDirection = new THREE.Vector3(0, 0, 1);
        } else if (KEYS.LEFT.includes(key)) {
            newDirection = new THREE.Vector3(-1, 0, 0);
        } else if (KEYS.RIGHT.includes(key)) {
            newDirection = new THREE.Vector3(1, 0, 0);
        }

        if (newDirection) {
            this.queuedDirection = newDirection;
        }
    }

    getDirection() {
        if (this.queuedDirection) {
            const direction = this.queuedDirection;
            this.queuedDirection = null;
            return direction;
        }
        return null;
    }

    reset() {
        this.currentDirection.set(1, 0, 0);
        this.queuedDirection = null;
    }
}