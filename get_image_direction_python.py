#!/usr/bin/env python
# -*- coding: utf-8 -*-

import progressbar
import os
from PIL.ExifTags import GPSTAGS
from PIL.ExifTags import TAGS

from PIL import Image
print("Iniciando extração de direção do 360 ...")
bar = progressbar.ProgressBar()


saida = open("./saida.csv", 'w', encoding='utf-8', errors="surrogateescape")
#EXIF_GPSImgDirection
saida.writelines('nome;direcao\n')

def get_exif(filename):
    image = Image.open(filename)
    image.verify()
    return image._getexif()

def get_geotagging(exif):
    if not exif:
        raise ValueError("No EXIF metadata found")

    geotagging = {}
    for (idx, tag) in TAGS.items():
        if tag == 'GPSInfo':
            if idx not in exif:
                raise ValueError("No EXIF geotagging found")

            for (key, val) in GPSTAGS.items():
                if val == 'GPSImgDirection':
                    if key in exif[idx]:
                        return exif[idx][key]

    return 'none'



pasta = './'
for diretorio, subpastas, arquivos in os.walk(pasta):
    bar.start(len(arquivos))
    i=0
    for arquivo in arquivos:
        if 'jpg' in arquivo:
            caminho = os.path.join(os.path.realpath(arquivo))
            exif = get_exif(caminho)
            direcao = get_geotagging(exif)
            linha = arquivo + " ; " + str(direcao)
            saida.writelines(linha+"\n")
            i+=1
            bar.update(i)

saida.close()

