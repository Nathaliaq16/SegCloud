from google.cloud import storage
import os
import uuid

# Configurar la conexión con GCS
BUCKET_NAME = "mi-bucket-carros"

def upload_image_to_gcs(file):
    """Sube una imagen al bucket de GCP y devuelve la URL pública."""
    try:
        storage_client = storage.Client()
        bucket = storage_client.bucket(BUCKET_NAME)

        # Generar un nombre único para la imagen
        file_extension = file.filename.split('.')[-1]
        blob_name = f"{uuid.uuid4()}.{file_extension}"

        blob = bucket.blob(blob_name)
        blob.upload_from_file(file, content_type=file.content_type)
        blob.make_public()  # Hacer la imagen accesible públicamente

        return blob.public_url
    except Exception as e:
        print(f"Error al subir la imagen: {e}")
        return None
