from flask import Blueprint, request, jsonify
from src.handlers.product_handler import (
    get_prodotti,
    crea_prodotto,
    aggiorna_prodotto,
    elimina_prodotto,
    get_totale_prodotti
)

# Blueprint per raggruppare tutte le route dei prodotti
prodotti_bp = Blueprint('prodotti', __name__)


@prodotti_bp.route('/products/count', methods=['GET'])
def conta_totale():
    """GET /products/count — ritorna il numero totale di prodotti nel magazzino."""
    totale = get_totale_prodotti()
    return jsonify({'totale': totale}), 200


@prodotti_bp.route('/products', methods=['GET'])
def lista_prodotti():
    """GET /products — ritorna tutti i prodotti come JSON."""
    prodotti = get_prodotti()
    return jsonify(prodotti), 200


@prodotti_bp.route('/products', methods=['POST'])
def aggiungi_prodotto():
    """POST /products — crea un nuovo prodotto dal body JSON."""
    dati = request.get_json()

    # Verifica che i campi obbligatori siano presenti
    if not dati or 'name' not in dati or 'quantity' not in dati:
        return jsonify({'error': 'Campi name e quantity sono obbligatori'}), 400

    nuovo = crea_prodotto(dati['name'], int(dati['quantity']))
    return jsonify(nuovo), 201


@prodotti_bp.route('/products/<int:product_id>', methods=['PUT'])
def modifica_prodotto(product_id):
    """PUT /products/<id> — aggiorna nome e/o quantità di un prodotto."""
    dati = request.get_json()

    prodotto = aggiorna_prodotto(
        product_id,
        nome=dati.get('name'),
        quantita=dati.get('quantity')
    )

    if prodotto is None:
        return jsonify({'error': 'Prodotto non trovato'}), 404

    return jsonify(prodotto), 200


@prodotti_bp.route('/products/<int:product_id>', methods=['DELETE'])
def cancella_prodotto(product_id):
    """DELETE /products/<id> — elimina un prodotto dal magazzino."""
    eliminato = elimina_prodotto(product_id)

    if not eliminato:
        return jsonify({'error': 'Prodotto non trovato'}), 404

    return jsonify({'message': 'Prodotto eliminato'}), 200
