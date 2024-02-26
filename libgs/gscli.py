#!/usr/bin/env python3
# -*- coding: utf-8 -*-

##################################################
## Conversion PDF
## avec Ghostscript libgs
##################################################
## Author: Gilles BIHAN
## Copyright: © 2024, Converio.fr gilles-bihan.fr
## Version: 1.0.0
## Email: gilles.bihan@converio.fr
## Status: Dev
##################################################

try:
    import gsapi
except Exception:
    print('Failure to import gsapi. Check shared library path')
    raise

import sys, tempfile, os, argparse, shutil, re, glob
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

# Format de page
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

csvInfos = []

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
            stdout += (ret[0] + '\n')
        else:
            stdout += s
        
    gsapi.gsapi_set_stdio(instance, None, stdout_info, None)
    gsapi.gsapi_set_arg_encoding(instance, gsapi.GS_ARG_ENCODING_UTF8)
    gsapi.gsapi_add_control_path(instance, gsapi.GS_PERMIT_FILE_READING, fichier)
    gsapi.gsapi_init_with_args(instance, parametres)

    gsapi.gsapi_exit(instance)
    gsapi.gsapi_delete_instance(instance)

    infos = {'pages':'0', '_CreationDate':''}

    infos['_CreationDate'] = datetime.strftime(datetime.now(timezone.utc).astimezone(get_localzone()), 'D:%Y%m%d%H%M%S%z')
    infos['_CreationDate'] = f"{infos['_CreationDate'][:-2]}'{infos['_CreationDate'][19:]}'"

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

def conversion(source, destination, args, tmpdirname):
    #global bar
    def stdout_fn(caller_handle, bytes_):
        #global bar
        m = re.search("Page (?P<page>[0-9]{1,})",bytes_.decode('utf-8',errors="ignore"))
        if m:
            if bar:
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

    destinationTemp = os.path.join(tmpdirname,os.path.basename(source))

    infos = get_infos(source,args.password)
    pages = int(infos['pages'])

    if args.info or (os.path.exists(source) and destination is None):
        infos['file'] = source
        infos['basename'] = os.path.basename(source)
        file_stats = os.stat(source)
        infos['filesize'] = file_stats.st_size
        infos['filesizeMB'] = file_stats.st_size / (1024 * 1024) # MegaBytes

        csvInfos.append(infos)
        for k,v in infos.items():
            if not k.startswith("_"):
                print(f"{k}: {v}")
        return

    parametres = ['gs', '-dNOPAUSE', '-dBATCH']
    if args.release:
        parametres += [f"-dCompatibilityLevel={args.release}"]
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
        parametres += [f"-dMonoImageDownsampleType=/{args.downsample}"]
        parametres += [f"-dGrayImageDownsampleType=/{args.downsample}"]
        parametres += [f"-dColorImageDownsampleType=/{args.downsample}"]

    if args.lockpwd:
        parametres += [f"-sUserPassword={args.lockpwd}"]
        if not args.admpwd:
            args.admpwd = args.lockpwd
    if args.admpwd:
        parametres += [f"-sOwnerPassword={args.admpwd}"]
                
        if args.permissions:
            mask=0b11000000
            if "print" in args.permissions:
                mask = mask | (1 << 2)
            if "change" in args.permissions:
                mask = mask | (1 << 3)
            if "extract" in args.permissions:
                mask = mask | (1 << 4) 
            if "annotation" in args.permissions:
                mask = mask | (1 << 5) 
            if "fill" in args.permissions:
                mask = mask | (1 << 8) 
            if "copy" in args.permissions:
                mask = mask | (1 << 9) 
            if "quality" in args.permissions:
                mask = mask | (1 << 11)
            parametres += [f"-dEncryptionR=3","-dKeyLength=128"]
            parametres += [f"-dPermissions={mask}"]
    parametres += ['-sDEVICE=pdfwrite', f"-sOutputFile={destinationTemp}" , "-f", source]

    metadatas = ""
    for metadata in ['title', 'author', 'subject', 'keywords', 'creator', 'producer']:
        if args.__getattribute__(metadata):
            ret = re.search('\A\"?(?P<metadata>[^\"]*)\"?\Z',args.__getattribute__(metadata))
            if ret:
                metadatas += f"/{str(metadata).capitalize()} ({ret.group('metadata')}) "
          
    modDate = datetime.strftime(datetime.now(timezone.utc).astimezone(get_localzone()), 'D:%Y%m%d%H%M%S%z')
    modDate = f"{modDate[:-2]}'{modDate[19:]}'"
    creationDate = infos["_CreationDate"][:23]
    parametres += ['-c', f"[{metadatas}/ModDate ({modDate}) /CreationDate ({creationDate}) /DOCINFO pdfmark"]
    print(" ".join(parametres))
    with tqdm(total=int(pages)) as bar:
        bar.set_description_str(os.path.basename(source))
        instance = gsapi.gsapi_new_instance(0)
    
        gsapi.gsapi_set_stdio(instance, None, stdout_fn, stderr_fn)
        gsapi.gsapi_set_arg_encoding(instance, gsapi.GS_ARG_ENCODING_UTF8)
        gsapi.gsapi_add_control_path(instance, gsapi.GS_PERMIT_FILE_READING, tmpdirname)
        gsapi.gsapi_init_with_args(instance, parametres)

        gsapi.gsapi_exit(instance)
        gsapi.gsapi_delete_instance(instance)

    if (os.path.exists(destination) and args.replace) or (not os.path.exists(destination)):
        shutil.copyfile(destinationTemp,destination)

