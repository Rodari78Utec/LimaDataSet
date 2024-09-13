import cv2
import os

# Parámetros
video_folder = "./dataset/input"  # Ruta a la carpeta donde están los videos
output_folder = "./dataset/output"   # Carpeta principal para almacenar las imágenes extraídas
n_seconds = 1  # Intervalo en segundos para capturar fotogramas

# Crear la carpeta principal para almacenar las imágenes extraídas, si no existe
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Procesar cada video en la carpeta de videos
for video_name in os.listdir(video_folder):
    if video_name.endswith(('.mp4', '.mov', '.MP4', '.MOV')):  # Filtrar archivos de video
        video_path = os.path.join(video_folder, video_name)

        # Cargar el video
        cap = cv2.VideoCapture(video_path)

        # Obtener la tasa de cuadros por segundo (FPS) del video
        fps = cap.get(cv2.CAP_PROP_FPS)

        # Calcular el número de cuadros que corresponden a n segundos y asegurarse de que sea un entero
        frame_interval = int(fps * n_seconds)
        print(f"Procesando video: {video_name}")
        print(f"FPS del video: {fps}")
        print(f"Intervalo de fotogramas: {frame_interval}")

        # Crear una subcarpeta para cada video en la carpeta de salida
        video_output_folder = os.path.join(output_folder, os.path.splitext(video_name)[0])
        if not os.path.exists(video_output_folder):
            os.makedirs(video_output_folder)

        # Extraer y guardar fotogramas cada n segundos
        frame_number = 0
        saved_frames = 0

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # Guardar el fotograma si es el correspondiente al intervalo
            if frame_number % frame_interval == 0:
                cv2.imwrite(f"{video_output_folder}/frame_{saved_frames:04d}.png", frame)
                saved_frames += 1

            frame_number += 1

        cap.release()
        print(f"Se han guardado {saved_frames} fotogramas del video {video_name}.")

cv2.destroyAllWindows()

print("Proceso completado.")
