#!/usr/bin/env python3
# -*- coding: utf-8 -*-

##################################################
## Conversion PDF
## avec Ghostscript libgs
##################################################
## Author: Gilles BIHAN
## Copyright: Copyright 2024, Converio.fr
## Version: 1.0.0
## Email: gilles.bihan@converio.fr
## Status: Dev
##################################################

try:
    import gsapi
except Exception:
    print('Failure to import gsapi. Check shared library path')
    raise

import sys, tempfile, os, argparse, shutil, re
from tqdm import tqdm
from datetime import datetime, timezone
from tzlocal import get_localzone

__version__ = "1.0.0"

# Couleurs pour la sortie STDOUT
RED   = "\033[1;31m"  
BLUE  = "\033[1;34m"
CYAN  = "\033[1;36m"
GREEN = "\033[0;32m"
RESET = "\033[0;0m"
BOLD    = "\033[;1m"
REVERSE = "\033[;7m"

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
try:
    this_file = __file__
except NameError:
    this_file = sys.argv[0]

if getattr(sys,'frozen',False):
    basepath = getattr(sys,'_MEIPASS',os.path.dirname(sys.executable))
else:
    basepath = os.path.dirname(this_file)

def stdout_fn(caller_handle, bytes_):
    global bar
    m = re.search("Page (?P<page>[0-9]{1,})",bytes_.decode('utf-8',errors="ignore"))
    if m:
        bar.update(1)
    m = re.search("This file requires a password for access",bytes_.decode('utf-8',errors="ignore"))
    if m:
        sys.stdout.write(RED)
        print(r"Mot de passe exigé pour accèder au fichier" )
        sys.stdout.write(RESET)

def stderr_fn(caller_handle, bytes_):
    sys.stdout.write(RED)
    print(bytes_.decode('utf-8',errors="ignore"))
    sys.stdout.write(RESET)

stdout = ""
def get_infos(fichier, password=""):
    global stdout
    stdout = ""
    parametres = ["gs", "-dQUIET", "-dBATCH", "-dNODISPLAY", "-dNOPAUSE", "-dPDFINFO", "-dFirstPage=1","-dLastPage=1", f"-sPDFPassword={password}",fichier]
    instance = gsapi.gsapi_new_instance(0)
    def stdout_info(caller_handle, bytes_):
        global stdout
        expression = "^(.+?)\\\\x"
        s = bytes_.decode('utf-8',errors="backslashreplace")
        ret=re.findall(expression,s, flags=re.UNICODE)
        if len(ret)>0:
            print(ret)
            stdout += (ret[0] + '\n')
        else:
            stdout += s
        
    gsapi.gsapi_set_stdio(instance, None, stdout_info, None)
    gsapi.gsapi_set_arg_encoding(instance, gsapi.GS_ARG_ENCODING_UTF8)
    gsapi.gsapi_add_control_path(instance, gsapi.GS_PERMIT_FILE_READING, fichier)
    gsapi.gsapi_init_with_args(instance, parametres)

    gsapi.gsapi_exit(instance)
    gsapi.gsapi_delete_instance(instance)

    infos = {'pages':'0'}

    if re.search('Unrecoverable error, exit code 1', str(stdout)) is not None: 
        pass
    if re.search('requires a password for access', str(stdout)) is not None:
        sys.stdout.write(RED)
        print("Mot de passe exigé pour accèder au fichier")
        sys.stdout.write(RESET)


    for field in ['MediaBox','CropBox']:
        ret = re.search(f"{field}:\s\[(?P<top>[\d\.]+).(?P<left>[\d\.]+).(?P<width>[\d\.]+).(?P<height>[\d\.]+)",str(stdout))
        if ret:
            infos['width'] = float(ret.group('width'))
            infos['height'] = float(ret.group('height'))
            infos['size'] = f"{infos['width']/72*2.54:.2f} cm x {infos['height']/72*2.54:.2f} cm"

    for field in ['Author', 'Title','Subject', 'Keywords', 'Creator', 'Producer', 'ModDate', 'CreationDate']:
        ret = re.search(f"{field}:\s(?P<{field}>.+)",str(stdout).replace('\\n','\n'),flags=re.IGNORECASE)
        
        if ret:
            if field in ['ModDate', 'CreationDate']:
                try:
                    infos["_" + field] = ret.group(field)[:23]
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
                        infos[field] = pdfDate.strftime('%d/%m/%Y %H:%M:%S %Z')
                        
                    else:
                        infos[field]='n/a'
                    
            else:
                if ret.group(field).encode() in [b'\\xfe\\xff']:
                    infos[field]=''
                else:
                    infos[field]=ret.group(field).encode().decode('unicode_escape')
        else:
            infos[field]='n/a'

    ret = re.search('(?P<pages>[0-9]{1,})',str(stdout))
    if 'pages' in ret.groupdict():
        infos['pages'] = ret.group('pages')

    return infos

