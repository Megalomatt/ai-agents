import * as THREE from 'three';
import { COLORS } from '../utils/Constants.js';

export class SceneManager {
    constructor() {
        this.scene = new THREE.Scene();
        this.camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
        this.renderer = new THREE.WebGLRenderer({
            canvas: document.getElementById('game-canvas'),
            antialias: true
        });

        this.init();
        this.setupLights();
        this.setupGrid();
        this.handleResize();
    }

    init() {
        this.renderer.setSize(window.innerWidth, window.innerHeight);
        this.renderer.shadowMap.enabled = true;
        this.camera.position.set(15, 15, 15);
        this.camera.lookAt(0, 0, 0);

        window.addEventListener('resize', this.handleResize.bind(this));
    }

    setupLights() {
        const ambientLight = new THREE.AmbientLight(COLORS.AMBIENT_LIGHT, 0.6);
        this.scene.add(ambientLight);

        const directionalLight = new THREE.DirectionalLight(COLORS.DIRECTIONAL_LIGHT, 0.8);
        directionalLight.position.set(10, 20, 10);
        directionalLight.castShadow = true;
        this.scene.add(directionalLight);
    }

    setupGrid() {
        const gridHelper = new THREE.GridHelper(20, 20, COLORS.GRID, COLORS.GRID);
        this.scene.add(gridHelper);

        // Add ground plane
        const groundGeometry = new THREE.PlaneGeometry(20, 20);
        const groundMaterial = new THREE.MeshStandardMaterial({
            color: 0x333333,
            transparent: true,
            opacity: 0.5
        });
        const ground = new THREE.Mesh(groundGeometry, groundMaterial);
        ground.rotation.x = -Math.PI / 2;
        ground.receiveShadow = true;
        this.scene.add(ground);
    }

    handleResize() {
        const width = window.innerWidth;
        const height = window.innerHeight;
        this.camera.aspect = width / height;
        this.camera.updateProjectionMatrix();
        this.renderer.setSize(width, height);
    }

    render() {
        this.renderer.render(this.scene, this.camera);
    }
} 