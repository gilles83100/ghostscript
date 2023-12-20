
Les fichiers PDF sont devenus une norme pour les échanges de documents. Ces fichiers peuvent avoir un poids en octets conséquent notamment en raison de la présence d'images. S'il existe des solutions pour transmettre des fichiers lourds (Wetransfer par ex.) il peut s'avérer judicieux de reduire leur taille. Pour cela nous disposons de nombreuses solutions. Celles que nous allons étudier repose soit sur Ghostscript soit sur du code Python.

# Avec Ghostscript

## Installation

### Windows

Nous installons Ghostscript à partir de la page de téléchargement. Sous Windows 11 nous choisissons la version 64 bit.

La version est installée dans le dossier `C:\Program Files\gs`. A l'intérieur un sous-repertoire pour la version installée. Par exemple, un sous répertoire `gs10.02.1`.

Dans un sous-répertoire `bin`, nous avons deux exécutables :
* `gswin64.exe` qui ouvre Ghostscript dans une fenêtre
* `gswin64c.exe` qui ouvre Ghostscript dans le terminal

Par exemple pour ouvrir ghostscript dans Powershell nous utiliserons un de ces exécutables.

```powershell
PS C:\Users\gille> & 'C:\Program Files\gs\gs10.00.0\bin\gswin64c.exe'
GPL Ghostscript 10.0.0 (2022-09-21)
Copyright (C) 2022 Artifex Software, Inc.  All rights reserved.
This software is supplied under the GNU AGPLv3 and comes with NO WARRANTY:
see the file COPYING for details.
GS>
```

> Pour une utilisation avec PowerShell il conviendra de prendre garde à la syntaxe. Par exemple pour le paramètre `CompatibilityLevel` nous écrirons `-dCompatibilityLevel='1.4'` ou `"-dCompatibilityLevel=1.4"`.

### macOS

