import { io } from 'socket.io-client';

// "undefined" means the URL will be computed from the `window.location` object

export const socket = io('http://localhost:5000', {
    transports: ['websocket'], // Force WebSocket transport
    upgrade: false, // Disable protocol upgrades
    autoConnect: false
});
