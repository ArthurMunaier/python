

const LABELS = {
    pendente: "Pendente",
    andamento: "Em andamento",
    concluida: "Concluída",
};

const CORES = {
    pendente: "#f0ad4e", 
    andamento: "#0d6efd", 
    concluida: "#198754", 
};

async function carregarProgresso() {
    try {
        const resposta = await fetch("/api/v1/progresso");
        if (!resposta.ok) throw new Error("Falha ao buscar progresso");
        const contagem = await resposta.json();

        const chaves = Object.keys(contagem);
        const total = chaves.reduce((soma, chave) => soma + contagem[chave], 0);

        if (total === 0) {
            document.getElementById("progresso-vazio").classList.remove("d-none");
        }

        const labels = chaves.map((chave) => LABELS[chave] || chave);
        const valores = chaves.map((chave) => contagem[chave]);
        const cores = chaves.map((chave) => CORES[chave] || "#6c757d");

        new Chart(document.getElementById("grafico-barras"), {
            type: "bar",
            data: {
                labels,
                datasets: [{ label: "Tarefas", data: valores, backgroundColor: cores }],
            },
            options: {
                responsive: true,
                plugins: { legend: { display: false } },
                scales: { y: { beginAtZero: true, ticks: { stepSize: 1 } } },
            },
        });

        new Chart(document.getElementById("grafico-pizza"), {
            type: "pie",
            data: {
                labels,
                datasets: [{ data: valores, backgroundColor: cores }],
            },
            options: { responsive: true },
        });
    } catch (erro) {
        console.error(erro);
    }
}

document.addEventListener("DOMContentLoaded", carregarProgresso);
