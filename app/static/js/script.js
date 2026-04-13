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

});