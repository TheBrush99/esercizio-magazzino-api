@echo off
echo ===================================================
echo   Avvio del Server Flask: Magazzino API
echo ===================================================
echo.

:: Controlla se la cartella venv esiste
if not exist "venv" (
    echo [ERRORE] L'ambiente virtuale (cartella venv) non esiste!
    echo Assicurati di aver creato il venv come descritto in AVVIA_PROGETTO.md.
    pause
    exit /b
)

echo [*] Attivazione ambiente virtuale venv...
call venv\Scripts\activate.bat

echo [*] Avvio del server Flask...
python app.py

echo.
echo [!] Il server e stato spento.
pause
