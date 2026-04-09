from PIL import Image, ImageDraw
import numpy as np

def converter_cinza(caminho_imagem):
    img_colorida = Image.open(caminho_imagem)
    largura, altura = img_colorida.size

    img_cinza = Image.new("L", (largura, altura))

    pixels_coloridos = img_colorida.load()
    pixel_cinza = img_cinza.load()

    for x in range(largura):
        for y in range(altura):
            r, g, b = pixels_coloridos[x, y]
            cinza = int(r * 0.299 + g * 0.587 + b * 0.114)
            pixel_cinza[x, y] = cinza

    resultado = Image.new("RGB", (largura * 2, altura))
    resultado.paste(img_colorida, ( 0, 0))
    resultado.paste(img_cinza, (largura, 0))
    resultado.show()

    return img_colorida, img_cinza

def binarizar_imagem(img_cinza, limiar=128):
    img_binaria = img_cinza.point(lambda p: 255 if p > limiar else 0, mode='1')
    largura, altura =img_binaria.size
    resultado = Image.new("RGB", (largura * 2, altura))
    resultado.paste(img_cinza, (0,0))
    resultado.paste(img_binaria, (largura, 0))
    resultado.show()

if __name__ == "__main__":
    _, cinza = converter_cinza("james_web_photo.jpg")
    binarizar_imagem(cinza)