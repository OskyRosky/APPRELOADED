import { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [url, setUrl] = useState('');
  const [progress, setProgress] = useState(0);
  const [mensaje, setMensaje] = useState('');
  const [mensajes, setMensajes] = useState([]);

  // Conexión WebSocket
  useEffect(() => {
    const socket = new WebSocket("ws://localhost:8001/ws");

    socket.onopen = () => {
      console.log("✅ Conectado al WebSocket");
    };

    socket.onmessage = (event) => {
      setMensajes(prev => [...prev, event.data]);
    };

    socket.onerror = (error) => {
      console.error("❌ Error WebSocket:", error);
    };

    return () => {
      socket.close();
    };
  }, []);

  const handleDownload = async (e) => {
    e.preventDefault();

    setProgress(0);
    setMensaje('');
    setMensajes([]); // Limpiar mensajes antes de nueva descarga

    try {
      const response = await fetch("http://127.0.0.1:8001/descargar", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ url, ruta: "/Users/sultan/Downloads/testdescarga" }), // puedes reemplazar la ruta después
      });

      const data = await response.json();
      setMensaje(data.status);

      // Progreso simulado (opcional)
      const interval = setInterval(() => {
        setProgress(prev => {
          if (prev >= 100) {
            clearInterval(interval);
            return 100;
          }
          return prev + 10;
        });
      }, 300);
    } catch (error) {
      console.error("Error en la descarga:", error);
      setMensaje("❌ Ocurrió un error en la descarga");
    }
  };

  return (
    <div className="container">
      <h1>📥 Módulo de Descarga SIGED Reloaded</h1>
      <form onSubmit={handleDownload}>
        <label>🔗 URL del SIGED/ZHED:</label><br />
        <input 
          type="text" 
          value={url} 
          onChange={(e) => setUrl(e.target.value)} 
          required 
          placeholder="https://..." 
        /><br /><br />

        <label>📁 Carpeta de destino:</label><br />
        <input 
          type="text" 
          disabled 
          placeholder="(Selector de carpeta no disponible aún)" 
        /><br /><br />

        <button type="submit">Iniciar Descarga</button>
      </form>

      <div className="progress-section">
        <label>Progreso:</label>
        <div className="progress-bar">
          <div className="progress-fill" style={{ width: `${progress}%` }}></div>
        </div>
        <p>{progress}%</p>
        <p>{mensaje}</p>
      </div>

      <div className="log-container">
        <h3>📝 Estado de la descarga:</h3>
        <pre style={{ whiteSpace: 'pre-wrap', backgroundColor: '#222', color: '#0f0', padding: '10px', borderRadius: '8px', maxHeight: '300px', overflowY: 'scroll' }}>
          {mensajes.join("\n")}
        </pre>
      </div>
    </div>
  );
}

export default App;