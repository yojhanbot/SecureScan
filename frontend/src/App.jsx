import "./App.css";
import { useEffect, useState } from "react";
import axios from "axios";

function KPI({ title, value, sub }) {
  return (
    <div className="card">
      <p className="card-title">{title}</p>
      <h2>{value}</h2>
      <span>{sub}</span>
    </div>
  );
}

export default function App() {
  const [data, setData] = useState(null);
  const [ip, setIp] = useState("");
  const [loading, setLoading] = useState(false);
  const [scan, setScan] = useState(null);

  useEffect(() => {
    axios
      .get("http://127.0.0.1:5000/api/dashboard")
      .then((res) => setData(res.data));
  }, []);

  const ejecutarScan = async () => {
    if (!ip) return;

    setLoading(true);
    setScan(null);

    try {
      const res = await axios.post("http://127.0.0.1:5000/api/scan", {
        ip: ip,
      });

      setScan(res.data);
    } catch (error) {
      alert("Error escaneando");
    }

    setLoading(false);
  };

  if (!data) return <h1 style={{ padding: "40px" }}>Cargando...</h1>;

  return (
    <div className="layout">

      <aside className="sidebar">
        <h1>🛡 SecureScan X</h1>

        <nav>
          <a href="#">Dashboard</a>
          <a href="#">Scanner</a>
          <a href="#">Threats</a>
          <a href="#">Reports</a>
        </nav>
      </aside>

      <main className="main">

        <header className="topbar">
          <div>
            <h2>Cyber Intelligence Center</h2>
            <p>Escaneo en tiempo real</p>
          </div>
        </header>

        <section className="grid">
          <KPI title="Riesgos" value={data.riesgos_criticos} sub="Live" />
          <KPI title="Hosts" value={data.hosts} sub="Activos" />
          <KPI title="Score" value={data.score + "/100"} sub="IA" />
          <KPI title="Eventos" value={data.eventos} sub="Hoy" />
        </section>

        <div className="panel">
          <h3>🔎 Ejecutar Escaneo</h3>

          <input
            className="scan-input"
            type="text"
            placeholder="Ej: scanme.nmap.org"
            value={ip}
            onChange={(e) => setIp(e.target.value)}
          />

          <button className="scan-btn" onClick={ejecutarScan}>
            Escanear
          </button>

          {loading && (
            <div className="loading-box">
              <p>⚡ Escaneando infraestructura...</p>

              <div className="progress-bar">
                <div className="progress-fill"></div>
              </div>
            </div>
    )}
        </div>

        {scan && (
          <div className="panels">

            <div className="panel">
              <h3>🚨 Riesgos Detectados</h3>

              <ul>
                {scan.riesgos.map((r, i) => (
                  <li key={i}>{r}</li>
                ))}
              </ul>
            </div>

            <div className="panel">
              <h3>💡 Recomendaciones</h3>

              <ul>
                {scan.recomendaciones.map((r, i) => (
                  <li key={i}>{r}</li>
                ))}
              </ul>
            </div>

          </div>
        )}

      </main>
    </div>
  );
}