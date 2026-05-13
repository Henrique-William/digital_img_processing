import rawpy  # type: ignore
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import convolve

if __name__ == "__main__":
    with rawpy.imread("geraldo.dng") as raw:
        imagem_crua = raw.raw_image_visible.copy().astype(np.float32)
        cores = raw.raw_colors_visible

        nv_preto = np.max(raw.black_level_per_channel)
        nv_branco = raw.white_level
        imagem_crua = np.clip((imagem_crua - nv_preto) / (nv_branco - nv_preto),0,1)

        R_esparso = imagem_crua * (cores == 0)
        G_esparso = imagem_crua * ((cores == 1) | (cores == 3))
        B_esparso = imagem_crua * (cores == 2)

        K_RB = np.array((
            (0.25, 0.50, 0.25),
            (0.50, 1.00, 0.50),
            (0.25, 0.50, 0.25)
        ))

        K_G = np.array((
            (0.00, 0.25, 0.00),
            (0.25, 1.00, 0.25),
            (0.00, 0.25, 0.00)
        ))

        R = convolve(R_esparso, K_RB, mode="mirror")
        G = convolve(G_esparso, K_G, mode="mirror")
        B = convolve(B_esparso, K_RB, mode="mirror")

        rgb = np.dstack([R,G,B])

        media = np.mean(rgb, axis=(0,1))

        rgb[:,:,0] *= (media[1] / media[0]) * 0.83  #0.83
        rgb[:,:,2] *= (media[1] / media[0]) * 0.90  #0.90
        rgb = np.clip(rgb,0,1)

        L = rgb[:,:,0] * 0.299 + rgb[:,:,1] * 0.587 + rgb[:,:,2] * 0.114
        L = L[:,:, np.newaxis]

        rgb_final = L + 1.5 * (rgb - L)
        rgb_final = np.clip(rgb_final, 0, 1)

        rgb_final = np.clip(rgb_final * 2.0, 0, 1)
        gama = 1.0/2.2
        rgb_final = np.power(np.maximum(rgb_final, 1e-6), gama)

        rgb_final = np.rot90(rgb_final, k=-1)

        plt.figure(figsize=(10,12))
        plt.imshow(rgb_final)
        plt.axis("off")
        plt.show()