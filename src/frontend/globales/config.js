// Detecta si estás en local o en producción automáticamente
const API_BASE_URL = window.location.hostname.includes('localhost') || window.location.hostname.includes('127.0.0.1')
    ? 'http://127.0.0.1:8000' // Tu URL local de Django
    : 'https://gestion-academica-del-instituto.onrender.com'; // La URL que Render te dará para el backend
