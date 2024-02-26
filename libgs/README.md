# Python avec libgs

Ghostscript peut être utilisé avec un exécutable binaire ou via une librairie partagée. C'est à cette deuxième hypothèse que nous nous intéressons. Nous allons piloter Ghostscript avec du code Python en utilisant la librairie *libgs*.

## Construire la librairie libgs

Les sources de version librairie partagée de Ghostscript sont disponibles de deux manières :

* avec une archive TAR compressée disponible sur le site ; 
* avec un dépôt distant à clôner localement.

### Archive

Le code source se télécharge à partir du site de [Ghostscript](https://ghostscript.com/releases/index.html). Il est commun pour toutes les plateformes (Windows, MacOs, Linux). Nous récupérons une archive TAR avec une compression GZIP. Le numéro de version est précisé dans le nom du fichier (`ghostscript-10.02.1.tar.gz` pour la version 10.02.1)

```bash
% wget https://github.com/ArtifexSoftware/ghostpdl-downloads/releases/download/gs10021/ghostscript-10.02.1.tar.gz
% tar xvf ghostscript-10.02.1.tar.gz 
% cd ghostscript-10.02.1
```

Dans Linux, nous mettons à jour le système, puis nous installons le compilateur GCC.

```bash
% sudo apt update && sudo apt upgrade
% sudo apt install build-essential
```

Dans MacOs, si nous n'utilisons pas Xcode, nous devons installer les utilisateurs de développement en ligne de commandes. Nous ouvrons le terminal et nous exécutons cette commande.

```bash
gilles@MBP-de-Gilles ~ %  xcode-select --install
```

Une fenêtre apparaît et nous cliquons sur le bouton `Installer`. Nous validons le contrat de licence. L'installation de _Command Line Developer Tools_ se fait automatiquement. Nous pouvons suivre la progression. A la fin, gcc est installé.

Pour vérifier la bonne installation de GCC, nous taperons la commande suivante :

```bash
$ gcc -v
gcc version 11.4.0 (Ubuntu 11.4.0-1ubuntu1~22.04) 
```

```bash
gilles@MBP-de-Gilles ~ % gcc -v
Apple clang version 13.1.6 (clang-1316.0.21.2.5)
Target: arm64-apple-darwin21.4.0
Thread model: posix
InstalledDir: /Library/Developer/CommandLineTools/usr/bin
```

Ensuite nous allons exécuter la configuration pour préparer les fichiers makefile.

```bash
% ./configure
```

Pour afficher l'aide du script de configuration nous exécuterons la commande `./configure --help` dans le terminal.

Pour lancer la compilation de la librairie partagée Ghostscript, nous exécuterons la commande `make so` ou `make debugso` dans le terminal.

```bash
% make so
```

Pour supprimer tous les fichiers de compilation nous avons à notre disposition `make soclean`. A la suite nous allons pouvoir relancer tout le processus de compilation avec une génération de tous les fichiers intermédiaires.

Pour exécuter l'exécutable sur le système, nous lancerons la commande `sudo make install-so` ou `sudo make install-sodebug` à la suite de la compilation. La librairie est installée dans le dossier `/usr/local/lib` (MacOS et Linux).

```bash
gilles@linux-mint:~/Téléchargements/ghostscript-10.02.1$ sudo make install-so
```

Les librairies compilées sont disponibles dans le dossier `sobin`. Sous Linux, nous trouverons des fichiers avec extension `so`. Par exemple pour la version 10.02, nous aurons la librairie `libgs.so.10.02`, et deux liens symboliques vers la librairie (`libgs.so` et `libgs.so.10`). Sous MacOs, les librairies auront une extension `dylib`. Pour la version 10.02 nous aurons la librairie `libgs.dylib.10.02` et deux liens symboliques (`libgs.dylib.10.02` ou `libgs.dylib.10`).

La librairie partagée peut être utilisée avec deux exécutables : `gsc` et `gsx`. Le premier est identique à `gs`. Le deuxième, `gsx`, utilise en sortie un périphérique d'affichage s'appuyant sur un widget GTK+.

```bash
% gsc -v
GPL Ghostscript 10.02.1 (2023-11-01)
Copyright (C) 2023 Artifex Software, Inc.  All rights reserved.
```

### Dépôt distant

Nous pouvons aussi compiler Ghostscript à partir d'un dépôt distant (Git). Bien entendu il faut au préalable avoir installé Git.

```bash
gilles@MBP-de-Gilles % git clone git://git.ghostscript.com/ghostpdl.git
Cloning into 'ghostpdl'...
remote: Enumerating objects: 231573, done.
remote: Counting objects: 100% (8266/8266), done.
remote: Compressing objects: 100% (5125/5125), done.
remote: Total 231573 (delta 4424), reused 4834 (delta 3122), pack-reused 223307
Receiving objects: 100% (231573/231573), 243.30 MiB | 10.57 MiB/s, done.
Resolving deltas: 100% (182471/182471), done.
```

Nous devons exécuter autogen.sh pour préparer localement le dépôt. Sous MacOs, nous devons au préalable installer via brew deux outils supplémentaires.

```bash
gilles@MBP-de-Gilles % brew install autoconf automake
```

Il nous reste à nous placer à la racine du dépôt local, et d'exécuter successivement 

```bash
gilles@MBP-de-Gilles gs % git clone git://git.ghostscript.com/ghostpdl.git
gilles@MBP-de-Gilles gs % cd ghostpdl
gilles@MBP-de-Gilles ghostpdl % ./autogen.sh 
gilles@MBP-de-Gilles ghostpdl % ./configure
gilles@MBP-de-Gilles ghostpdl % make debugso
```

Pour synchroniser localement avec le dépôt distant nous exécuterons à la racine du dépôt local la commande git pull dans le terminal.

```bash
gilles@MBP-de-Gilles ghostpdl % git pull
```

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
(.venv) PS C:\Users\gilles\Documents\Python Scripts\pdf> python install tzlocal tqdm
```

Nous pouvons aussi utiliser un fichier texte que nous appelerons `requirements.txt` auquel nous ajouterons la ligne suivante :

```python
tqdm==4.66.2
tzlocal==5.2
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
% conda create -n reduce_pdf -c conda-forge python=3.11 tqdm
```

Une bibliothèque peut être installée par la suite lorsque l'environnement est en cours d'utilisation.

```bash
% conda install -c conda-forge tqdm
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

## Fichiers complémentaires

Dans le dossier comportant le script Python nous copions la librairie libgs (avec un lien symbolique).

* `ghostscript/libgs/libgs.dylib`
* `ghostscript/libgs/libgs.dylib.10.02`

Nous devons également copier le fichier `gsapi.py` du dossier `demos/python` des sources de Ghostscript.

Le dossier contenant le script `gs.py` doit comporter a minima les fichiers suivants.

```text
libgs
├── README.md
├── gs.py
├── gsapi.py
├── libgs.dylib -> libgs.dylib.10.02
├── libgs.dylib.10.02
└── requirements.txt
```

## Utilisation

Pour afficher l'aide de la commande nous ajoutons le paramètre `-h`.

```bash
python3 ./ghostscript/libgs/gs.py -h
usage: gscli.py [-h] [-v] [-o DESTINATION] [--replace | --no-replace] [--recursive | --no-recursive] [-p PASSWORD] [--lockpwd LOCKPWD] [--admpwd ADMPWD] [--permissions [{print,change,extract,fill,copy,annotation,quality,none} ...]] [-d DPI] [-r RELEASE] [--strategy {Gray,RGB,CMYK}]
                [--gray [STRATEGY]] [--rgb [STRATEGY]] [--cmyk [STRATEGY]] [--compression {LZW,Flate,jpeg,RLE}] [--lzw [COMPRESSION]] [--flate [COMPRESSION]] [--jpeg [COMPRESSION]] [--rle [COMPRESSION]] [--downsample {Subsample,Average,Bicubic}] [--subsample [DOWNSAMPLE]]
                [--average [DOWNSAMPLE]] [--bicubic [DOWNSAMPLE]]
                [--papersize {a0,a1,a2,a3,a4,a4small,a5,a6,a7,a8,a9,a10,isob0,isob1,isob2,isob3,isob4,isob5,isob6,c0,c1,c2,c3,c4,c5,c6,11x17,ledger,legal,letter,lettersmall,arche,archd,archc,archb,archa,jisb0,jisb1,jisb2,jisb3,jisb4,jisb5,jisb6,flsa,flse,halfletter,hagaki}]
                [--profile {printer,default,prepress,screen,PSL2Printer,ebook}] [-i] [--title TITLE] [--author AUTHOR] [--subject SUBJECT] [--keywords KEYWORDS] [--creator CREATOR] [--producer PRODUCER] [--csv CSV] [--delimiter DELIMITER]
                [source ...]

Conversion de fichier au format PDF

positional arguments:
  source                Fichier source

options:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -o DESTINATION, --destination DESTINATION
                        Fichier ou Dossier de destination
  --replace, --no-replace
                        Remplacement des fichiers existants
  --recursive, --no-recursive
                        Recherche dans les dossiers et sous-dossiers
  -p PASSWORD, --password PASSWORD
                        Mot de passe pour les documents vérouillés
  --lockpwd LOCKPWD     Mot de passe pour vérouiller l'ouverture du document
  --admpwd ADMPWD       Mot de passe du propriétaire du document
  --permissions [{print,change,extract,fill,copy,annotation,quality,none} ...]
                        Permissions accordés
  -d DPI, --dpi DPI     Points par pouce
  -r RELEASE, --release RELEASE
                        Version du document PDF (défaut=1.4)
  --strategy {Gray,RGB,CMYK}
                        Stratégie de conversion des couleurs
  --gray [STRATEGY]     Conversion en niveaux de gris (8 bits)
  --rgb [STRATEGY]      Conversion en couleurs (24 bits)
  --cmyk [STRATEGY]     Conversion en CMYK (32 bits)
  --compression {LZW,Flate,jpeg,RLE}
                        Méthode de compression des images
  --lzw [COMPRESSION]   Compression sans perte
  --flate [COMPRESSION]
                        Compression sans perte basée sur GZIP/ZIP
  --jpeg [COMPRESSION]  Compression avec perte
  --rle [COMPRESSION]   Compression simple sans perte basée sur la répétition des données (run-length encoding ou RLE)
  --downsample {Subsample,Average,Bicubic}
                        Algorithme de rééchantillonage des images
  --subsample [DOWNSAMPLE]
                        Algorithme de rééchantillonage plus rapide
  --average [DOWNSAMPLE]
                        Algorithme de rééchantillonage intermédiaire
  --bicubic [DOWNSAMPLE]
                        Algorithme de rééchantillonage qualitatif (plus lent)
  --papersize {a0,a1,a2,a3,a4,a4small,a5,a6,a7,a8,a9,a10,isob0,isob1,isob2,isob3,isob4,isob5,isob6,c0,c1,c2,c3,c4,c5,c6,11x17,ledger,legal,letter,lettersmall,arche,archd,archc,archb,archa,jisb0,jisb1,jisb2,jisb3,jisb4,jisb5,jisb6,flsa,flse,halfletter,hagaki}
                        Appliquer à tout le document un format de page
  --profile {printer,default,prepress,screen,PSL2Printer,ebook}
                        Profile Distiller
  -i, --info            Informations sur le fichier
  --title TITLE         Titre du document
  --author AUTHOR       Auteur du document
  --subject SUBJECT     Sujet ou objet du document
  --keywords KEYWORDS   Mots clefs séparés par une virgule et un espace
  --creator CREATOR     Créateur
  --producer PRODUCER   Outil de création du document
  --csv CSV             Enregistre les informations dans un fichier csv
  --delimiter DELIMITER
                        Délimiteur CSV

Utilisation de libgs (https://ghostscript.com)
```

Pour afficher des informations sur un document PDF nous lancerons le script `gs.py` avec le nom du fichier en argument. 

```bash
% python3 ./gs.py "/Users/gilles/Downloads/dossier.pdf"
Fichier: /Users/gilles/Downloads/dossier.pdf
pages: 239
width: 583.200012
height: 834.47998
size: 20.57 cm x 29.44 cm
Author: gilles
Title: dossier
Subject: n/a
Keywords: n/a
Creator: OmniPage CSDK 20.2
Producer: GPL Ghostscript 10.02.1
ModDate: 21/02/2024 17:20:51 UTC+01:00
CreationDate: 14/02/2024 15:30:58
```

Il est possible d'obtenir les informations pour tous les fichiers d'un dossier. Par exemple, pour le dossier `pdf`.

```bash
% python3 ./gs.py --info "/Users/gilles/Downloads/pdf"
```

Pour une exploitation des informations obtenues, il est possible de créer un fichier CSV pour une utilisation d'un outil tiers comme un tableur.

```bash
% python3 ./gs.py --info --csv "/Users/gilles/Downloads/infos.csv" "/Users/gilles/Downloads/pdf"
```

Par défaut, les colonnes du fichier CSV sont séparées par une tabulation `\t`. Avec l'option `--delimiter` nous définissons un délimiteur personnalisé.

Pour faire une conversion simple, nous précisions un fichier de destination. Dans cet exemple, il n'y a aucune modification dans le fichier hormis la date de modification (`ModDate`).


* 1 fichier source -> 1 fichier destination : le fichier source est converti vers un fichier destination.

  ```bash
  % python3 ./gs.py --replace --gray --destination "/Users/gilles/Downloads/dossier-gray.pdf" "/Users/gilles/Downloads/dossier.pdf"
  ```

* dossier(s) sources(s) -> dossier destination : tous les fichiers du dossier source sont copiés dans le dossier destination. Les fichiers destination ne sont pas renommés. Par exemple nous faisons une convertion de tous les fichiers PDF du dossier `pdfs` vers le dossier `pdfs`. Si plusieurs dossiers sources sont indiqués, les fichiers PDF de chaque dossier sera converti dans le dossier de destination.

  ```bash
  % python3 ./gs.py --replace --gray --destination "/Users/gilles/Downloads/pdfs-gray" "/Users/gilles/Downloads/pdfs"
  % python3 ./gs.py --replace --gray --destination "/Users/gilles/Downloads/pdfs-gray" "/Users/gilles/Downloads/pdf1" "/Users/gilles/Downloads/pdf2"
  ```

* Fichier(s) source(s) -> dossier destination : si le dossier destination n'existe pas il sera automatiquement créé. Par exemple, les fichiers sources sont précisés les uns après les autres comme paramètre source (ici `dossier.pdf` et `annexes.pdf`). Le dossier `pdfs-gray` accueillera les fichiers convertis.

  ```bash
  % python3 ./gs.py --replace --gray --destination "/Users/gilles/Downloads/pdfs-gray" "/Users/gilles/Downloads/dossier.pdf" "/Users/gilles/Downloads/annexes.pdf"
  ```

> Si la destination n'est pas définie, les fichiers seront copiés à la racine du dossier de l'utilisateur actif.

Nous pouvons modifier les métadatas dans un nouveau fichier. Dans cet exemple nous allons donner un titre, un auteur ainsi que deux mots clefs. Chaque valeur de métadatas doit être passée en argument avec en début et fin des doubles guillemets. Chaque mot-clef doit être séparé par une virgule et un espace.

```bash
% python3 ./gs.py --title "Dossier" --author "Gilles" --keywords "dossier, projet" --destination "/Users/gilles/Downloads/pdf1/dossier-convertion.pdf" "/Users/gilles/Downloads/pdf1/dossier.pdf"
```

Les profils __Adobe Distiller__ sont utilisables en invoquant l'option `--profile` suivi de l'identifiant d'un des profils acceptés par Ghostscript (pour obtenir la liste, il faut afficher l'aide en ligne).

