import "./App.css";
import { useEffect, useState } from "react";
import axios from "axios";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer
} from "recharts";

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
  const [history, setHistory] = useState([]);

  useEffect(() => {
    const cargarDashboard = () => {
      axios
        .get("http://127.0.0.1:5000/api/dashboard")
        .then((res) => setData(res.data))
        .catch((err) => console.log(err))
        .get("http://127.0.0.1:5000/api/history")
        .then((res) => setHistory(res.data));
    };

    cargarDashboard();

    const intervalo = setInterval(() => {
      cargarDashboard();
    }, 5000);

    return () => clearInterval(intervalo);
  }, []);

  const ejecutarScan = async () => {
    if (!ip) return;

    setLoading(true);
    setScan(null);

    try {
      const res = await axios.post("http://127.0.0.1:5000/api/scan", {
        ip: ip
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
          <>
            {/* HERO SECTION */}
            <section className="hero-grid">
              <div className="panel hero-score">
                <h3>🧠 Security Score IA</h3>

                <div className="score-box">
                  <div className="quantum-score">
                    <div className="ring">
                      <div className="core">
                        <h1>{scan.score}</h1>
                        <span>/100</span>
                      </div>
                    </div>
                  </div>

                  <p>
                    {scan.score >= 85
                      ? "🟢 Excelente"
                      : scan.score >= 65
                      ? "🟡 Riesgo Medio"
                      : "🔴 Crítico"}
                  </p>
                </div>
              </div>

              <div className="panel hero-map">
                <h3>🌍 Quantum Threat Grid</h3>

                <div className="world-map">
                  <span className="node usa"></span>
                  <span className="node colombia"></span>
                  <span className="node europe"></span>
                  <span className="node asia"></span>
                  <span className="node brazil"></span>

                  <span className="beam beam1"></span>
                  <span className="beam beam2"></span>
                  <span className="beam beam3"></span>
                </div>
              </div>
            </section>

            {/* MID SECTION */}
            <section className="hero-grid">
              <div className="panel">
                <h3>📊 Puertos Detectados</h3>

                <ResponsiveContainer width="100%" height={280}>
                  <BarChart
                    data={scan.puertos.map((p) => ({
                      puerto: p,
                      valor: 1
                    }))}
                  >
                    <XAxis dataKey="puerto" />
                    <YAxis hide />
                    <Tooltip />
                    <Bar
                      dataKey="valor"
                      fill="#38bdf8"
                      radius={[8, 8, 0, 0]}
                    />
                  </BarChart>
                </ResponsiveContainer>
              </div>

              <div className="panel">
                <h3>🧠 AI Vulnerability Advisor</h3>

                <ul>
                  {scan.riesgos.map((r, i) => {
                    let texto =
                      "Monitorear servicio y aplicar buenas prácticas.";

                    if (r.includes("22")) {
                      texto =
                        "SSH expuesto. Use llaves SSH, limite IPs y desactive root login.";
                    } else if (r.includes("21")) {
                      texto =
                        "FTP inseguro. Migrar a SFTP o FTPS inmediatamente.";
                    } else if (r.includes("3306")) {
                      texto =
                        "MySQL expuesto. Restringir acceso externo y usar firewall.";
                    } else if (r.includes("80")) {
                      texto =
                        "HTTP detectado. Forzar HTTPS y revisar headers.";
                    } else if (r.includes("443")) {
                      texto =
                        "HTTPS activo. Validar TLS moderno.";
                    }

                    return <li key={i}>{texto}</li>;
                  })}
                </ul>
              </div>
            </section>

            {/* BOTTOM */}
            <section className="panels">
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
            </section>
          </>
        )}
      </main>

      <div className="panel">
        <h3>📜 Últimos Escaneos</h3>

        <table className="history-table">
          <thead>
            <tr>
              <th>IP</th>
              <th>Score</th>
              <th>Puertos</th>
              <th>Fecha</th>
            </tr>
          </thead>

          <tbody>
            {history.map((item, i) => (
              <tr key={i}>
                <td>{item.ip}</td>
                <td>{item.score}</td>
                <td>{item.puertos}</td>
                <td>{item.fecha}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      
    </div>
  );
}