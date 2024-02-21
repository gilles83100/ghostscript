
```bash
gilles@MacStuddeGilles gs % git clone git://git.ghostscript.com/ghostpdl.git
gilles@MacStuddeGilles ghostpdl % cd ghostpdl
gilles@MacStuddeGilles ghostpdl % ./autogen.sh
gilles@MacStuddeGilles ghostpdl % make debugso
```

Dans le dossier comportant le script Python nous copions la librairie libgs (avec un lien symbolique).

* `ghostscript/libgs/libgs.dylib`
* `ghostscript/libgs/libgs.dylib.10.02`

Nous devons également copier le fichier `gsapi.py` du dossier `demos/python` des sources de Ghostscript, ainsi que le fichier viewjpeg.ps du dossier `lib`.



pip install pytz tzlocal tqdm