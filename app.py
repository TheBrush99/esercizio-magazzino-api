from flask import Flask, render_template
from src.routes import prodotti_bp

# Creiamo l'istanza Flask e registriamo le route
app = Flask(__name__)
app.register_blueprint(prodotti_bp, url_prefix='/api')


@app.route('/')
def index():
    """Pagina principale con la UI del magazzino."""
    return render_template('index.html')


if __name__ == '__main__':
    # debug=True ci fa vedere gli errori in chiaro durante lo sviluppo
    app.run(debug=True, port=5000)
