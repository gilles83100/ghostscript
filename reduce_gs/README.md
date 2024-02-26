# Interfacer Ghostscript avec Python

Ghostscript dans sa version exécutable binaire est utilisé avec Python pour manipuler les fichiers PDF. Le script proposé va convertir par lot un dossier complet vers un dossier de destination.

## Installation du script Python

### Windows

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

```powershell
(.venv) PS C:\Users\gilles\Documents\Python Scripts\pdf> python install tqdm tabulate
```

Nous pouvons aussi utiliser un fichier texte que nous appelerons `requirements.txt` auquel nous ajouterons la ligne suivante :

```python
tqdm==4.66.2
tabulate
```

Pour installer les bibliothèques, nous utiliserons le fichier `requirements.txt` avec la commande `pip`.

```powershell
(.venv) PS C:\Users\gilles\Documents\Python Scripts\pdf> pip install -r requirements.txt
```

### Mac OS

Dans le système d'Apple nous allons utiliser l'environnement Python _Conda_. Nous pouvons utiliser les distributions _Anaconda_ ou Miniconda pour utiliser _Conda_. Elles sont compatibles avec tous les systèmes d'exploitation (Windows, Mac Os ou Linux). Cela permet une meilleure intégration d'un environnement de travail Python.

Une fois installée, nous allons travailler dans des environnements virtuels. Pour obtenir la liste des environnements présents sur le système, nous utiliserons dans le Terminal les instructions qui suivent :

```bash
% conda env list
```

ou

```bash
% conda info --envs
```

Nous pouvons également obtenir des informations sur l'environnement. Ici, nous sommes en présence d'un environnement sous Mac OS Silicon (arm).

```bash
% conda info
	active environment : base
	active env location : /Users/gilles/opt/anaconda3
	shell level : 1
	user config file : /Users/gilles/.condarc
	populated config files : /Users/gilles/.condarc
	conda version : 4.13.0
	conda-build version : 3.21.8
	python version : 3.9.12.final.0
	virtual packages : __osx=13.3.1=0
	__unix=0=0
	__archspec=1=arm64
	base environment : /Users/gilles/opt/anaconda3  (writable)
	conda av data dir : /Users/gilles/opt/anaconda3/etc/conda
	conda av metadata url : None
	channel URLs : https://repo.anaconda.com/pkgs/main/osx-arm64
	https://repo.anaconda.com/pkgs/main/noarch
	https://repo.anaconda.com/pkgs/r/osx-arm64
	https://repo.anaconda.com/pkgs/r/noarch
	package cache : /Users/gilles/opt/anaconda3/pkgs
	/Users/gilles/.conda/pkgs
	envs directories : /Users/gilles/opt/anaconda3/envs
	/Users/gilles/.conda/envs
	platform : osx-arm64
	user-agent : conda/4.13.0 requests/2.27.1 CPython/3.9.12 Darwin/22.4.0 OSX/13.3.1
	UID:GID : 501:20
	netrc file : None
	offline mode : False
```

L'environnement de développement Python peut être mis à jour.

```bash
% conda update conda
```

Si nous utilisons la distribution _Anaconda_, nous pouvons également utiliser la commande suivante :

```bash
% conda update anaconda
```

Pour développer, nous devons créer un environnement virtuel. Pour cela, nous utilisons la commande create, suivi de l'argument `-n` pour donner un nom à l'environnement. Optionnellement, nous pouvons définir la version de Python à installer.

```bash
% conda create -n reduce_pdf python=3.11
```

ou

```bash
% conda create --name reduce_pdf python=3.11
```

Nous pouvons également intégrer des bibliothèques à la création de l'environnement. `-c conda-forge` est utilisé pour définir le dépôt de bibliothèque à utiliser.

```bash
% conda create -n reduce_pdf -c conda-forge python=3.11 tqdm tabulate
```

Une bibliothèque peut être installée par la suite lorsque l'environnement est en cours d'utilisation.

```bash
% conda install -c conda-forge tqdm tabulate
```

Si nous souhaitons mettre à jour un package spécifique nous utiliserons la commande `update` suivi du ou des noms de packages.

```bash
% conda update tdqm
```

Les dépendances (packages) sont également mises à jour. Tout est automatique, il n'est pas nécessaire de s'en inquiéter. `update` propose quelques options supplémentaires :

* `--no-deps` pour ne pas mettre à jour les dépendances
* `--force-reinstall` pour forcer la mise à jour même si le package est à jour
* `--dry-run` pour simuler la mise à jour
* `--yes` pour répondre automatiquement oui à toute question

