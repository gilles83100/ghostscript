# Installation du script Python

## Windows

Pour exécuter cette application, il est fortement conseillé de créer un environnement virtuel.

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
python-utils      3.8.1
setuptools        65.5.0
```

Pour fonctionner ce script a besoin de bibliothèques auxiliaires. Nous pouvons les installer directement par une commande `pip`.

```bash
python install alive-progress
```
Nous pouvons aussi utiliser un fichier texte que nous appelerons `requirements.txt` auquel nous ajouterons la ligne suivante :

```python
alive-progress==3.1.5
```

Pour installer les bibliothèques, nous utiliserons le fichier `requirements.txt` avec la commande `pip`.

```powershell
(.venv) PS C:\Users\gilles\Documents\Python Scripts\pdf> pip install -r requirements.txt
```

## Mac OS

# Utilisation

Pour afficher l'aide de la commande nous ajoutons le paramètre `-h`.

```powershell
(.venv) PS C:\Users\gilles\Documents\Python Scripts\pdf> python .\reduce_gs\reduce_gs.py -h
usage: reduce_gs.py [-h] [-d DPI] [-v VERSION] [-r REPLACE] source destination

Réduction de la taille des fichiers PDF

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

Pour fonctionner nous devons a minima préciser un dossier source et un dossier destination. Avec le script Python, nous procéderons comme suit :

```bash
python reduce_gs.py ~/Documents/Factures /Users/gilles/Factures
```

Avec le fichier exécutable, l'utilisation de la commande sera :

```powershell
reduce_gs.exe ~/Documents/Factures /Users/gilles/Factures
```

Avec le paramètre `-r` nous pouvons choisir de ne pas remplacer les fichiers existants dans le dossier destination. 

```powershell
python reduce_gs.py  "C:\Users\gilles\OneDrive\Documents\Factures\" "C:\Users\gilles\Documents\Factures\" -r non
```

Pour modifier la densité de points par pouce nous utiliserons le paramètre `-d` suivi de la valeur désirée. Rappelons nous que plus la valeur est basse, plus la qualité des images est dégradrée. Inversement, il est inutile d'augmenter les DPI au delà de la valeur utilisée par les images sources. 

> Dans Windows, l'accès a un disque réseau nécessite dans Powershell de se connecter avec des identifiants valides. Pour cela nous devons au préalable lancer la ligne sui suit :
> ```powershell
> net use \\192.168.1.14\mondisque /user:gilles
> ```
