# 📦 Magazzino API — Guida completa per realizzare il servizio

Questa guida spiega **passo per passo** come costruire il microservizio, cosa fa ogni file e come tenerlo funzionante.

---

## Indice

1. [Cos'è il progetto](#1-cosè-il-progetto)
2. [Struttura delle cartelle](#2-struttura-delle-cartelle)
3. [Setup iniziale](#3-setup-iniziale)
4. [Costruire il backend — fase per fase](#4-costruire-il-backend--fase-per-fase)
5. [Costruire la UI](#5-costruire-la-ui)
6. [Come avviare il server](#6-come-avviare-il-server)
7. [Come testare le API](#7-come-testare-le-api)
8. [Note sui file](#8-note-sui-file)

---

## 1. Cos'è il progetto

Un **microservizio REST** scritto in Python con Flask che gestisce un inventario di prodotti.  
Invece di un database, usiamo un semplice file **CSV** — più semplice da capire e da visualizzare.

Il servizio espone **4 endpoint HTTP** (CRUD):

| Metodo | URL                  | Cosa fa                      |
|--------|----------------------|------------------------------|
| GET    | `/api/products`      | Legge tutti i prodotti       |
| POST   | `/api/products`      | Aggiunge un prodotto         |
| PUT    | `/api/products/<id>` | Modifica un prodotto         |
| DELETE | `/api/products/<id>` | Elimina un prodotto          |

---

## 2. Struttura delle cartelle

Questa è la struttura **esatta** che dobbiamo rispettare:

```
magazzino-api/
├── .env               ← variabili d'ambiente (opzionale)
├── .gitignore         ← esclude file inutili da git
├── requirements.txt   ← dipendenze Python
├── app.py             ← crea l'app Flask e registra le route
├── main.py            ← punto di ingresso alternativo
├── data/
│   └── products.csv   ← il nostro "database"
├── src/
│   ├── routes.py              ← definisce i 4 endpoint HTTP
│   ├── utils.py               ← piccole funzioni di supporto
│   └── handlers/
│       └── product_handler.py ← tutta la logica CRUD sul CSV
├── static/
│   ├── css/
│   │   └── style.css  ← stile della pagina web
│   └── js/
│       └── app.js     ← logica frontend (chiamate API + rendering)
└── templates/
    └── index.html     ← pagina HTML principale
```

---

## 3. Setup iniziale

### 3.1 — Clona o crea la cartella del progetto

```bash
mkdir magazzino-api
cd magazzino-api
```

### 3.2 — Crea un ambiente virtuale Python

L'ambiente virtuale isola le dipendenze del progetto da tutto il resto del sistema.  
È buona pratica farlo **sempre** per ogni nuovo progetto Python.

```bash
# Crea l'ambiente virtuale nella cartella venv/
python3 -m venv venv

# Attivalo (macOS / Linux)
source venv/bin/activate

# Attivalo (Windows)
venv\Scripts\activate
```

Quando è attivo, il terminale mostra `(venv)` prima del prompt.

### 3.3 — Installa le dipendenze

```bash
pip install -r requirements.txt
```

Il file `requirements.txt` contiene solo Flask:

```
flask==3.0.3
```

### 3.4 — Crea la struttura delle cartelle

```bash
mkdir -p data src/handlers static/css static/js templates
```

---

## 4. Costruire il backend — fase per fase

### Fase 1 — Il CSV (`data/products.csv`)

Questo è il nostro "database". Tre colonne: `id`, `name`, `quantity`.

```csv
id,name,quantity
1,Tastiera,15
2,Monitor,8
```

> **Attenzione**: Flask cerca il CSV relativo a dove gira. Il percorso viene calcolato dinamicamente nel handler per evitare problemi.

---

### Fase 2 — La logica sul CSV (`src/handlers/product_handler.py`)

Questo file contiene **4 funzioni** — una per ogni operazione CRUD.  
Non sa nulla di Flask: si occupa solo di leggere e scrivere il CSV.

**Struttura interna:**

```python
def _leggi_csv() -> list[dict]
    # Apre il file, usa csv.DictReader, converte id e quantity in int
    # Ritorna lista di dizionari es: [{'id':1, 'name':'Monitor', 'quantity':8}]

def _scrivi_csv(prodotti)
    # Sovrascrive il CSV con csv.DictWriter
    # Usa sempre writeheader() per mantenere la riga di intestazione

def get_prodotti()       → lista tutti i prodotti
def crea_prodotto()      → genera id incrementale, appende, riscrive
def aggiorna_prodotto()  → trova per id, modifica in memoria, riscrive
def elimina_prodotto()   → filtra fuori il prodotto, riscrive
```

> **Strategia CSV**: leggiamo tutto in memoria, modifichiamo, riscriviamo tutto.  
> Non è performante su file enormi, ma per un magazzino piccolo funziona benissimo.

---

### Fase 3 — Gli endpoint Flask (`src/routes.py`)

Qui usiamo un **Blueprint** di Flask per raggruppare le 4 route.  
Un Blueprint è un modo per organizzare le route senza metterle tutte in `app.py`.

```python
prodotti_bp = Blueprint('prodotti', __name__)
```

Ogni funzione:
1. Riceve la richiesta HTTP
2. Chiama la funzione corretta del handler
3. Ritorna una risposta JSON con il codice di stato appropriato

Codici di stato usati:
- `200 OK` — operazione riuscita
- `201 Created` — prodotto creato
- `400 Bad Request` — dati mancanti o malformati
- `404 Not Found` — prodotto non esistente

---

### Fase 4 — L'app Flask (`app.py`)

```python
app = Flask(__name__)
app.register_blueprint(prodotti_bp, url_prefix='/api')
```

Il `url_prefix='/api'` fa sì che tutti gli endpoint abbiano `/api` davanti.  
Questo è importante per separare le API dalla UI (che risponde su `/`).

---

## 5. Costruire la UI

La UI è opzionale ma molto utile per testare il servizio a colpo d'occhio.

### Come funziona

1. Flask serve `templates/index.html` sulla root `/`
2. La pagina carica `static/css/style.css` e `static/js/app.js`
3. JavaScript fa chiamate `fetch()` alle API e aggiorna la tabella dinamicamente

### Funzionalità UI

- Tabella con tutti i prodotti (si aggiorna automaticamente)
- Quantità basse (≤5) evidenziate in rosso
- Form laterale per aggiungere o modificare un prodotto
- Pulsanti per modificare (riempie il form) o eliminare
- Toast di notifica per ogni operazione riuscita o fallita

---

## 6. Come avviare il server

```bash
# Assicurati di essere nella cartella del progetto con venv attivo
python app.py
```

Output atteso:

```
 * Running on http://127.0.0.1:5000
 * Debug mode: on
```

Apri il browser su `http://localhost:5000` per vedere la UI.

---

## 7. Come testare le API

Puoi usare **curl**, **Postman**, oppure la UI stessa.

### Leggi tutti i prodotti

```bash
curl http://localhost:5000/api/products
```

### Aggiungi un prodotto

```bash
curl -X POST http://localhost:5000/api/products \
  -H "Content-Type: application/json" \
  -d '{"name": "Webcam", "quantity": 3}'
```

### Modifica un prodotto

```bash
curl -X PUT http://localhost:5000/api/products/1 \
  -H "Content-Type: application/json" \
  -d '{"name": "Tastiera meccanica", "quantity": 20}'
```

### Elimina un prodotto

```bash
curl -X DELETE http://localhost:5000/api/products/2
```

---

## 8. Note sui file

| File | Ruolo |
|------|-------|
| `requirements.txt` | Lista le dipendenze — sempre da aggiornare quando aggiungi librerie |
| `.gitignore` | Esclude `venv/`, `__pycache__/`, file `.pyc` dal repository |
| `data/products.csv` | Il file che simula il database — non va escluso da git in questo caso |
| `src/utils.py` | Funzioni generiche riutilizzabili (es. validazione input) |

---

> Progetto realizzato come esercitazione su microservizi REST con Flask.
