#!/usr/bin/env python3
# -*- coding: utf-8 -*-

##################################################
## reduction de la taille des PDF
##################################################
## Author: Gilles BIHAN
## Copyright: Copyright 2023, Converio.fr
## Version: 1.0.0
## Email: gilles.bihan@converio.fr
## Status: Dev
##################################################

import os, subprocess, re, shutil, argparse
from platform import system

# pip install progressbar2
from progressbar import ProgressBar


if system() in [ 'Linux', 'Darwin']:
    ghostscript = shutil.which("gs")
elif system() in ['Windows']:
    ghostscript = shutil.which("gswin64c.exe")

def numberOfPage(source):
    cmd = [ghostscript, "-dQUIET", "-dBATCH", "-dNODISPLAY", "-dNOPAUSE", "-dPDFINFO", "-dFirstPage=1","-dLastPage=1", source]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = proc.communicate()
    ret = re.findall('([0-9]{1,})',str(stderr))
    if len(ret)>0:
        return re.search('([0-9]{1,})',str(stderr))[0]
    return 0

def cli(cmd,source,pages):
        page=0
        fichier = "[{:^20s}] ".format(os.path.basename(source)[:20])
        with ProgressBar(prefix=fichier,max_value=int(pages)) as progress:
            p = subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,universal_newlines=True)
            while True:
                chunk = p.stdout.readline()
                if chunk=='':
                    break
                m = re.search("Page (?P<page>[0-9]{1,})",chunk)
                if m:
                    progress.update(page)
                    page+=1
                    #print(m.group('page'))


def reduction(dossierSource, dossierDestination, dpi=150, version="1.4", replace=False):
    global ghostscript
    source_size = 0
    dest_size = 0
    nbr_file = 0

    for path, subdirs, files in os.walk(dossierSource):
        fichiers = [file for file in files if os.path.splitext(file)[1]==".pdf"]
        for fichier in fichiers:
            source = os.path.join(path, fichier)
            destination = source.replace(dossierSource,dossierDestination)
            
            if os.path.exists(destination) and not replace:
                continue

            destinationFinale= destination
            if replace:
                destination=re.sub('(?i)'+re.escape(".pdf"), lambda m:  ".tmp", destination)

            cmd = [ghostscript, '-sDEVICE=pdfwrite', '-dNOPAUSE', '-dBATCH', 
                    '-sColorConversionStrategy=Gray', '-dDownsampleGrayImages=true', f"-dGrayImageResolution={dpi}", f"-dCompatibilityLevel={version}",
                    f"-sOutputFile={destination}",
                    f"{source}"]

            try:
                cli(cmd,source=source,pages=numberOfPage(source=source))
                source_size += os.stat(source).st_size
                dest_size += os.stat(destination).st_size

                if replace and os.path.exists(destinationFinale):
                    os.remove(destinationFinale)
                    shutil.move(destination,destinationFinale)
            
            except FileNotFoundError:
                shutil.copyfile(source,destination)
            except Exception as e:
                print(e)

            nbr_file += 1

    return nbr_file,source_size,dest_size 

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("source", help="Dossier source",type=str)
    parser.add_argument("destination", help="Dossier de destination",type=str)
    parser.add_argument("-d","--dpi", help="Points par pouce (défaut=150)",type=int,default=150)
    parser.add_argument("-v","--version", help="Version du document PDF (défaut=1.4)",type=str,default="1.4",)
    parser.add_argument("-r","--replace", help="Points par pouce (défaut=150)",type=bool,default=False)
    try:
        args = parser.parse_args()
        if ghostscript is None:
            print("Ghostscript n'a pas été trouvé. Veuillez l'installer.")
        elif os.path.exists(args.source):       
            if not os.path.exists(args.destination):
                os.makedirs(args.destination)
            nbr_file,source_size,dest_size = reduction(dossierSource=args.source, 
                                                    dossierDestination=args.destination, 
                                                        dpi=args.dpi, version=args.version, replace=args.replace)
                
            print(f"Nbr de fichiers: {nbr_file}\tSources: {source_size / (1024*1024):.2f} mbytes\tDestinations: {dest_size / (1024*1024):.2f} mbytes soit gain de {max(0,1-(dest_size/source_size)):.2%}")
    except ZeroDivisionError:
        print("Aucun fichier n'a été traité")
    except Exception as e:
        print(e)