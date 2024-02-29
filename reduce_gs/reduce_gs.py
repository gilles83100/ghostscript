#!/usr/bin/env python3
# -*- coding: utf-8 -*-

##################################################
## reduction de la taille des PDF
##################################################
## Author: Gilles BIHAN
## Copyright: © 2024, Converio.fr gilles-bihan.fr
## Version: 1.0.0
## Email: gilles.bihan@converio.fr
## Status: Dev
##################################################

import os, subprocess, re, shutil, argparse
from platform import system
from datetime import datetime

from tqdm import tqdm
from tabulate import tabulate, SEPARATING_LINE

paper = ["a0", "a1", "a2", "a3", "a4",
        "a4small", "a5", "a6", "a7", "a8",
        "a9" ,"a10", "isob0", "isob1", "isob2",
        "isob3", "isob4", "isob5", "isob6", "c0",
        "c1", "c2", "c3", "c4", "c5",
        "c6", "11x17", "ledger", "legal", "letter",
        "lettersmall", "arche", "archd", "archc", "archb",
        "archa", "jisb0", "jisb1", "jisb2", "jisb3",
        "jisb4", "jisb5", "jisb6", "flsa", "flse",
        "halfletter", "hagaki"]

if system() in [ 'Linux', 'Darwin']:
    ghostscript = shutil.which("gs")
elif system() in ['Windows']:
    ghostscript = shutil.which("gswin64c.exe")

def getProfile():
    cmd = [ghostscript,'-dNODISPLAY','-c', ".distillersettings {exch ==only ( ) print ==} forall quit"]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = proc.communicate()

    ret = re.findall("^\/(.*) -dict-",stdout.decode(),re.MULTILINE)
    if ret:
        return ret
    return ["default", "screen", "ebook", "printer", "prepress"]

def numberOfPage(source, password=""):
    cmd = [ghostscript, "-dQUIET", "-dBATCH", "-dNODISPLAY", "-dNOPAUSE", f"-sPDFPassword={password}", "-dPDFINFO", "-dFirstPage=1","-dLastPage=1", source]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = proc.communicate()
    ret = re.findall('([0-9]{1,})',str(stderr))
    if len(ret)>0:
        return re.search('([0-9]{1,})',str(stderr))[0]
    return 0

def cli(cmd, source, pages):
    fichier = "[{:^20s}] ".format(os.path.basename(source)[:20])
    with tqdm(total=int(pages)) as bar:
        bar.set_description_str(fichier)
        p = subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,universal_newlines=True)
        while True:
            chunk = p.stdout.readline()
            if chunk=='':
                break
            m = re.search("Page (?P<page>[0-9]{1,})",chunk)
            if m:
                bar.update(1)
                