La mise à jour de tous les packages d'un environnement se fait de cette manière.

```bash
% conda update -all
```

L'utilisation d'un environnement nécessite son activation. Pour faire cela, nous avons la commande :

```bash
% conda activate reduce_pdf
```

Pour quitter l'environnement nous procéderons comme suit :

```bash
% conda deactivate
```

Pour supprimer un environnement de développement :

```bash
% conda env remove --name reduce_pdf
```

Pour supprimer tous les environnements à un emplacement spécifique, nous utiliserons l'argument `--prefix`.

```bash
%  conda env remove --prefix /Users/gilles/envs
```

## Utilisation

Pour afficher l'aide de la commande nous ajoutons le paramètre `-h`.

```bash
(.venv) gilles@MacStuddeGilles reduce_gs % python reduce_gs.py 
usage: reduce_gs.py [-h] [-d DPI] [-p PASSWORD] [-v VERSION] [-r {o,oui,y,yes,n,non,no}] [-k {LeaveColorUnchanged,Gray,RGB,CMYK}] [-z {LZW,Flate,jpeg,RLE}] [-m {Subsample,Average,Bicubic}]
                    [-e {a0,a1,a2,a3,a4,a4small,a5,a6,a7,a8,a9,a10,isob0,isob1,isob2,isob3,isob4,isob5,isob6,c0,c1,c2,c3,c4,c5,c6,11x17,ledger,legal,letter,lettersmall,arche,archd,archc,archb,archa,jisb0,jisb1,jisb2,jisb3,jisb4,jisb5,jisb6,flsa,flse,halfletter,hagaki}]
                    [-s {ebook,printer,default,prepress,screen,PSL2Printer}] [-c CSV] [-o DESTINATION]
                    source
reduce_gs.py: error: the following arguments are required: source
(.venv) gilles@MacStuddeGilles reduce_gs % python reduce_gs.py -h
usage: reduce_gs.py [-h] [-d DPI] [-p PASSWORD] [-v VERSION] [-r {o,oui,y,yes,n,non,no}] [-k {LeaveColorUnchanged,Gray,RGB,CMYK}] [-z {LZW,Flate,jpeg,RLE}] [-m {Subsample,Average,Bicubic}]
                    [-e {a0,a1,a2,a3,a4,a4small,a5,a6,a7,a8,a9,a10,isob0,isob1,isob2,isob3,isob4,isob5,isob6,c0,c1,c2,c3,c4,c5,c6,11x17,ledger,legal,letter,lettersmall,arche,archd,archc,archb,archa,jisb0,jisb1,jisb2,jisb3,jisb4,jisb5,jisb6,flsa,flse,halfletter,hagaki}]
                    [-s {ebook,printer,default,prepress,screen,PSL2Printer}] [-c CSV] [-o DESTINATION]
                    source

Réduction de la taille des fichiers PDF

positional arguments:
  source                Dossier source

options:
  -h, --help            show this help message and exit
  -d DPI, --dpi DPI     Points par pouce
  -p PASSWORD, --password PASSWORD
                        Mot de passe pour les documents vérouillés
  -v VERSION, --version VERSION
                        Version du document PDF (défaut=1.4)
  -r {o,oui,y,yes,n,non,no}, --replace {o,oui,y,yes,n,non,no}
                        Remplacer les fichiers existants
  -k {LeaveColorUnchanged,Gray,RGB,CMYK}, --strategy {LeaveColorUnchanged,Gray,RGB,CMYK}
                        Stratégie de conversion des couleurs
  -z {LZW,Flate,jpeg,RLE}, --compression {LZW,Flate,jpeg,RLE}
                        Méthode de compression des images
  -m {Subsample,Average,Bicubic}, --downsample {Subsample,Average,Bicubic}
                        Méthode de transformation des images
  -e {a0,a1,a2,a3,a4,a4small,a5,a6,a7,a8,a9,a10,isob0,isob1,isob2,isob3,isob4,isob5,isob6,c0,c1,c2,c3,c4,c5,c6,11x17,ledger,legal,letter,lettersmall,arche,archd,archc,archb,archa,jisb0,jisb1,jisb2,jisb3,jisb4,jisb5,jisb6,flsa,flse,halfletter,hagaki}, --papersize {a0,a1,a2,a3,a4,a4small,a5,a6,a7,a8,a9,a10,isob0,isob1,isob2,isob3,isob4,isob5,isob6,c0,c1,c2,c3,c4,c5,c6,11x17,ledger,legal,letter,lettersmall,arche,archd,archc,archb,archa,jisb0,jisb1,jisb2,jisb3,jisb4,jisb5,jisb6,flsa,flse,halfletter,hagaki}
                        Appliquer à tout le document un format de page
  -s {ebook,printer,default,prepress,screen,PSL2Printer}, --profile {ebook,printer,default,prepress,screen,PSL2Printer}
                        Profile Distiller
  -c CSV, --csv CSV     Enregistrer les informations dans un fichier CSV
  -o DESTINATION, --destination DESTINATION
                        Dossier de destination
```

