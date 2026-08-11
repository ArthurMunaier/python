

const CHAVE_TEMA = "painel-tarefas-tema";

function aplicarTema(tema) {
    document.documentElement.setAttribute("data-bs-theme", tema);
    const botao = document.getElementById("btn-modo-escuro");
    if (botao) {
        const icone = botao.querySelector("i");
        icone.className = tema === "dark" ? "bi bi-sun" : "bi bi-moon-stars";
    }
}

function iniciarModoEscuro() {
    const temaSalvo = localStorage.getItem(CHAVE_TEMA) || "light";
    aplicarTema(temaSalvo);

    const botao = document.getElementById("btn-modo-escuro");
    if (!botao) return;

    botao.addEventListener("click", () => {
        const temaAtual = document.documentElement.getAttribute("data-bs-theme");
        const novoTema = temaAtual === "dark" ? "light" : "dark";
        localStorage.setItem(CHAVE_TEMA, novoTema);
        aplicarTema(novoTema);
    });
}

const CORES_POR_STATUS = {
    pendente: "warning",
    andamento: "primary",
    concluida: "success",
};

const LABELS_POR_STATUS = {
    pendente: "Pendente",
    andamento: "Em andamento",
    concluida: "Concluída",
};

function criarCardTarefa(tarefa) {
    const cor = tarefa.status_cor || CORES_POR_STATUS[tarefa.status] || "secondary";
    const label = tarefa.status_label || LABELS_POR_STATUS[tarefa.status] || tarefa.status;

    const col = document.createElement("div");
    col.className = "col-md-6 col-lg-4";
    col.dataset.tarefaCard = tarefa.id;

    col.innerHTML = `
        <div class="card h-100 border-${cor} shadow-sm">
            <div class="card-header bg-${cor} bg-opacity-25 d-flex justify-content-between align-items-center">
                <span class="badge text-bg-${cor}">${label}</span>
                <small class="text-body-secondary">#${tarefa.id}</small>
            </div>
            <div class="card-body">
                <h5 class="card-title">${escaparHtml(tarefa.titulo)}</h5>
                <p class="card-text">${escaparHtml(tarefa.descricao) || "Sem descrição."}</p>
            </div>
            <div class="card-footer bg-transparent d-flex justify-content-between">
                <a href="/editar/${tarefa.id}" class="btn btn-sm btn-outline-primary">
                    <i class="bi bi-pencil-square"></i> Editar
                </a>
                <div class="d-flex gap-2">
                    ${tarefa.status !== "concluida" ? `
                    <button type="button" class="btn btn-sm btn-outline-success btn-concluir" data-id="${tarefa.id}" title="Marcar como concluída">
                        <i class="bi bi-check-lg"></i>
                    </button>` : ""}
                    <button type="button" class="btn btn-sm btn-outline-danger btn-excluir" data-id="${tarefa.id}" title="Excluir">
                        <i class="bi bi-trash"></i>
                    </button>
                </div>
            </div>
        </div>
    `;
    return col;
}

function escaparHtml(texto) {
    const div = document.createElement("div");
    div.textContent = texto || "";
    return div.innerHTML;
}

async function carregarTarefas(status) {
    const lista = document.getElementById("lista-tarefas");
    if (!lista) return;

    const url = status ? `/api/v1/tarefas?status=${encodeURIComponent(status)}` : "/api/v1/tarefas";

    try {
        const resposta = await fetch(url);
        if (!resposta.ok) throw new Error("Falha ao buscar tarefas");
        const tarefas = await resposta.json();

        lista.innerHTML = "";
        if (tarefas.length === 0) {
            lista.innerHTML = '<p class="text-body-secondary fst-italic">Nenhuma tarefa encontrada para esse filtro.</p>';
            return;
        }
        tarefas.forEach((tarefa) => lista.appendChild(criarCardTarefa(tarefa)));
    } catch (erro) {
        console.error(erro);
        lista.innerHTML = '<p class="text-danger">Não foi possível carregar as tarefas agora.</p>';
    }
}

function iniciarFiltroStatus() {
    const filtro = document.getElementById("filtro-status");
    if (!filtro) return;

    filtro.addEventListener("change", () => {
        carregarTarefas(filtro.value);
    });
}

function iniciarAcoesTarefa() {
    const lista = document.getElementById("lista-tarefas");
    if (!lista) return;

    lista.addEventListener("click", async (evento) => {
        const botaoExcluir = evento.target.closest(".btn-excluir");
        const botaoConcluir = evento.target.closest(".btn-concluir");

        if (botaoExcluir) {
            const id = botaoExcluir.dataset.id;
            if (!confirm("Tem certeza que deseja excluir essa tarefa?")) return;

            try {
                const resposta = await fetch(`/api/v1/tarefas/${id}`, { method: "DELETE" });
                if (!resposta.ok) throw new Error("Falha ao excluir");
                const card = lista.querySelector(`[data-tarefa-card="${id}"]`);
                if (card) card.remove();
            } catch (erro) {
                console.error(erro);
                alert("Não foi possível excluir a tarefa. Tente novamente.");
            }
        }

        if (botaoConcluir) {
            const id = botaoConcluir.dataset.id;
            try {
                const resposta = await fetch(`/api/v1/tarefas/${id}`, {
                    method: "PUT",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ status: "concluida" }),
                });
                if (!resposta.ok) throw new Error("Falha ao atualizar");

                
                const filtro = document.getElementById("filtro-status");
                carregarTarefas(filtro ? filtro.value : "");
            } catch (erro) {
                console.error(erro);
                alert("Não foi possível concluir a tarefa. Tente novamente.");
            }
        }
    });
}

document.addEventListener("DOMContentLoaded", () => {
    iniciarModoEscuro();
    iniciarFiltroStatus();
    iniciarAcoesTarefa();
});
