// =====================================================
// Magazzino API — Frontend JS
// Gestisce le chiamate alle API e aggiorna la UI
// =====================================================

const BASE = '/api';

// Teniamo in memoria l'id del prodotto che stiamo modificando (null = modalità creazione)
let editingId = null;

// --- Utility: mostra un toast a schermo ---
function toast(msg, tipo = 'ok') {
  const el = document.getElementById('toast');
  el.textContent = msg;
  el.className = `show ${tipo}`;
  setTimeout(() => { el.className = ''; }, 2800);
}

// --- Carica e mostra tutti i prodotti ---
async function caricaProdotti() {
  const res = await fetch(`${BASE}/products`);
  const prodotti = await res.json();
  renderTabella(prodotti);
}

// --- Costruisce le righe della tabella ---
function renderTabella(prodotti) {
  const tbody = document.getElementById('tbody');

  if (prodotti.length === 0) {
    tbody.innerHTML = `<tr><td colspan="4" class="empty">— Nessun prodotto nel magazzino —</td></tr>`;
    return;
  }

  tbody.innerHTML = prodotti.map(p => {
    const qtyClass = p.quantity <= 5 ? 'low' : 'ok';
    return `
      <tr>
        <td class="id">#${p.id}</td>
        <td>${p.name}</td>
        <td class="qty ${qtyClass}">${p.quantity}</td>
        <td>
          <div class="btn-row">
            <button class="btn-icon" onclick="avviaModifica(${p.id}, '${p.name}', ${p.quantity})" title="Modifica">✎</button>
            <button class="btn-icon del" onclick="eliminaProdotto(${p.id})" title="Elimina">✕</button>
          </div>
        </td>
      </tr>
    `;
  }).join('');
}

// --- Gestisce il submit del form (crea o aggiorna) ---
async function submitForm() {
  const nome = document.getElementById('inp-nome').value.trim();
  const qty  = document.getElementById('inp-qty').value;

  if (!nome || qty === '') {
    toast('Compila tutti i campi', 'err');
    return;
  }

  if (editingId !== null) {
    // Modalità UPDATE
    const res = await fetch(`${BASE}/products/${editingId}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name: nome, quantity: parseInt(qty) })
    });

    if (res.ok) {
      toast(`Prodotto #${editingId} aggiornato`);
      resetForm();
      caricaProdotti();
    } else {
      toast('Errore durante la modifica', 'err');
    }

  } else {
    // Modalità CREATE
    const res = await fetch(`${BASE}/products`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name: nome, quantity: parseInt(qty) })
    });

    if (res.ok) {
      toast('Prodotto aggiunto!');
      resetForm();
      caricaProdotti();
    } else {
      toast('Errore durante l\'inserimento', 'err');
    }
  }
}

// --- Prepopola il form per la modifica ---
function avviaModifica(id, nome, qty) {
  editingId = id;
  document.getElementById('inp-nome').value = nome;
  document.getElementById('inp-qty').value  = qty;
  document.getElementById('form-title').textContent = `Modifica #${id}`;
  document.getElementById('btn-submit').textContent = 'Aggiorna prodotto';
  document.getElementById('btn-reset').style.display = 'block';
}

// --- Elimina un prodotto dopo conferma ---
async function eliminaProdotto(id) {
  if (!confirm(`Eliminare il prodotto #${id}?`)) return;

  const res = await fetch(`${BASE}/products/${id}`, { method: 'DELETE' });

  if (res.ok) {
    toast(`Prodotto #${id} eliminato`, 'ok');
    caricaProdotti();
  } else {
    toast('Prodotto non trovato', 'err');
  }
}

// --- Resetta il form alla modalità creazione ---
function resetForm() {
  editingId = null;
  document.getElementById('inp-nome').value = '';
  document.getElementById('inp-qty').value  = '';
  document.getElementById('form-title').textContent = 'Aggiungi prodotto';
  document.getElementById('btn-submit').textContent = 'Inserisci prodotto';
  document.getElementById('btn-reset').style.display = 'none';
}

// Carica i prodotti al caricamento della pagina
document.addEventListener('DOMContentLoaded', caricaProdotti);