def getProfile():
    global stdout, basepath
    stdout = ""
    try:
        parametres = ['gs','-dNODISPLAY','-c', ".distillersettings {exch ==only ( ) print ==} forall quit"]

        instance = gsapi.gsapi_new_instance(0)
        def stdout_info(caller_handle, bytes_):
            global stdout
            stdout += bytes_.decode('utf-8')
            
        gsapi.gsapi_set_stdio(instance, None, stdout_info, stdout_info)
        gsapi.gsapi_set_arg_encoding(instance, gsapi.GS_ARG_ENCODING_UTF8)
        gsapi.gsapi_init_with_args(instance, parametres)

        gsapi.gsapi_exit(instance)
        gsapi.gsapi_delete_instance(instance)
    except Exception as e:
        pass
    finally:
        ret = re.findall("^\/(.*) -dict-",stdout,re.MULTILINE)
        if ret:
            return ret
    return ["screen", "ebook", "printer", "prepress"]

if __name__ == '__main__':
    description = "Conversion avec PDF"
    parser = argparse.ArgumentParser(description=description,exit_on_error=False)
    parser.add_argument("source", help="Fichier source",type=str, default='')
    parser.add_argument("-o", "--destination", help="Dossier de destination",type=str)
    parser.add_argument("-r","--replace", help="Remplacer les fichiers existants",type=str, choices=['o','oui','y', 'yes', 'n','non','no'],default='n')
    parser.add_argument("-p","--password", help="Mot de passe pour les documents vérouillés",type=str,default=None)
    parser.add_argument("-d","--dpi", help="Points par pouce",type=int,default=None)
    parser.add_argument("-v","--version", help="Version du document PDF (défaut=1.4)",type=str,default="1.4",)
    parser.add_argument("-k","--strategy", help="Stratégie de conversion des couleurs",type=str, choices=["Gray", "RGB", "CMYK"],default=None)
    parser.add_argument("-z","--compression", help="Méthode de compression des images",type=str, choices=["LZW", "Flate", "jpeg", "RLE"],default=None)
    parser.add_argument("-m","--downsample", help="Méthode de transformation des images",type=str, choices=["Subsample", "Average", "Bicubic"],default=None)
    parser.add_argument("-e","--papersize", help="Appliquer à tout le document un format de page",type=str, choices=paper,default=None)
    parser.add_argument("-s","--profile", help="Profile Distiller",type=str, choices=getProfile(),default=None)
    parser.add_argument("-i", help="Informations sur le fichier",action='store_true',default=False)
    parser.add_argument("--title", help="Titre du document",type=str, default=None)
    parser.add_argument("--author", help="Auteur du document",type=str, default=None)
    parser.add_argument("--subject", help="Sujet ou objet du document",type=str, default=None)
    parser.add_argument("--keywords", help="Mots clefs séparés par une virgule et un espace (\\ )",type=str, default=None)
    parser.add_argument("--creator", help="Créateur",type=str, default=None)
    parser.add_argument("--producer", help="Outil de création du document",type=str, default=None)
    try:
        if len(sys.argv)==1:
            exit(0)
        args = parser.parse_args()
        with tempfile.TemporaryDirectory() as tmpdirname:
            source = args.source
            destination = args.destination
            replace = False if args.replace.startswith("n") else True
            destinationTemp = os.path.join(tmpdirname,os.path.basename(source))

            infos = get_infos(source,args.password)
            pages = int(infos['pages'])

            if args.i or (os.path.exists(args.source) and args.destination is None):
                print(f"Fichier: {source}")
                for k,v in infos.items():
                    if not k.startswith("_"):
                        print(f"{k}: {v}")
                exit(0)

            parametres = ['gs', '-dNOPAUSE', '-dBATCH']
            if args.version:
                parametres += [f"-dCompatibilityLevel={args.version}"]
            if args.papersize:
                parametres += [f"-sPAPERSIZE={args.papersize}","-dFIXEDMEDIA","-dPDFFitPage"]
            if args.profile:
                parametres += [f"-dPDFSETTINGS=/{args.profile}"]
            if args.password:
                parametres += [f"-sPDFPassword={args.password}"]
            if args.strategy:
                if args.strategy=="Gray":
                    parametres += ['-sColorConversionStrategy=Gray', '-dDownsampleGrayImages=true']
                    if args.dpi:
                        parametres += [f"-dGrayImageResolution={args.dpi}", "-dDownsampleGrayImages=true"]
                elif args.strategy in ["RGB","CMYK"]:
                    parametres += [f"-sColorConversionStrategy={args.strategy}", '-dDownsampleColorImages=true']
                    if args.dpi:
                        parametres += [f"-dColorImageResolution={args.dpi}", "-dDownsampleColorImages=true"]
            else:
                if args.dpi:
                    parametres += [f"-dMonoImageResolution={args.dpi}","-dDownsampleMonoImages==true"]
                    parametres += [f"-dGrayImageResolution={args.dpi}","-dDownsampleGrayImages=true"]
                    parametres += [f"-dColorImageResolution={args.dpi}","-dDownsampleColorImages=true"]

            if args.compression:
                parametres += [f"-dCompression=/{args.compression}"]
            if args.downsample:
                parametres += [f"dMonoImageDownsampleType==/{args.downsample}"]
                parametres += [f"dGrayImageDownsampleType==/{args.downsample}"]
                parametres += [f"dColorImageDownsampleType==/{args.downsample}"]

            parametres += ['-sDEVICE=pdfwrite', f"-sOutputFile={destinationTemp}" , "-f", source]

            metadatas = ""
            for metadata in ['title', 'author', 'subject', 'keywords', 'creator', 'producer']:
                if args.__getattribute__(metadata):
                    metadatas += f"/{str(metadata).capitalize()} ({args.__getattribute__(metadata)}) "
          
            modDate = datetime.strftime(datetime.now(timezone.utc).astimezone(get_localzone()), 'D:%Y%m%d%H%M%S%z')
            modDate = f"{modDate[:-2]}'{modDate[19:]}'"
            creationDate = infos["_CreationDate"][:23]
            parametres += ['-c', f"[{metadatas}/ModDate ({modDate}) /CreationDate ({creationDate}) /DOCINFO pdfmark"]

            with tqdm(total=int(pages)) as bar:
                bar.set_description_str(os.path.basename(args.source))
                instance = gsapi.gsapi_new_instance(0)
    
                gsapi.gsapi_set_stdio(instance, None, stdout_fn, stderr_fn)
                gsapi.gsapi_set_arg_encoding(instance, gsapi.GS_ARG_ENCODING_UTF8)
                gsapi.gsapi_add_control_path(instance, gsapi.GS_PERMIT_FILE_READING, tmpdirname)
                gsapi.gsapi_init_with_args(instance, parametres)

                gsapi.gsapi_exit(instance)
                gsapi.gsapi_delete_instance(instance)

            if (os.path.exists(destination) and replace) or (not os.path.exists(destination)):
                shutil.copyfile(destinationTemp,destination)

    except argparse.ArgumentError as e:
        print(e)
    except Exception as e:
        print(e)

    