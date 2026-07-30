// Configuração Base
const API_BASE = "";

// Mapeamento de Elementos da DOM
const DOM = {
    authSection: document.getElementById('auth-section'),
    dashboardSection: document.getElementById('dashboard-section'),
    loginForm: document.getElementById('login-form'),
    registerForm: document.getElementById('register-form'),
    saldoDisplay: document.getElementById('saldo-display'),
    extratoBody: document.getElementById('extrato-body'),
    toast: document.getElementById('toast'),
    toastMsg: document.getElementById('toast-msg')
};

// Inicialização
window.addEventListener('DOMContentLoaded', () => {
    const token = localStorage.getItem('token');
    if (token) {
        mostrarDashboard();
    }
});

// Sistema de Notificações
function showToast(message, type = 'success') {
    DOM.toastMsg.innerText = message;
    
    // Configura as cores do Tailwind baseadas no tipo
    if (type === 'error') {
        DOM.toast.className = `fixed top-5 right-5 shadow-xl rounded-xl p-4 border-l-4 z-50 bg-rose-50 border-rose-500 text-rose-700 toast-visible`;
    } else {
        DOM.toast.className = `fixed top-5 right-5 shadow-xl rounded-xl p-4 border-l-4 z-50 bg-emerald-50 border-emerald-500 text-emerald-700 toast-visible`;
    }
    
    // Oculta após 4 segundos
    setTimeout(() => {
        DOM.toast.classList.replace('toast-visible', 'toast-hidden');
    }, 4000);
}

// UI: Alternar Login/Cadastro
function toggleAuth() {
    DOM.loginForm.classList.toggle('hidden');
    DOM.registerForm.classList.toggle('hidden');
}