if __name__ == '__main__':
    description = "Conversion de fichier au format PDF"
    epilog = "Utilisation de libgs (https://ghostscript.com)"
    parser = argparse.ArgumentParser(description=description,epilog=epilog,exit_on_error=False)
    parser.add_argument('-v','--version', action='version', version='%(prog)s 1.0.0')
    parser.add_argument("source", help="Fichier source",type=str, default='', nargs="*")
    parser.add_argument("-o", "--destination", help="Fichier ou Dossier de destination",type=str)
    parser.add_argument("--replace", help="Remplacement des fichiers existants",action=argparse.BooleanOptionalAction,default=False)
    parser.add_argument("--recursive", help="Recherche dans les dossiers et sous-dossiers",action=argparse.BooleanOptionalAction,default=False)
    parser.add_argument("-p","--password", help="Mot de passe pour les documents vérouillés",type=str,default=None)
    parser.add_argument("--lockpwd", help="Mot de passe pour vérouiller l'ouverture du document",type=str,default=None)
    parser.add_argument("--admpwd", help="Mot de passe du propriétaire du document",type=str,default=None)
    parser.add_argument("--permissions", help="Permissions accordés",type=str, choices=['print','change','extract','fill','copy','annotation','quality','none'], nargs="*", default=None)
    parser.add_argument("-d","--dpi", help="Points par pouce",type=int,default=None)
    parser.add_argument("-r","--release", help="Version du document PDF (défaut=1.4)",type=str,default="1.4",)
    parser.add_argument("--strategy", help="Stratégie de conversion des couleurs",type=str, choices=["Gray", "RGB", "CMYK"],default=None)
    parser.add_argument("--gray", help="Conversion en niveaux de gris (8 bits)",dest="strategy", const="Gray", nargs="?")
    parser.add_argument("--rgb", help="Conversion en couleurs (24 bits)",dest="strategy", const="RGB", nargs="?")
    parser.add_argument("--cmyk", help="Conversion en CMYK (32 bits)",dest="strategy", const="CMYK", nargs="?")
    parser.add_argument("--compression", help="Méthode de compression des images",type=str, choices=["LZW", "Flate", "jpeg", "RLE"],default=None)
    parser.add_argument("--lzw", help="Compression sans perte",dest="compression", const="LZW", nargs="?")
    parser.add_argument("--flate", help="Compression sans perte basée sur GZIP/ZIP ",dest="compression", const="Flate", nargs="?")
    parser.add_argument("--jpeg", help="Compression avec perte",dest="compression", const="jpeg", nargs="?")
    parser.add_argument("--rle", help="Compression simple sans perte basée sur la répétition des données (run-length encoding ou RLE)",dest="compression", const="RLE", nargs="?")
    parser.add_argument("--downsample", help="Algorithme de rééchantillonage des images",type=str, choices=["Subsample", "Average", "Bicubic"],default=None)
    parser.add_argument("--subsample", help="Algorithme de rééchantillonage plus rapide",dest="downsample", const="Subsample", nargs="?")
    parser.add_argument("--average", help="Algorithme de rééchantillonage intermédiaire",dest="downsample", const="Average", nargs="?")
    parser.add_argument("--bicubic", help="Algorithme de rééchantillonage qualitatif (plus lent)",dest="downsample", const="Bicubic", nargs="?")
    parser.add_argument("--papersize", help="Appliquer à tout le document un format de page",type=str, choices=paper,default=None)
    parser.add_argument("--profile", help="Profile Distiller",type=str, choices=getProfile(),default=None)
    parser.add_argument("-i","--info", help="Informations sur le fichier",action='store_true',default=False)
    parser.add_argument("--title", help="Titre du document",type=str, default=None)
    parser.add_argument("--author", help="Auteur du document",type=str, default=None)
    parser.add_argument("--subject", help="Sujet ou objet du document",type=str, default=None)
    parser.add_argument("--keywords", help="Mots clefs séparés par une virgule et un espace",type=str, default=None)
    parser.add_argument("--creator", help="Créateur",type=str, default=None)
    parser.add_argument("--producer", help="Outil de création du document",type=str, default=None)
    parser.add_argument("--csv", help="Enregistre les informations dans un fichier csv",type=str,default=None)
    parser.add_argument("--delimiter", help="Délimiteur CSV",type=str,default='\t')

    try:
        if len(sys.argv)==1:
            parser.print_help()
            exit(0)
        args = parser.parse_args()
    
        with tempfile.TemporaryDirectory() as tmpdirname:
            if args.destination is None:
                args.destination = os.path.expanduser( '~' ) # Dossier utilisateur actif
                args.destination = "/Users/gilles/Downloads/pdf1"
            if len(args.source)==1:
                source = args.source[0]
                if not os.path.exists(source):
                    sys.stderr.write(RED)
                    sys.stderr.write(f"'{source}' ne peut être utilisé")
                    sys.stderr.write(RESET)
                    exit(0)
                elif os.path.isdir(args.destination):
                    if os.path.isfile(source):
                        # fichier source -> dossier destination
                        destination = os.path.join(args.destination, os.path.basename(source))
                        conversion(source, args.destination, args, tmpdirname)
                    else:
                        # dossier source -> dossier destination
                        fichiers = glob.glob(f'{source}/**/*.pdf' if args.recursive else f'{source}/*.pdf', recursive=args.recursive)
                        for fichier in fichiers:
                            if not os.path.exists(fichier):
                                sys.stderr.write(RED)
                                sys.stderr.write(f"'{fichier}' ne peut être utilisé")
                                sys.stderr.write(RESET)
                                continue
                            destination = os.path.join(args.destination, os.path.basename(fichier))
                            conversion(fichier, destination, args, tmpdirname)
                else:
                    if os.path.isfile(source):
                        # fichier source -> fichier destination
                        conversion(source, args.destination, args, tmpdirname)
                    else:
                        fichiers = glob.glob(f'{source}/**/*.pdf' if args.recursive else f'{source}/*.pdf', recursive=args.recursive)
                        #fichiers = [os.path.join(source,fichier) for fichier in os.listdir(source) if os.path.splitext(fichier.lower())[1] == ".pdf"]
                        if not os.path.exists(args.destination):
                            try:
                                os.mkdir(args.destination)
                            except Exception as e:
                                sys.stderr.write(e)
                        for fichier in fichiers:
                            if not os.path.exists(fichier):
                                sys.stderr.write(RED)
                                sys.stderr.write(f"'{fichier}' ne peut être utilisé")
                                sys.stderr.write(RESET)
                                continue
                            destination = os.path.join(args.destination, os.path.basename(fichier))
                            conversion(fichier, destination, args, tmpdirname)

            else:
                # Plusieurs source(s) -> dossier destination
                if not os.path.exists(args.destination):
                    try:
                        os.mkdir(args.destination)
                    except Exception as e:
                        sys.stderr.write(e)
                if os.path.isdir(args.destination):
                    for source in args.source:
                        if os.path.isfile(source):
                            # Source est un fichier
                            destination = os.path.join(args.destination, os.path.basename(source))
                            conversion(source, destination, args, tmpdirname)
                        else:
                            # Source est un dossier
                            fichiers = glob.glob(f'{source}/**/*.pdf' if args.recursive else f'{source}/*.pdf', recursive=args.recursive)
                            for fichier in fichiers:
                                if not os.path.exists(fichier):
                                    sys.stderr.write(RED)
                                    sys.stderr.write(f"'{fichier}' ne peut être utilisé")
                                    sys.stderr.write(RESET)
                                    continue
                                destination = os.path.join(args.destination, os.path.basename(fichier))
                                conversion(fichier, destination, args, tmpdirname)
                else:
                    sys.stderr.write(RED)
                    sys.stderr.write("Le dossier destination ne peut être utilisé car un fichier avec ce nom existe")
                    sys.stderr.write(RESET)

    except argparse.ArgumentError as e:
        sys.stderr.write(e)
    except Exception as e:
        sys.stderr.write(e)

    if len(csvInfos)>0 and args.csv:
        headers = ["Fichiers","Noms","Taille (byte)","Taille(Megabytes)", "Auteurs", "Titres", "Sujets", "Mot-clefs", "Créateurs", "Producteurs", "Dates modifications", "Dates creations", "Pages", "Dimensions","Largeur (pts)","Hauteur (pts)"]
        fields = ["file","basename","filesize","filesizeMB","Author","Title","Subject","Keywords","Creator","Producer","ModDate","CreationDate","pages","size","width","height"]         
        import csv
        with open(args.csv, 'w', newline='', encoding='utf-8') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=args.delimiter)
            spamwriter.writerows([headers])
            for info in csvInfos:
                spamwriter.writerows([[info[n] if n in info else "" for n in fields]])
    