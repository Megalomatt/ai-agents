import * as THREE from 'three';
import { COLORS, CELL_SIZE, INITIAL_SNAKE_LENGTH, GRID_SIZE } from '../utils/Constants.js';

export class Snake {
    constructor(scene) {
        this.scene = scene;
        this.segments = [];
        this.direction = new THREE.Vector3(1, 0, 0);
        this.nextDirection = new THREE.Vector3(1, 0, 0);
        this.material = new THREE.MeshStandardMaterial({ color: COLORS.SNAKE_BODY });
        this.headMaterial = new THREE.MeshStandardMaterial({ color: COLORS.SNAKE_HEAD });

        this.speed = 7;
        this.positions = []; // Track positions for each segment

        this.init();
    }

    init() {
        const startX = -2;
        const startZ = 0;

        // Create initial snake segments
        for (let i = 0; i < INITIAL_SNAKE_LENGTH; i++) {
            const position = new THREE.Vector3(startX - i * CELL_SIZE, 0, startZ);
            this.addSegment(position, i === 0);
            this.positions.push(position.clone());
        }
    }

    update(deltaTime) {
        const timeStep = Math.min(deltaTime, 32) / 1000;
        const moveAmount = this.speed * timeStep;

        // Move head
        const head = this.segments[0];
        head.position.add(this.direction.clone().multiplyScalar(moveAmount));

        // Update segment positions
        for (let i = 1; i < this.segments.length; i++) {
            const segment = this.segments[i];
            const ahead = this.segments[i - 1];
            const toAhead = ahead.position.clone().sub(segment.position);
            const distance = toAhead.length();

            if (distance > CELL_SIZE) {
                toAhead.normalize();
                segment.position.add(toAhead.multiplyScalar(moveAmount));
            }
        }

        // Check boundaries
        const halfGrid = (GRID_SIZE / 2) - CELL_SIZE;
        return !(Math.abs(head.position.x) > halfGrid || Math.abs(head.position.z) > halfGrid);
    }

    changeDirection(newDirection) {
        if (!newDirection) return;

        // Prevent 180-degree turns
        const oppositeDirection = newDirection.clone().multiplyScalar(-1);
        if (!this.direction.equals(oppositeDirection)) {
            this.direction.copy(newDirection);
        }
    }

    addSegment(position, isHead = false) {
        const geometry = new THREE.BoxGeometry(CELL_SIZE, CELL_SIZE, CELL_SIZE);
        const material = isHead ? this.headMaterial : this.material;
        const segment = new THREE.Mesh(geometry, material);

        segment.position.copy(position);
        segment.castShadow = true;
        segment.receiveShadow = true;

        this.segments.push(segment);
        this.scene.add(segment);
    }

    grow() {
        const lastSegment = this.segments[this.segments.length - 1];
        const newPosition = lastSegment.position.clone();
        this.addSegment(newPosition);
        this.positions.push(newPosition.clone());
    }

    reset() {
        while (this.segments.length > 0) {
            const segment = this.segments.pop();
            this.scene.remove(segment);
            segment.geometry.dispose();
            segment.material.dispose();
        }

        this.positions = [];
        this.direction.set(1, 0, 0);

        this.init();
    }

    checkSelfCollision() {
        const head = this.segments[0];
        for (let i = 1; i < this.segments.length; i++) {
            if (head.position.distanceTo(this.segments[i].position) < CELL_SIZE * 0.8) {
                return true;
            }
        }
        return false;
    }

    checkFoodCollision(foodPosition) {
        return this.segments[0].position.distanceTo(foodPosition) < CELL_SIZE;
    }
}