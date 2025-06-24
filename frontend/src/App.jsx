import { useState } from 'react'
import './App.css'

function App() {
  const [url, setUrl] = useState('');
  const [progress, setProgress] = useState(0);
  const [mensaje, setMensaje] = useState('');

  const handleDownload = async (e) => {
    e.preventDefault();

    setProgress(0);
    setMensaje('');

    try {
      const response = await fetch("http://127.0.0.1:8000/descargar", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ url }),
      });

      const data = await response.json();
      setMensaje(data.status);

      // Simular progreso visual
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
    </div>
  );
}

export default App;