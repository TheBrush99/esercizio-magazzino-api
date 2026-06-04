# Magazzino API

Un piccolo servizio web per gestire l'inventario di un magazzino.  
Backend in Python + Flask, "database" in CSV, interfaccia web inclusa.

---

## Cosa fa

Espone 4 operazioni su un elenco di prodotti (nome + quantità):

- leggere la lista completa
- aggiungere un prodotto
- modificare un prodotto esistente
- eliminare un prodotto

I dati vivono in un file `products.csv` — niente database, niente configurazioni complicate.

---

## Come è stato costruito

Il progetto segue una separazione netta tra le parti:

**`src/handlers/product_handler.py`**  
È il cuore del backend. Contiene tutta la logica per leggere e scrivere il CSV.  
Non sa nulla di HTTP — fa solo operazioni su file.

**`src/routes.py`**  
Collega Flask alla logica del handler. Ogni endpoint riceve la richiesta, chiama la funzione giusta e risponde con JSON.

**`app.py`**  
Crea l'applicazione Flask, registra le route e serve la pagina web.

**`templates/index.html` + `static/`**  
L'interfaccia grafica. Una pagina HTML con un po' di JavaScript che chiama le API e aggiorna la tabella in tempo reale.

---

## Come si usa

**1. Installa le dipendenze**

```bash
python3 -m venv venv
source venv/bin/activate   # su Windows: venv\Scripts\activate
pip install -r requirements.txt
```

**2. Avvia il server**

```bash
python app.py
```

**3. Apri il browser**

Vai su `http://localhost:5000` per usare la UI, oppure usa le API direttamente:

```
GET    /api/products         → lista prodotti
POST   /api/products         → aggiungi prodotto
PUT    /api/products/<id>    → modifica prodotto
DELETE /api/products/<id>    → elimina prodotto
```

---

## Struttura del progetto

```
magazzino-api/
├── app.py
├── main.py
├── requirements.txt
├── data/
│   └── products.csv
├── src/
│   ├── routes.py
│   ├── utils.py
│   └── handlers/
│       └── product_handler.py
├── static/
│   ├── css/style.css
│   └── js/app.js
└── templates/
    └── index.html
```

---

## Scelte tecniche

- **Flask** invece di FastAPI o Django perché è semplice e basta per questo caso d'uso.
- **CSV come storage** per eliminare dipendenze esterne e rendere il progetto autonomo.
- **Blueprint Flask** per tenere le route separate dall'inizializzazione dell'app — diventa utile quando il progetto cresce.
- **JavaScript vanilla** nella UI, niente React o Vue — una pagina sola con `fetch()` è sufficiente.
