from skimage.metrics import structural_similarity as ssim
import cv2
import os



def compare_images(imageA, imageB):
    # Convierte las imágenes a escala de grises
    grayA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
    grayB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)

    # Calcula el índice de similitud estructural (SSIM)
    score, _ = ssim(grayA, grayB, full=True)
    return score

# Ruta a la carpeta de imágenes
def elimina_duplicados(image_folder):
    threshold = 0.8  # Umbral para eliminar imágenes similares (entre 0 y 1)
    removed_images = 0

    # Recorrer todas las carpetas y subcarpetas dentro de image_folder
    for root, dirs, files in os.walk(image_folder):
        # Obtener todas las imágenes en la carpeta actual (root) y ordenarlas alfabéticamente
        images = sorted([f for f in files if f.endswith(".png")])

        for i in range(len(images) - 1):
            imageA_path = os.path.join(root, images[i])
            imageB_path = os.path.join(root, images[i + 1])

            imageA = cv2.imread(imageA_path)
            imageB = cv2.imread(imageB_path)

            if imageA is None or imageB is None:
                print(f"No se pudo cargar una de las imágenes, saltando... {imageA_path} o {imageB_path}")
                continue

            similarity_score = compare_images(imageA, imageB)
            if similarity_score > threshold:
                # Eliminar la imagen si es muy similar a la anterior
                os.remove(imageB_path)
                removed_images += 1
                print(f"Imagen eliminada: {imageB_path} por ser similar a {imageA_path}")

    return removed_images

def is_blurry(image, threshold=90.0):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    laplacian_var = cv2.Laplacian(gray, cv2.CV_64F).var()
    return laplacian_var < threshold

def elimina_borrosas(image_folder):
    blurry_images = 0

    # Recorrer todas las carpetas y subcarpetas dentro de image_folder
    for root, dirs, files in os.walk(image_folder):
        images = [f for f in files if f.endswith(".png")]

        for img in images:
            image_path = os.path.join(root, img)  # Usar root para obtener la ruta completa de la imagen
            image = cv2.imread(image_path)

            if image is None:
                print(f"No se pudo cargar la imagen {img}, saltando...")
                continue

            if is_blurry(image):
                os.remove(image_path)
                blurry_images += 1
                #print(f"Imagen borrosa eliminada: {image_path}")

    return blurry_images


def resize_images(image_folder, output_folder, size=(640, 640)):
    # Crear la carpeta de salida si no existe
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Inicializar un contador global para los nombres correlativos
    global_counter = 754

    # Recorrer todas las carpetas y subcarpetas dentro de image_folder
    for root, dirs, files in os.walk(image_folder):
        # Obtener todas las imágenes en la carpeta actual (root) y ordenarlas alfabéticamente
        images = sorted([f for f in files if f.endswith(".png")])

        # Redimensionar cada imagen y guardarla con un nombre correlativo
        for img in images:
            img_path = os.path.join(root, img)
            image = cv2.imread(img_path)

            if image is None:
                print(f"No se pudo cargar la imagen {img}, saltando...")
                continue

            # Redimensionar la imagen
            resized_image = cv2.resize(image, size)

            # Guardar la imagen redimensionada con nombre correlativo en la carpeta de salida
            output_filename = f"img_{global_counter:05d}.png"
            cv2.imwrite(os.path.join(output_folder, output_filename), resized_image)

            # Incrementar el contador global
            global_counter += 1

    return global_counter



image_folder = "./dataset/output"
output_folder = "./dataset/output-final"


# blurry_images= elimina_borrosas (image_folder)
# print(f"{blurry_images} imágenes eliminadas por ser borrosas.")

# removed_images = elimina_duplicados(image_folder)
# print(f"{removed_images} imágenes eliminadas por ser similares.")

# Redimensionar las imágenes a 416x416 píxeles
global_counter= resize_images(image_folder, output_folder, size=(640, 640))
print(f"Se redimensionaron y guardaron {global_counter} imágenes en la carpeta '{output_folder}'.")