Pour fonctionner nous devons a minima préciser un dossier source et un dossier destination. Avec le script Python, nous procéderons comme suit :

```bash
% python reduce_gs.py -o "/Users/gilles/Downloads/destination" "/Users/gilles/Downloads/source"
```

Avec le paramètre `-r` nous pouvons choisir de ne pas remplacer les fichiers existants dans le dossier destination. 

```bash
% python reduce_gs.py -r o -o "/Users/gilles/Downloads/destination" "/Users/gilles/Downloads/source"
```

Certains documents peuvent avoir plusieurs formats de page. Il est possible de contraindre à un format particulier toutes les pages d'un document avec l'option `--papersize a5` avec en argument le format standardisé (par. `a5` ou `letter`)

```bash
% python reduce_gs.py --papersize a5 -r o -o "/Users/gilles/Downloads/destination" "/Users/gilles/Downloads/source"
```

Pour alléger un document, nous pouvons modifier la densité de points par pouce. Pour cela nous utiliserons le paramètre `-d`  ou `--dpi` suivi de la valeur de densité désirée. Rappelons nous que plus la valeur est basse, plus la qualité des images est dégradrée. Inversement, il est inutile d'augmenter les DPI au delà de la valeur utilisée par les images sources.

```bash
% python reduce_gs.py --dpi 100 --papersize letter -r o -o "/Users/gilles/Downloads/destination" "/Users/gilles/Downloads/source"
```

Pour améliorer la réduction en kilo-octets (et donc faciliter l'envoi), nous pouvons choisir un format de compression et un passage en niveau de gris pour le document. Avec cette approche, les gains seront importants.

```bash
% python reduce_gs.py --dpi 100 --papersize letter --strategy Gray --compression LZW -r o -o "/Users/gilles/Downloads/destination" "/Users/gilles/Downloads/source"
```

Enfin, nous pouvons une liste des fichiers sources dans un tableau. Pour cela nous ne mettons en options que le dossier source. A noter que les dimensions affichées sont évaluées à partir de la première page du document.

```bash
% python reduce_gs.py "/Users/gilles/Downloads/pdf1"                                                                                           
Fichiers       Auteurs    Titres     Sujets    Mot-clefs    Créateurs            Producteurs      Dates modifications            Dates creations                  Pages  Dimensions
-------------  ---------  ---------  --------  -----------  -------------------  ---------------  -----------------------------  -----------------------------  -------  -------------------
dossier.pdf    gilles     dossier    n/a       n/a          OmniPage CSDK 20.2   GPL Ghostscript  21/02/2024 17:20:51 UTC+01:00  14/02/2024 15:30:58                239  20.57 cm x 29.44 cm
                                                                                 10.02.1
-------------  ---------  ---------  --------  -----------  -------------------  ---------------  -----------------------------  -----------------------------  -------  -------------------
expertise.pdf  gilles     expertise  n/a       n/a          Gilles               GPL Ghostscript  21/02/2024 17:22:00 UTC+01:00  09/02/2024 07:11:27                174  20.99 cm x 29.70 cm
                                                                                 10.02.1
-------------  ---------  ---------  --------  -----------  -------------------  ---------------  -----------------------------  -----------------------------  -------  -------------------
relevés.pdf    gilles     relevés    n/a       n/a          Adobe InDesign 17.4  GPL Ghostscript  21/02/2024 17:22:50 UTC+01:00  27/06/2023 14:23:22 UTC+05:30      366  19.05 cm x 23.50 cm
                                                            (Windows)            10.02.1
-------------  ---------  ---------  --------  -----------  -------------------  ---------------  -----------------------------  -----------------------------  -------  -------------------
```

> Dans Windows, l'accès a un disque réseau nécessite dans Powershell de se connecter avec des identifiants valides. Pour cela nous devons au préalable lancer la ligne suivante :
>
> ```powershell
> net use \\192.168.1.14\mondisque /user:gilles
> ```