// Autenticação: Login
DOM.loginForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const email = document.getElementById('login-email').value;
    const senha = document.getElementById('login-senha').value;

    try {
        const res = await fetch(`${API_BASE}/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, senha })
        });
        const data = await res.json();

        if (res.ok) {
            localStorage.setItem('token', data.token);
            showToast('Acesso liberado com sucesso!');
            mostrarDashboard();
        } else {
            showToast(data.erro, 'error');
        }
    } catch (error) {
        showToast('Erro ao conectar com a API. Backend está rodando?', 'error');
    }
});

// Autenticação: Cadastro
DOM.registerForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const username = document.getElementById('reg-username').value;
    const email = document.getElementById('reg-email').value;
    const senha = document.getElementById('reg-senha').value;

    try {
        const res = await fetch(`${API_BASE}/cadastrar`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, email, senha })
        });
        const data = await res.json();

        if (res.ok) {
            showToast('Conta criada! Faça login para acessar.');
            toggleAuth();
            DOM.registerForm.reset();
        } else {
            showToast(data.erro, 'error');
        }
    } catch (error) {
        showToast('Erro ao conectar com a API.', 'error');
    }
});

// Dashboard: Controller Principal
async function mostrarDashboard() {
    DOM.authSection.classList.add('hidden');
    DOM.dashboardSection.classList.remove('hidden');
    await carregarDadosDashboard();
}

// Data Fetching: Saldo e Extrato
async function carregarDadosDashboard() {
    const token = localStorage.getItem('token');
    if (!token) return logout();

    const headers = { 'Authorization': `Bearer ${token}` };

    try {
        // Busca Saldo e Trata Token Expirado (401)
        const resSaldo = await fetch(`${API_BASE}/saldo`, { headers });
        if (resSaldo.status === 401) {
            showToast('Sessão expirada. Faça login novamente.', 'error');
            return logout(); 
        }
        
        const dataSaldo = await resSaldo.json();
        const saldoFormatado = new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(dataSaldo.saldo || 0);
        DOM.saldoDisplay.innerText = saldoFormatado;

        // Busca Extrato
        const resExtrato = await fetch(`${API_BASE}/extrato`, { headers });
        const dataExtrato = await resExtrato.json();
        
        renderizarExtrato(dataExtrato.extrato);
    } catch (error) {
        showToast('Falha ao carregar as informações.', 'error');
    }
}

// UI: Renderizar Tabela
function renderizarExtrato(extrato) {
    DOM.extratoBody.innerHTML = '';
    
    if (!extrato || extrato.length === 0) {
        DOM.extratoBody.innerHTML = `
            <tr>
                <td colspan="3" class="py-8 text-center text-slate-400 italic">
                    Nenhuma movimentação registrada até o momento.
                </td>
            </tr>`;
        return;
    }

    extrato.forEach(trans => {
        const isGanho = trans.tipo === 'GANHO';
        const row = document.createElement('tr');
        row.className = 'hover:bg-slate-50 transition-colors duration-150 group';
        
        const valorFormatado = new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(trans.valor);
        
        row.innerHTML = `
            <td class="py-4 text-slate-700 font-medium">${trans.descricao}</td>
            <td class="py-4 text-center">
                <span class="px-3 py-1 text-[10px] font-bold uppercase tracking-wider rounded-full ${isGanho ? 'bg-emerald-100 text-emerald-800' : 'bg-rose-100 text-rose-800'}">
                    ${trans.tipo}
                </span>
            </td>
            <td class="py-4 text-right font-bold ${isGanho ? 'text-emerald-600' : 'text-rose-600'}">
                ${isGanho ? '+' : '-'}${valorFormatado}
            </td>
        `;
        DOM.extratoBody.appendChild(row);
    });
}

// Operação: Nova Transação
document.getElementById('transacao-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const descricao = document.getElementById('trans-desc').value;
    const valor = parseFloat(document.getElementById('trans-valor').value);
    const tipo = document.getElementById('trans-tipo').value;
    const token = localStorage.getItem('token');

    try {
        const res = await fetch(`${API_BASE}/transacao`, {
            method: 'POST',
            headers: { 
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({ descricao, valor, tipo })
        });
        
        const data = await res.json();

        if (res.ok) {
            showToast('Movimentação registrada com sucesso!');
            document.getElementById('transacao-form').reset();
            carregarDadosDashboard(); // Refetch automático e reativo
        } else {
            showToast(data.erro, 'error');
        }
    } catch (error) {
        showToast('Erro ao enviar transação.', 'error');
    }
});

// UI: Logout
function logout() {
    localStorage.removeItem('token');
    DOM.dashboardSection.classList.add('hidden');
    DOM.authSection.classList.remove('hidden');
    DOM.loginForm.reset();
    DOM.registerForm.reset();
}


// Indicador de força de senha — apenas estética/UX no cadastro.
// Regras obrigatórias espelham EXATAMENTE validar_senha() do services_usuario.py
const regSenhaInput = document.getElementById('reg-senha');

if (regSenhaInput) {
    regSenhaInput.addEventListener('input', () => {
        const senha = regSenhaInput.value;

        const criterios = {
            tamanho: senha.length >= 8,
            numero: /\d/.test(senha)
        };
        const bonus = {
            maiuscula: /[A-Z]/.test(senha),
            simbolo: /[^A-Za-z0-9]/.test(senha)
        };

        atualizarChecklist('chk-tamanho', criterios.tamanho);
        atualizarChecklist('chk-numero', criterios.numero);
        atualizarChecklist('chk-maiuscula', bonus.maiuscula);
        atualizarChecklist('chk-simbolo', bonus.simbolo);

        const score = Object.values(criterios).filter(Boolean).length
                    + Object.values(bonus).filter(Boolean).length;

        atualizarBarraForca(score, senha.length);
    });
}

function atualizarChecklist(id, cumprido) {
    const el = document.getElementById(id);
    if (!el) return;
    el.classList.toggle('ok', cumprido); // classList, nunca innerHTML
}

function atualizarBarraForca(score, tamanho) {
    const barra = document.querySelector('.pwd-bar');
    const label = document.getElementById('pwd-label');
    if (!barra || !label) return;

    barra.className = 'pwd-bar';
    label.className = 'pwd-label';

    if (tamanho === 0) {
        label.textContent = '\u00A0';
        return;
    }

    if (score <= 1) {
        barra.classList.add('score-1'); label.classList.add('label-weak'); label.textContent = 'Fraca';
    } else if (score === 2) {
        barra.classList.add('score-2'); label.classList.add('label-ok'); label.textContent = 'Razoável';
    } else if (score === 3) {
        barra.classList.add('score-3'); label.classList.add('label-good'); label.textContent = 'Boa';
    } else {
        barra.classList.add('score-4'); label.classList.add('label-strong'); label.textContent = 'Forte';
    }
}