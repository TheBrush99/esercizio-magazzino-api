# 🚀 Come Avviare il Progetto

Questa guida ti spiega come avviare il server Flask sul tuo computer sia manualmente che in modo automatico.

---

## 🚀 Metodo 1: Avvio Rapido (Consigliato)

Ho creato un file chiamato `avvia.bat` nella cartella principale del progetto. 

1. Fai doppio clic sul file **`avvia.bat`**.
2. Il terminale si aprirà da solo, attiverà l'ambiente virtuale (`venv`) e avvierà il server.
3. Apri il browser all'indirizzo: [http://localhost:5000](http://localhost:5000)
4. Per spegnere il server, chiudi semplicemente la finestra del terminale o premi `CTRL + C` nel terminale.

---

## 💻 Metodo 2: Avvio Manuale da PowerShell / Prompt

Se preferisci avviarlo manualmente tramite riga di comando:

1. **Apri il terminale** (PowerShell o CMD) e spostati nella cartella del progetto:
   ```powershell
   cd C:\Users\A1621apulia\Desktop\esercizio-magazzino-api
   ```

2. **Attiva l'ambiente virtuale** (`venv`):
   ```powershell
   .\venv\Scripts\activate
   ```
   *(Noterai la scritta `(venv)` all'inizio del prompt del terminale).*

3. **Avvia il server Flask**:
   ```powershell
   python app.py
   ```

4. Apri il browser all'indirizzo: [http://localhost:5000](http://localhost:5000) oppure http://127.0.0.1:5000