Pour installer Ghostscript dans sur macOS nous allons passer par le gestionnaire de package [brew](https://brew.sh/index_fr)

```bash
% brew update
% brew upgrade
% brew install ghostscript
% brew brew cleanup
```

Pour mettre à jour Ghostscript

```bash
% brew upgrade ghostscript
```

Pour afficher les fichiers PDF avec Ghostscript nous devons installer [xquartz](https://www.xquartz.org):

```bash
% brew install --cask xquartz
```

L'exécutable de Ghostscript est `gs`. Pour connaître la version de ghostscript :

```bash
% gs --version              
9.56.1
```

Pour connaître l'emplacement de l'exécutable :

```bash
% which gs
/opt/local/bin/gs
```

Il est possible que le fichier à cet emplacement soit un lien symbolique. Pour vérifier cela nous tapons la ligne de commandes qui suit. Nous constatons que les informations du fichier commence par `l` (*link*). `->` précise l'emplacement de l'exécutable lié et qui sera exécuté.

```bash
% ls -la /opt/local/bin/gs                                                    
lrwxr-xr-x  1 root  wheel  47 15 déc 11:07 /opt/local/bin/gs -> /opt/homebrew/Cellar/ghostscript/10.02.1/bin/gs
```

Nous pouvons constater que par exemple la dernière version est installée par *brew* dans le dossier `/opt/homebrew/Cellar/ghostscript`. A l'intérieur de cet emplacement nous avons un répertoire par version de ghostscript. Par exemple, nous avons un répertoire 10.01.2. A l'intérieur un sous-répertoire `bin` avec l'exécutable `gs` (pour ghostscript).

```bash
% /opt/homebrew/Cellar/ghostscript/10.01.2/bin/gs 
GPL Ghostscript 10.01.2 (2023-06-21)
Copyright (C) 2023 Artifex Software, Inc.  All rights reserved.
This software is supplied under the GNU AGPLv3 and comes with NO WARRANTY:
see the file COPYING for details.
```

Nous pouvons créer un lien symbolique vers l'exécutable pour un appel simplifié. Dans notre cas nous utiliserons `ghostscript` pour appeler l'exécutable `gs`. La commande `ln` avec l'option `-s` crée un lien symbolique vers un fichier.

```bash
% sudo rm /opt/local/bin/gs
% sudo ln -s /opt/homebrew/Cellar/ghostscript/10.01.2/bin/gs /opt/local/bin/ghostscript
% which ghostscript
/opt/local/bin/ghostscript
```

### Linux

En fonction de la distribution utilisée, nous utiliserons les lignes de commandes qui suivent.

#### Pour les distributions à base de Debian

```bash
gilles@debian:~$ sudo apt update
gilles@debian:~$ sudo apt install ghostscript
```

#### Pour la distribution Arch Linux

```bash
[gilles@Archlinux ~]$ sudo pacman -U http://mirror.archlinuxarm.org/aarch64/extra/libpaper-2.1.1-1-aarch64.pkg.tar.xz
[gilles@Archlinux ~]$ sudo pacman -S ghostscript
```

#### Pour la distribution Alpine Linux

```bash
~ $ sudo apk update
~ $ sudo apk add ghostscript
```

#### Pour les distributions à base de Fedora

```bash
[gilles@fedora ~]$ sudo yum install ghostscript
```

L'exécutable de Ghostscript est `gs`.

Pour construire l'application Ghostscript à partir des sources, nous procédons comme suit.

* Nous commençons par récupérer un URL valide vers l'archive contant les sources. Pour cela, nous allons sur la page de [téléchargement](https://ghostscript.com/releases/gsdnld.html) et nous récupérons le lien (par ex. [https://github.com/ArtifexSoftware/ghostpdl-downloads/releases/download/gs10012/ghostscript-10.01.2.tar.gz](https://github.com/ArtifexSoftware/ghostpdl-downloads/releases/download/gs10012/ghostscript-10.01.2.tar.gz)).

* Dans le terminal nous nous déplaçons dans le répertoire de téléchargement ou dans un répertoire temporaire quelconque. Nous allons décompresser dans ce répertoire les sources. Pour télécharger l'archive dans le terminal nous avons à notre disposition la commande `wget`. Si elle n'est pas disponible, tous les gestionnaires de paquets la répertorie dans leurs dépôts (par ex. `sudo apt install wget`).

* Nous désarchivons le fichier téléchargé. A partir d'un gestionnaire de fenêtres, en double cliquant dessus nous allons pouvoir le faire automatiquement. Dans le terminal nous utiliserons une ligne de commandes pour désarchiver : `tar -xzf ghostscript-10.01.2.tar.gz`. Un sous répertoire est créé. Les sources sont à l'intérieur

* Nous définissons comme répertoire en cours la racine de ce répertoire. Par ex. `cd ghostscript-10.01.2`

* A l'intérieur, nous exécutons le fichier de configuration `./configure`. Ce fichier va préparer la compilation à partir des données collectés dans le système (architecture par exemple). Un fichier `makefile` est créé.

* Pour lancer la compilation du code nous tapons la commande `make`. Cette opération peut être plus ou moins longue en fonction de la puissance de l'ordinateur.

* Enfin, pour installer le code compilé  dans notre système, nous exécuterons en mode super utilisateur la commande `sudo make install`

En résumé, nous pouvons exécuter les commandes suivantes :

```bash
[gilles@Archlinux Downloads]$ wget https://github.com/ArtifexSoftware/ghostpdl-downloads/releases/download/gs10012/ghostscript-10.01.2.tar.gz
[gilles@Archlinux Downloads]$ tar -xzf ghostscript-10.01.2.tar.gz
[gilles@Archlinux Downloads]$ cd ghostscript-10.01.2    
[gilles@Archlinux ghostscript-10.01.2]$ ./configure
[gilles@Archlinux ghostscript-10.01.2]$ ./configure
[gilles@Archlinux ghostscript-10.01.2]$ make
[gilles@Archlinux ghostscript-10.01.2]$ sudo make install
```

## Options

Ghostscript est une logiciel en ligne de commandes. Par défaut, il va s'exécuter en mode interactif. L'utilisateur doit entrer les commandes à la suite d'un prompt et les valider par appui sur la touche entrée. Pour sortir de ce mode, il faut taper la commande `quit`.

Pour ce qui nous concerne il est plus intéressant de l'utiliser en mode shell, sans interaction. A la suite du nom de la commande Ghostscript (par ex. `gs`) nous saisirons une suite de paramètres et d'arguments, ainsi que le nom des fichiers à traiter en entrée et en sortie.

[](https://ghostscript.readthedocs.io/en/gs10.01.1/VectorDevices.html#distiller-parameters)

Commandes | Descriptions
--- | ---
`gs -h` | affiche l'aide et la configuration de base, notamment la liste des périphériques disponibles (device).
`-q` ou `-dQUIET` | Supprime l'affichage des messages de démarrage (version, copyright)
`-d` | Affecte sous 
`-s` | Affecte sous forme de texte une valeur à un paramètre interne
`-dNODISPLAY` | Utilise un périphérique `NUL` qui ne génère pas de sortie. Cela remplace le périphérique de sortie par défaut ou défini avec `-sDEVICE=`. A utiliser dans le cas d'une évaluation.
`-dPDFSETTINGS=`  | Profile Adobe Distiller pour traiter le fichier en sortie. Ils comportent des préréglages en fonction de la destination. Par ex. `/screen`. Les valeurs possibles sont : `\screen` (résolution basse, optimisé pour les écrans), `\ebook` (résolution moyenne, optimisé pour livre numérique), `\printer` (résolution élevée, optimisé pour impression), `\prepress` (optimisé prepress) et `\default`
`-sDEVICE=` | Défini le périphérique de sortie. C'est par exemple un fichier Adobe PDF avec `pdfwrite`. 
`-sPAPERSIZE=` | Défini les dimensions par défaut des pages. Par ex. `-sPAPERSIZE=a4` ou `-sPAPERSIZE=legal`
`-dDEVICEWIDTHPOINTS=w` | Définir la largeur d'une page en DPI (point par pouce, 1 point = 1/72 de pouce ). Par exemple
`-dDEVICEHEIGHTPOINTS=h` | Définir la hauteur d'une page en DPI (point par pouce, 1 point = 1/72 de pouce ). Par exemple
`-dMonoImageResolution=` | Résolution en DPI pour les images monochrome. Par ex.  `-dMonoImageResolution=100`
`-dColorImageResolution=` | Résolution en DPI pour les images couleur. Par ex. `100`
`-dGrayImageResolution=` | Résolution en DPI pour les images en niveaux de gris. Par ex. `150`
`-dDownsampleColorImages=` | Autorise la modification de la résolution des images couleurs. `true` pour autoriser.
`-dColorImageDownsampleType=` | Défini la méthode de transformation de la résolution des images. Les valeurs possibles sont : `/Subsample`, `/Average` et `/Bicubic`.
`-dAntiAliasColorImages=` |  Active le traitement anti-alias des images couleurs. `true` pour autoriser.
`-dDownsampleGrayImages=` | Autorise la modification de la résolution des images en niveaux de gris. `true` pour autoriser.
`-dGrayImageDownsampleType=` | Défini la méthode de transformation de la résolution des images. Les valeurs possibles sont : `/Subsample`, `/Average` et `/Bicubic`.
`-dAntiAliasGrayImages=` |  Active le traitement anti-alias des images en niveaux de gris. `true` pour autoriser.
`-dDownsampleMonoImages=` | Autorise la modification de la résolution des images monochromes. `true` pour autoriser.
`-dMonoImageDownsampleType=` | Défini la méthode de transformation de la résolution des images. Les valeurs possibles sont : `/Subsample`, `/Average` et `/Bicubic`.
`-dAntiAliasMonochromeImages=` |  Active le traitement anti-alias des images en monochrome. `true` pour autoriser.
`-dBATCH` | N'ouvre pas la console de Ghostscript et traite directement le ou les fichiers en entrée. Ghostscript se ferme automatiquement quand toutes les opérations sont terminées. A utiliser pour l'utilisation dans des scripts
`-dNOPROMPT` | En mode interactif, masque l'invite pour saisir de Ghostscript
`-dNOPAUSE` | Désactive la pause automatique après chaque page. Il est utilisé conjointement avec Normalement, on `-dBATCH`.
`-sColorConversionStrategy=` | Défini la stratégie de conversion des couleurs avec une chaîne de caractères. Les valeurs possibles sont : `LeaveColorUnchanged`, `Gray`, `RGB`, ou `CMYK`.
`-dColorConversionStrategy=` | Défini la stratégie de conversion des couleurs. Les valeurs possibles sont : `/LeaveColorUnchanged`, `/Gray`, `/RGB`, ou `/CMYK`.
`-dCompatibilityLevel=` | Niveau de compatibilité. Par ex. `1.4`
`-o` ou `-sOutputFile=` | Définir le fichier de sortie avec les options `-dBATCH` et `-dNOPAUSE`. Par ex. `-o out.pdf` ou `-sOutputFile=out.pdf`
`-sCompression=` | Type de compression `None`, `LZW`, `Flate`, `jpeg` et `RLE`
`-dDetectDuplicateImages=` | Regroupe en une seule images les images ayant un hashage identique. La valeur par défaut est à `true`.

## Afficher un PDF

Par exemple, sous Linux, nous indiquons à Ghostscript le fichier à afficher.

```bash
[gilles@Archlinux Downloads]$ gs cours-python.pdf 
GPL Ghostscript 10.01.2 (2023-06-21)
Copyright (C) 2023 Artifex Software, Inc.  All rights reserved.
This software is supplied under the GNU AGPLv3 and comes with NO WARRANTY:
see the file COPYING for details.
Unknown .defaultpapersize: (A4).
Processing pages 1 through 298.
Page 1
>>showpage, press <return> to continue<<
```

## Obtenir des informations

Pour récupérer les informations disponibles dans un fichier PDF et afficher les métadatas nous procéderons comme suit : 

```bash
% gs -dQUIET -dBATCH -dNODISPLAY -dNOPAUSE -dPDFINFO "merge.pdf"

        (null) has 15 pages

Title: ??
Author: Gilles
Subject: 
Keywords: 
Creator: ??
Producer: GPL Ghostscript 9.56.1
CreationDate: D:20230718174033+02'00'
ModDate: D:20230718174033+02'00'
```

La date et l'heure sont définies au format `D:%Y%m%d%H%M%S`. Pour convertir une date en utilisant le language Python nous procéderons ainsi :

```python
from datetime import datetime

# PDF Date -> date
datePDF=datetime.strptime('D:20230719101359','D:%Y%m%d%H%M%S')
print(datePDF) # -> 2023-07-19 10:13:59

# date -> PDF Date
dateActuelle=datetime.strftime(datetime.now(), 'D:%Y%m%d%H%M%S')
print(dateActuelle) # -> 'D:20230719101359'
```

Pour afficher le détail des documents PDF il existe une alternative avec [Poppler](https://freedesktop.org/wiki/Software/poppler/). C'est une bibliothèque open source spécialisée pour les documents PDF.

```bash
% brew install poppler
```

```bash
% pdfinfo "/Users/gilles/Downloads/source.pdf" 
Title:           
Creator:         Adobe Acrobat 22.1
Producer:        Adobe Acrobat 22.1 Image Conversion Plug-in
CreationDate:    Wed Nov  8 19:01:34 2023 CET
ModDate:         Wed Nov  8 19:01:34 2023 CET
Custom Metadata: no
Metadata Stream: yes
Tagged:          no
UserProperties:  no
Suspects:        no
Form:            none
JavaScript:      no
Pages:           567
Encrypted:       no
Page size:       532.8 x 646.08 pts
Page rot:        0
File size:       438948393 bytes
Optimized:       yes
PDF version:     1.6
```
Les dimensions de la page (page size) sont en points. Pour les convertir nous appliquons la formule valeur en point multiplié par 1/72 et multipliée par 2.54 pour une valeur en centimètres. Dans notre exemple, nous évaluons pour la largeur `532.8 * 1/72 * 2.54` soit `18.796 cm`. La hauteur sera de `22.792 cm`.

Pour connaître le détail des images d'un document PDF, nous exécuterons la ligne suivante :

```bash
% pdfimages -list "/Users/gilles/Downloads/source.pdf"
page   num  type   width height color comp bpc  enc interp  object ID x-ppi y-ppi size ratio
--------------------------------------------------------------------------------------------
   1     0 image    2220  2692  rgb     3   8  jpeg   no      3564  0   300   300  945K 5.4%
   2     1 image    2220  2692  rgb     3   8  jpeg   no         4  0   300   300  497K 2.8%
   3     2 image    2220  2692  rgb     3   8  jpeg   no         8  0   300   300  581K 3.3%
   4     3 image    2220  2692  rgb     3   8  jpeg   no        12  0   300   300  666K 3.8%

...
```

Dans ce document nous identifions la largeur, hauteur, mode couleur et la densité de points par pouce (*inch*).

## Dévérouiller un PDF

Un document PDF peut être protégé par un mot de passe. Pour récupérer par exemple des informations sur ce fichier, nous devrons transmettre le mot de passe avec `-sPDFPassword=`.

```bash
% gs -dQUIET -dBATCH -dNODISPLAY -dNOPAUSE -sPDFPassword=XXXXXXXX -dPDFINFO "crypte.pdf"

        (null) has 2 pages

Title: /var/www/kalilab-tmp/ktag8f9l8f.rtf
Author: Laurent Schlegel
Creator: Ted: http://www.nllgg.nl/Ted
Producer: Ted: http://www.nllgg.nl/Ted
CreationDate: D:202108121018
ModDate: D:202109141311
```

## Joindre plusieurs fichiers

Nous allons joindre plusieurs fichiers PDF en un seul. Nous en profitons pour convertir toutes les pages en niveau de gris.

```bash
* gs -sDEVICE=pdfwrite -dNOPAUSE -sColorConversionStrategy=Gray -dCompatibilityLevel=1.4 -sOutputFile='merge.pdf' -dBATCH 'source1.pdf' 'source2.pdf' 'source3.pdf'
```

## Convertir en PDF/A

Un document PDF/A (*Portable Document Format Archivable*) est une variante normalisée ISO. Ce type de document a été créé pour réaliser un archivage long et apporter des garanties. Ghostscript propose d'ajouter le paramètre `-dPDFA=1`.

```bash
% gs -dPDFA=1 -sDEVICE=pdfwrite -dNOPAUSE -dBATCH -sColorConversionStrategy=Gray -dDownsampleGrayImages=true  -dGrayImageResolution=150 -dGrayImageDownsampleType=/Bicubic -dCompatibilityLevel=1.4 -sOutputFile="/Users/gilles/Downloads/destination.pdf" "/Users/gilles/Downloads/source.pdf"
```

## Réduction de la taille des documents

### Profile Distiller

L'utilisation de profiles inspirés d'Adobe Distiller est une approche simple pour réduire le poids d'un document. Ces profiles utilisent des réglages adaptés en fonction de l'appareil qui affichera le PDF.

Pour afficher la liste des profiles supportés par l'option `-dPDFSETTINGS=...' nous utiliserons la commande suivante sous macOS ou Linux :

```bash
% gs -dNODISPLAY -c ".distillersettings {exch ==only ( ) print ==} forall quit"
GPL Ghostscript 9.56.1 (2022-04-04)
Copyright (C) 2022 Artifex Software, Inc.  All rights reserved.
This software is supplied under the GNU AGPLv3 and comes with NO WARRANTY:
see the file COPYING for details.
/default -dict-
/prepress -dict-
/screen -dict-
/PSL2Printer -dict-
/ebook -dict-
/printer -dict-
```

Sous Windows, dans Powershell nous utiliserons la même commande.

```powershell
PS C:\Users\gille> & 'C:\Program Files\gs\gs10.00.0\bin\gswin64c.exe' -dNODISPLAY -c ".distillersettings {exch ==only ( ) print ==} forall quit"
GPL Ghostscript 10.0.0 (2022-09-21)
Copyright (C) 2022 Artifex Software, Inc.  All rights reserved.
This software is supplied under the GNU AGPLv3 and comes with NO WARRANTY:
see the file COPYING for details.
/default -dict-
/prepress -dict-
/screen -dict-
/PSL2Printer -dict-
/ebook -dict-
/printer -dict-
```

Pour afficher les paramètres par défaut d'un profile comme par exemple `/screen` :

```bash
% gs -q -dNODISPLAY -c ".distillersettings /screen get {exch ==only ( ) print ===} forall quit" | sort
/AutoRotatePages /PageByPage
/CannotEmbedFontPolicy /Warning
/ColorACSImageDict << /ColorTransform 1 /Blend 1 /HSamples [2 1 1 2] /VSamples [2 1 1 2] /QFactor 0.76 >>
/ColorConversionStrategy /sRGB
/ColorImageDownsampleType /Average
/ColorImageResolution 72
/CompatibilityLevel 1.5
/CreateJobTicket false
/DoThumbnails false
/EmbedAllFonts true
/GrayACSImageDict << /ColorTransform 1 /Blend 1 /HSamples [2 1 1 2] /VSamples [2 1 1 2] /QFactor 0.76 >>
/GrayImageDownsampleType /Average
/GrayImageResolution 72
/MonoImageDownsampleType /Subsample
/MonoImageResolution 300
/NeverEmbed [/Courier /Courier-Bold /Courier-Oblique /Courier-BoldOblique /Helvetica /Helvetica-Bold /Helvetica-Oblique /Helvetica-BoldOblique /Times-Roman /Times-Bold /Times-Italic /Times-BoldItalic /Symbol /ZapfDingbats]
/PreserveEPSInfo false
/PreserveOPIComments false
/PreserveOverprintSettings false
/UCRandBGInfo /Remove
```

A la suite d'un paramètre de sortie (ici `screen`) nous pouvons modifier certains paramètres comme la résolution de sortie pour les images (ici pour les images monochrome, niveau de gris et couleur).

```bash
% gs -dPDFSETTINGS=/screen -sDEVICE=pdfwrite -dMonoImageResolution=150 
-dColorImageResolution=100 -dGrayImageResolution=150 
-dBATCH -dNOPROMPT -dNOPAUSE -sOutputFile="/Users/gilles/Documents/Archives/temporaire/pdf-out.pdf" "/Users/gilles/Documents/Archives/temporaire/pdf-in.pdf"
```

### Niveaux de gris

Pour réduire le poids d'un document, une approche consiste à transformer toutes les images en niveaux de gris. En effet, une image avec cette colorimétrie utilise 256 niveaux de gris. Le nombre d'informations stockées pour une image sera réduit. 

Nous personnaliserons la ligne de commandes pour forcer ce type de conversion.

* `-sColorConversionStrategy=Gray` pour appliquer une conversion vers du niveaux de gris à toutes les images.
* `-dGrayImageResolution=100` pour modifier la densité de points par pouce (DPI ou nombre de points imprimés sur une ligne). Un pouce (inch) est égale à 2.54 cm. Une image de 10 cm x 5 cm aura pour une densité de 200 dpi aura environ 787 points en largeur (10 cm / 2.54 x 200 dpi). Plus la résolution en DPI est élevée, plus l'image sera volumineuse. A contrario, une résolution faible allégera le poids de l'image avec en contre-partie une détérioration de la qualité.
* `-dDownsampleGrayImages=true` pour activer le changement de résolution.

Pour réduire la taille de l'image nous allons jouer sur le nombre de DPI.

```bash
gs -sDEVICE=pdfwrite -dNOPAUSE -dBATCH -sColorConversionStrategy=Gray -dDownsampleGrayImages=true  -dGrayImageResolution=100 -dCompatibilityLevel=1.4 -sOutputFile="/Users/gilles/Downloads/destination.pdf" "/Users/gilles/Downloads/source.pdf"
```

A savoir que pour une visualisation sur un écran spécifique (je pense notamment à une liseuse ou une tablette), il faut tenir de la résolution. Par exemple pour un écran 24" full hd (1920 x 1080) nous aurons une densité de pixels de 92 [PPI](https://en.wikipedia.org/wiki/Pixel_density) (*Pixels per inch*).

ppi = nombre de pixels de large / largeur de l'écran en pouce (inch)

Attention, il s'agit de la largeur d'un écran en pouce, et non pas de la diagonale. Par exemple pour un écran [Huawei MateView 28.2"](https://www.displayspecifications.com/en/model-width/b4452703) nous avons approximativement une largeur de 23.95 pouces pour une résolution horizontale de 3840 pixels.

*ppi = 3840 pixels / 23.95 pouces = 160 PPI*

Pour un liseuse, une Amazon Kindle Scribe 10.2" (1860x2480 pixels) à une densité de 300 PPI. Pour récupérer la largeur en pouce, nous appliquerons la formule suivante :

*largeur en pouces = largeur en pixels / ppi = 1860 / 300 = 6.2"*

## Automatisation

Il existe de nombreuses possibilités en matière d'automatisation. L'utilisation du terminal est une de ces solutions. Ce n'est pas une approche facile pour le néophite, mais son utilisation peut s'avérer un puissant allié pour réduire la taille des fichiers. 

### Windows Powershell

Sous Windows, en utilisant PowerShell nous pouvons automatiser la réduction de la taille des fichiers. Nous créons un fichier texte `reduction.ps1` dans lequel nous intégrons ces lignes. Sans faire un cours sur PowerShell, notons les points suivants :

* `Get-ChildItem` récupère dans un tableau tous les fichiers (y compris dans les sous-dossiers) avec extension `.pdf`.
* `$gs` précise l'emplacement de Ghostscript.
* `$destinationFolder` identifie le dossier de destination où tous les fichiers réduits seront créés.
* `ForEach` parcoure les éléments du tableau `$files`. Chaque élément est placé dans une variable `$file`.
* `$destination` comporte le nom complet du fichier à créer (dossier et fichier).
* `if` est utilisé pour ne réduire que les fichiers de 100 Mo et plus. C'est facultatif. Nous pouvons supprimer ce test et les accolades associées.
* `& $gs ...` exécute Ghostscript avec les paramètres pour chaque élément de la liste `$files`.

```powershell
$files= Get-ChildItem -Path "D:\travail" -Filter *.pdf -Recurse -ErrorAction SilentlyContinue -Force
$gs = 'C:\Program Files\gs\gs10.02.1\bin\gswin64c.exe'
$destinationFolder = "d:\pdf_reduits"

ForEach ($file in $files) {
    $destination = [io.path]::Combine($destinationFolder,$file)
    If ((($file.Length) / 1024 / 1024) -ge 100) {
        & $gs -sDEVICE=pdfwrite -dNOPAUSE -dBATCH -sColorConversionStrategy=Gray -dDownsampleGrayImages=true -dGrayImageResolution=150 "-dCompatibilityLevel=1.4" -o $destination $file.FullName
    }  
}
```

> Pour exécuter ce script dans PowerShell nous devons autoriser l'utilisateur actuel. Pour cela nous ouvrons le terminal en mode administrateur et nous tapons la commande suivante :
>
> ```powershell
> PS C:\Users\gilles> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
> ```

### Shell MacOS/Linux

Nous allons créer un fichier texte que nous nommerons `reduction.sh`. Cela se fait automatiquement par la ligne de commandes qui suit :

```bash
% nano reduction.sh
```

A l'intérieur de ce fichier nous allons créer une fonction récursive pour parcourir tous les sous-répertoires d'un emplacement spécifié lors de l'appel de la fonction. L'écriture de script pour le terminal utilise un langage particulièrement abscon. Il faut être vigileant à bien reproduire la syntaxe.

```bash
#!/bin/bash
sourceFolder=/Users/gilles/Downloads/pdf
destinationFolder=/Users/gilles/Downloads/pdf_reduce/

recherche () {
    for chemin in "$1"/*; do
        if [ -d "$chemin" ]; then
            walk_dir "$chemin"
        elif [ -e "$chemin" ]; then
            case "$chemin" in
                *.pdf|*.PDF)
                        destination=$destinationFolder$(basename "$chemin") 
                        gs -sDEVICE=pdfwrite -dNOPAUSE -dBATCH -sColorConversionStrategy=Gray 
                           -dDownsampleGrayImages=true  -dGrayImageResolution=150
                           -dCompatibilityLevel=1.4 -o "${destination}" "${chemin}"
            esac
        fi
    done
}

recherche "$sourceFolder"
```

Le script pourra être exécuté tout simplement.

```bash
% bash reduction.sh
```

Pour rendre exécutable le script nous exécuterons cette commande.

```bash
% sudo chmod +x reduction.sh
```

L'exécution du script se fera de cette façon :

```bash
% ./reduction.sh
```

Nous pouvons modifier le script pour définir dans la ligne de commandes en paramètres les dossiers de recherche (`$1`) et de destination (`$2`).

```bash
#!/bin/bash
sourceFolder=$1
destinationFolder=$2

...
```

Nous lançons le script en ajoutant les chemins source et destination (avec un `/` à la fin).

```bash
% ./reduce.sh /Users/gilles/Downloads/pdf_source /Users/gilles/Downloads/pdf_destination/
```

> Pour afficher la liste de tous les fichiers PDF contenus dans un dossier et ses sous-dossiers nous avons à notre disposition la commande `find`.
>
> ```bash
> % find /Users/gilles/Downloads/pdf -type f -name '*.pdf' -exec printf "%s\n" {} +   
> ```

Sous MacOS et Linux il existe de nombreuses autres possibilités pour automatiser en ligne de commandes la réduction de la taille des fichiers. Au lieu d'utiliser un script avec une boucle, nous pouvons le faire en une seule ligne de commandes en utilisant `find`. Cette commande est capable d'exécuter une ou plusieurs commandes en communiquant chaque nom de fichier trouvé (récupérable avec `{}`). `basename` est utilisé pour extraire le nom du fichier sans extension.

```bash
% find /Users/gilles/Downloads/pdf_source -type f -name "*.pdf" -exec bash -c 'destination="/Users/gilles/Downloads/pdf_destination/"$(basename "$0" .pdf); gs -sDEVICE=pdfwrite -dNOPAUSE -dBATCH -sColorConversionStrategy=Gray -dDownsampleGrayImages=true -dGrayImageResolution=150 -dCompatibilityLevel=1.4 -o $destination".reduce.pdf" "$0";' {} \;
```

En mode terminal, nous pouvons également utiliser des variables locales (`destinationDossier` et `sourceDossier`) pour renseigner la ligne de commandes.

```bash
% destinationDossier="/Users/gilles/Downloads/pdf_reduce/"
% sourceDossier="/Users/gilles/Downloads/pdf"
% find $sourceDossier -type f -name "*.pdf" -exec zsh -c 'destination=$1$(basename "$0" .pdf)".reduce.pdf"; gs -sDEVICE=pdfwrite -dNOPAUSE -dBATCH -sColorConversionStrategy=Gray -dDownsampleGrayImages=true -dGrayImageResolution=150 -dCompatibilityLevel=1.4 -o $destination "$0";' {} $destinationDossier \;
```
### Python

Nous allons créer un programme Python pour automatiser la réduction. 

# Avec Python

En développement Python il existe de nombreux packages pour travailler sur les fichiers PDF. [pypdf](https://pypdf.readthedocs.io/en/latest/index.html) est une des solutions les plus abouties. Elle est open source et gratuite. Au fil du temps les fonctionnalités ont évoluées.

## Installation

Pour installer la bibliothèque dans un environnement Python classique nous utiliserons la commande `pip`.

```
pip install --upgrade pip
pip install pyside6 pypdf==3.12.2
pip install pypdf[image]
```

Pour installer Ghostscript pour un usage à partir de *Conda* :

```bash
% conda install -c conda-forge ghostscript
```

## Metadata

```bash
$ pip install pikepdf
```

```python
import pikepdf
pdf = pikepdf.Pdf.open(pdf_filename)
docinfo = pdf.docinfo
for key, value in docinfo.items():
    print(key, ":", value)
```