def get_infos(dossierSource, password="", csvFilename=None):
    table = []

    for path, subdirs, files in os.walk(dossierSource):
        fichiers = [file for file in files if os.path.splitext(file)[1]==".pdf"]
        for fichier in fichiers:
            size,pages = "?","?"
            row = [fichier]
            source = os.path.join(path, fichier)
            cmd = [ghostscript, "-dQUIET", "-dBATCH", "-dNODISPLAY", "-dNOPAUSE", "-dPDFINFO", "-dFirstPage=1","-dLastPage=1", f"-sPDFPassword={password}",source]
            proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = proc.communicate()
            try:
                if re.search('Unrecoverable error, exit code 1', str(stderr)) is not None: 
                    continue
                if re.search('requires a password for access', str(stderr)) is not None:
                    continue
                ret = re.search('(?P<pages>[0-9]{1,})',str(stderr))
                if 'pages' in ret.groupdict():
                    pages = int(ret.group('pages'))
                
                for field in ['MediaBox','CropBox']:
                    ret = re.search(f"{field}:\s\[(?P<top>[\d\.]+).(?P<left>[\d\.]+).(?P<width>[\d\.]+).(?P<height>[\d\.]+)",str(stderr))
                    if ret:
                        width = float(ret.group('width'))/72*2.54
                        height = float(ret.group('height'))/72*2.54
                        size = f"{width:.2f} cm x {height:.2f} cm"

                for field in ['Author', 'Title','Subject', 'Keywords', 'Creator', 'Producer', 'ModDate', 'CreationDate']:
                    ret = re.search(f"{field}:\s(?P<{field}>.+)",str(stderr).replace('\\n','\n'),flags=re.IGNORECASE)
                    
                    if ret:
                        if field in ['ModDate', 'CreationDate']:
                            try:
                                pdfDate = datetime.strptime(ret.group(field).replace("'",':')[:-1],'D:%Y%m%d%H%M%S%z')
                            except:
                                try:
                                    pdfDate = datetime.strptime(ret.group(field),"D:%Y%m%d%H%M%SZ")
                                except:
                                    try:
                                        pdfDate = datetime.strptime(ret.group(field)[:16],'D:%Y%m%d%H%M%S')
                                    except:
                                        pdfDate = None
                            finally:
                                if pdfDate is not None:
                                    row.append(pdfDate.strftime('%d/%m/%Y %H:%M:%S %Z'))

                                else:
                                    row.append('n/a')
                                
                        else:
                            if ret.group(field).encode() in [b'\\xfe\\xff']:
                                row.append('')
                            else:
                                row.append(ret.group(field).encode().decode('unicode_escape'))
                    else:
                        row.append('n/a')
                
            except Exception as e:
                print(e)
            finally:
                row += [pages,size]
                table.append(row)
                table.append(SEPARATING_LINE)
                
    headers = ["Fichiers", "Auteurs", "Titres", "Sujets", "Mot-clefs", "Créateurs", "Producteurs", "Dates modifications", "Dates creations", "Pages", "Dimensions"]          
    print(tabulate(table,headers=headers, maxcolwidths=[40,20,20,20,20,20,20,32,32]))
    if csvFilename:
        import csv
        with open(csvFilename, 'w', newline='') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter='\t')
            spamwriter.writerows([headers])
            for line in [r for r in table if r != '\x01']:
                spamwriter.writerows([line])

def reduction(dossierSource, dossierDestination, dpi=None, version="1.4", replace=False, password="", profile="default", colorStrategy=None, compression=None, downsample=None, paperSize=None):
    global ghostscript
    source_size = 0
    dest_size = 0
    nbr_file = 0

    for path, subdirs, files in os.walk(dossierSource):
        fichiers = [file for file in files if os.path.splitext(file)[1]==".pdf"]
        for fichier in fichiers:
            source = os.path.join(path, fichier)
            destination = source.replace(os.path.dirname(source),dossierDestination)
            
            if os.path.exists(destination) and not replace:
                continue

            destinationFinale = destination
            if replace:
                destination=re.sub('(?i)'+re.escape(".pdf"), lambda m:  ".tmp", destination)

            cmd = [ghostscript, '-sDEVICE=pdfwrite', '-dNOPAUSE', '-dBATCH']
            
            if paperSize:
                cmd += [f"-sPAPERSIZE={paperSize}","-dFIXEDMEDIA","-dPDFFitPage"]

            if profile !="default":
                cmd += [f"-dPDFSETTINGS=/{profile}"]
            if colorStrategy:
                if colorStrategy=="Gray":
                    cmd += ['-sColorConversionStrategy=Gray', '-dDownsampleGrayImages=true']
                    if dpi:
                        cmd += [f"-dGrayImageResolution={dpi}", "-dDownsampleGrayImages=true"]
                elif colorStrategy in ["RGB","CMYK"]:
                    cmd += [f"-sColorConversionStrategy={colorStrategy}", '-dDownsampleColorImages=true']
                    if dpi:
                        cmd += [f"-dColorImageResolution={dpi}", "-dDownsampleColorImages=true"]
            else:
                if dpi:
                    cmd += [f"-dMonoImageResolution={dpi}","-dDownsampleMonoImages==true"]
                    cmd += [f"-dGrayImageResolution={dpi}","-dDownsampleGrayImages=true"]
                    cmd += [f"-dColorImageResolution={dpi}","-dDownsampleColorImages=true"]

            if compression:
                cmd += [f"-dCompression=/{compression}"]
            if downsample:
                cmd += [f"dMonoImageDownsampleType==/{downsample}"]
                cmd += [f"dGrayImageDownsampleType==/{downsample}"]
                cmd += [f"dColorImageDownsampleType==/{downsample}"]

            cmd += [f"-dCompatibilityLevel={version}"]
            if password != "":
                cmd += [f"-sPDFPassword={password}"]
            

            cmd += [f"-sOutputFile={destination}", f"{source}"]

            try:
                cli(cmd,source=source,pages=numberOfPage(source=source, password=password))
                source_size += os.stat(source).st_size
                dest_size += os.stat(destination).st_size

                if replace and os.path.exists(destinationFinale):
                    os.remove(destinationFinale)
                    shutil.move(destination,destinationFinale)
                elif replace:
                    shutil.move(destination,destinationFinale)
                    
            except FileNotFoundError:
                if os.path.exists(source):
                    shutil.copyfile(source,destination)
            except Exception as e:
                print(e)

            nbr_file += 1

    return nbr_file,source_size,dest_size 

