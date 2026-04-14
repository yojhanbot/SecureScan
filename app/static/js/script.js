document.addEventListener("DOMContentLoaded", function () {

    const canvas = document.getElementById("graficaRiesgos");

    if (canvas) {

        const datos = JSON.parse(canvas.dataset.valores);

        const ctx = canvas.getContext("2d");

        new Chart(ctx, {
            type: "bar",
            data: {
                labels: ["Alto", "Medio", "Bajo"],
                datasets: [{
                    label: "Nivel de Riesgo",
                    data: datos,
                    backgroundColor: [
                        "#ef4444",
                        "#facc15",
                        "#22c55e"
                    ]
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        labels: {
                            color: "white"
                        }
                    }
                },
                scales: {
                    x: {
                        ticks: { color: "white" }
                    },
                    y: {
                        ticks: { color: "white" }
                    }
                }
            }
        });
    }

    function actualizarAlertas() {

    fetch("/alertas")
        .then(res => res.json())
        .then(data => {

            const lista = document.getElementById("lista-alertas");

            if (!lista) return;

            lista.innerHTML = "";

            data.forEach(alerta => {
                const li = document.createElement("li");
                li.textContent = alerta;
                li.style.color = "#ef4444";
                lista.appendChild(li);
            });

        });
}

// cada 5 segundos 
setInterval(actualizarAlertas, 5000);

});