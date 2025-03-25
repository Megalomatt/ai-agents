export const GRID_SIZE = 20;
export const CELL_SIZE = 1;
export const MOVE_INTERVAL = 200; // Slightly slower for smoother movement
export const INITIAL_SNAKE_LENGTH = 3;

export const COLORS = {
    SNAKE_HEAD: 0x00ff00,
    SNAKE_BODY: 0x008800,
    FOOD: 0xff0000,
    GRID: 0x444444,
    AMBIENT_LIGHT: 0xffffff,
    DIRECTIONAL_LIGHT: 0xffffff
};

export const KEYS = {
    UP: ['ArrowUp', 'w', 'W'],
    DOWN: ['ArrowDown', 's', 'S'],
    LEFT: ['ArrowLeft', 'a', 'A'],
    RIGHT: ['ArrowRight', 'd', 'D']
};