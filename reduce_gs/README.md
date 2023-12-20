Pour exécuter cette application, il est fortement conseillé de créer un environnement virtuel.

## Windows

```powershell
PS C:\Users\gilles\Documents\Python Scripts\pdf> python -m venv .venv
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

Pour afficher l'aide de la commande nous ajoutons le paramètre `-h`.

```powershell
(.venv) PS C:\Users\gilles\Documents\Python Scripts\pdf> python .\reduce_gs\reduce_gs.py -h
usage: reduce_gs.py [-h] [-d DPI] [-v VERSION] [-r REPLACE] source destination

positional arguments:
  source                Dossier source
  destination           Dossier de destination

options:
  -h, --help            show this help message and exit
  -d DPI, --dpi DPI     Points par pouce (défaut=150)
  -v VERSION, --version VERSION
                        Version du document PDF (défaut=1.4)
  -r REPLACE, --replace REPLACE
                        Points par pouce (défaut=150)
```