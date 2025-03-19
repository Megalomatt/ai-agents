import * as THREE from 'three';
import { COLORS, CELL_SIZE, GRID_SIZE } from '../utils/Constants.js';

export class Food {
    constructor(scene) {
        this.scene = scene;
        this.position = new THREE.Vector3();

        // Create food mesh
        const geometry = new THREE.SphereGeometry(CELL_SIZE / 2, 16, 16);
        const material = new THREE.MeshStandardMaterial({
            color: COLORS.FOOD,
            emissive: COLORS.FOOD,
            emissiveIntensity: 0.5
        });
        this.mesh = new THREE.Mesh(geometry, material);
        this.mesh.castShadow = true;

        scene.add(this.mesh);

        // Add point light to make food glow
        this.light = new THREE.PointLight(COLORS.FOOD, 1, 3);
        this.mesh.add(this.light);
    }

    spawn() {
        const halfGrid = (GRID_SIZE / 2) - 1;
        const x = Math.floor(Math.random() * GRID_SIZE - halfGrid) * CELL_SIZE;
        const z = Math.floor(Math.random() * GRID_SIZE - halfGrid) * CELL_SIZE;

        this.position.set(x, 0, z);
        this.mesh.position.copy(this.position);
    }
}