if __name__ == "__main__":
    description="Réduction de la taille des fichiers PDF"
    parser = argparse.ArgumentParser(description=description,exit_on_error=False)
    parser.add_argument("source", help="Dossier source",type=str)
    parser.add_argument("-d","--dpi", help="Points par pouce",type=int,default=None)
    parser.add_argument("-p","--password", help="Mot de passe pour les documents vérouillés",type=str,default="")
    parser.add_argument("-v","--version", help="Version du document PDF (défaut=1.4)",type=str,default="1.4",)
    parser.add_argument("-r","--replace", help="Remplacer les fichiers existants",type=str, choices=['o','oui','y', 'yes', 'n','non','no'],default='n')
    parser.add_argument("-k","--strategy", help="Stratégie de conversion des couleurs",type=str, choices=["LeaveColorUnchanged", "Gray", "RGB", "CMYK"],default='LeaveColorUnchanged')
    parser.add_argument("-z","--compression", help="Méthode de compression des images",type=str, choices=["LZW", "Flate", "jpeg", "RLE"],default=None)
    parser.add_argument("-m","--downsample", help="Méthode de transformation des images",type=str, choices=["Subsample", "Average", "Bicubic"],default=None)
    parser.add_argument("-e","--papersize", help="Appliquer à tout le document un format de page",type=str, choices=paper,default=None)
    parser.add_argument("-s","--profile", help="Profile Distiller",type=str, choices=getProfile(),default='default')
    parser.add_argument("-c","--csv", help="Enregistrer les informations dans un fichier CSV",type=str,default="",)
    parser.add_argument("-o", "--destination", help="Dossier de destination",type=str)
    try:
        args = parser.parse_args()
        replace = False if args.replace.startswith("n") else True
        if ghostscript is None:
            print("Ghostscript n'a pas été trouvé. Veuillez l'installer.")
        elif os.path.exists(args.source) and args.destination is None:
            get_infos(dossierSource=args.source,password=args.password,csvFilename=args.csv)
        elif os.path.exists(args.source):       
            if not os.path.exists(args.destination):
                os.makedirs(args.destination)
            nbr_file,source_size,dest_size = reduction(dossierSource=args.source, 
                                                    dossierDestination=args.destination, 
                                                        dpi=args.dpi, version=args.version, replace=replace, password=args.password, 
                                                        profile=args.profile, colorStrategy=args.strategy, compression=args.compression, downsample=args.downsample, paperSize=args.papersize)
                
            print(f"Nbr de fichiers: {nbr_file}\tSources: {source_size / (1024*1024):.2f} mbytes\tDestinations: {dest_size / (1024*1024):.2f} mbytes soit gain de {max(0,1-(dest_size/source_size)):.2%}")
    except argparse.ArgumentError as e:
        print(e)
    except ZeroDivisionError:
        print("Aucun fichier n'a été traité")
    except Exception as e:
        print(e)
