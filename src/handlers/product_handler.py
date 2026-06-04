import csv
import os

# Percorso del file CSV dove salviamo i prodotti
CSV_PATH = os.path.join(os.path.dirname(__file__), '../../data/products.csv')
CSV_FIELDS = ['id', 'name', 'quantity']


def _leggi_csv():
    """Legge il CSV e ritorna una lista di dizionari."""
    prodotti = []
    try:
        with open(CSV_PATH, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for riga in reader:
                # Convertiamo id e quantity in interi
                prodotti.append({
                    'id': int(riga['id']),
                    'name': riga['name'],
                    'quantity': int(riga['quantity'])
                })
    except FileNotFoundError:
        # Se il file non esiste, ritorniamo lista vuota
        pass
    return prodotti


def _scrivi_csv(prodotti):
    """Sovrascrive il CSV con la lista di prodotti aggiornata."""
    with open(CSV_PATH, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=CSV_FIELDS)
        writer.writeheader()
        writer.writerows(prodotti)


def get_prodotti():
    """Ritorna tutti i prodotti dal CSV."""
    return _leggi_csv()


def crea_prodotto(nome, quantita):
    """Aggiunge un nuovo prodotto e ritorna quello creato."""
    prodotti = _leggi_csv()

    # Generiamo un id incrementale: prendiamo il massimo id presente + 1
    nuovo_id = max((p['id'] for p in prodotti), default=0) + 1

    nuovo = {
        'id': nuovo_id,
        'name': nome,
        'quantity': quantita
    }
    prodotti.append(nuovo)
    _scrivi_csv(prodotti)
    return nuovo


def aggiorna_prodotto(product_id, nome=None, quantita=None):
    """Modifica un prodotto esistente. Ritorna il prodotto aggiornato o None se non trovato."""
    prodotti = _leggi_csv()

    for p in prodotti:
        if p['id'] == product_id:
            # Aggiorniamo solo i campi che ci vengono passati
            if nome is not None:
                p['name'] = nome
            if quantita is not None:
                p['quantity'] = quantita
            _scrivi_csv(prodotti)
            return p

    # Prodotto non trovato
    return None


def elimina_prodotto(product_id):
    """Rimuove un prodotto dal CSV. Ritorna True se eliminato, False se non trovato."""
    prodotti = _leggi_csv()
    prodotti_filtrati = [p for p in prodotti if p['id'] != product_id]

    if len(prodotti_filtrati) == len(prodotti):
        # Nessun prodotto rimosso, id non esisteva
        return False

    _scrivi_csv(prodotti_filtrati)
    return True