```bash
 % python3 ./gs.py --profile ebook --destination "/Users/gilles/Downloads/dossier-convertion.pdf" "/Users/gilles/Downloads/dossier.pdf"
```

Le document peut être converti en niveau de gris et les images adaptées à 100 DPI.

```bash
% python3 ./gs.py --strategy Gray --dpi 100 --destination "/Users/gilles/Downloads/dossier-convertion.pdf" "/Users/gilles/Downloads/dossier.pdf"
```

Par défaut le script Python ne supprime pas les fichiers de destination qui existent. Il faut donc ajouter `--replace` pour forcer le remplacement.

Pour définir un mot de passe à l'ouverture d'un fichier, nous devons à la fois définir le mot de passe du propriétaire (_owner_) et le mot de passe de l'utilisateur.

```bash
 % python3 ./gs.py --profile ebook --lockpwd pwduser --admpwd pwdadmin  --destination "/Users/gilles/Downloads/dossier-convertion.pdf" "/Users/gilles/Downloads/dossier.pdf"
```

Nous pouvons aussi modifier les autorisations d'usage. Par exemple, le document peut être limité en lecture et impression.

```bash
 % python3 ./gs.py --profile ebook --lockpwd pwduser --admpwd pwdadmin --permissions print --destination "/Users/gilles/Downloads/dossier-convertion.pdf" "/Users/gilles/Downloads/dossier.pdf"
```

> Les mots de passe utilisateur et propriétaire doivent être différent.

Le tableau qui suit récapitule les différentes autorisations.

Autorisations | print | change | extract | fill | copy | annotation
--- | :---: | :---: | :---: | :---: | :---: | :---: | 
impression | ✓ | | | | | | 
Copie du texte ou des graphisme | | | ✓ | | | |
Modification des attributs du document | | ✓ | | ✓ | | ✓ |
Insertion, rotation ou suppression de pages | | ✓ | | | | |
Ajout d'annotations ou de signatures | | | | | | ✓ |
Extraction du texte à des fins d'accessibilité | | | | | ✓ | |
Remplissage des champs de formulaire existants | | | | ✓ | | ✓ |