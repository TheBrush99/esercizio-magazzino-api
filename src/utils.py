# Piccoli helper usati nell'app

def valida_quantita(valore):
    """Controlla che la quantità sia un intero non negativo."""
    try:
        q = int(valore)
        return q >= 0
    except (TypeError, ValueError):
        return False
