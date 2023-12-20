Pour exécuter cette application, il est fortement conseillé de créer un environnement virtuel.

## Windows

```powershell
python -m venv .venv
```

Pour activer l'environnement dans Powershell nous écrirons les commandes suivantes :

```powershell
PS C:\Users\gilles\Documents\Python Scripts\pdf> .\.venv\Scripts\Activate.ps1
(.venv) PS C:\Users\gilles\Documents\Python Scripts\pdf> pip list
Package           Version
----------------- -------
pip               23.3.2
progressbar2      4.3.2
python-utils      3.8.1
setuptools        65.5.0
typing_extensions 4.9.0
```

Pour installer les bibliothèques, nous utiliserons le fichier `requirements.txt` avec la commande `pip`.

```powershell
(.venv) PS C:\Users\gilles\Documents\Python Scripts\pdf> pip install -r requirements.txt
```