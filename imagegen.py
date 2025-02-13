from gradio_client import Client
import shutil


client = Client("KingNish/Realtime-FLUX")
result = client.predict(
		prompt="Hello!!",
		seed=42,
		width=500,
		height=500,
		api_name="/generate_image"
)


image_path = result[0]  # La ruta de la imagen generada


# Copiar la imagen a otro directorio o guardarla con otro nombre
shutil.copy(image_path, 'generated_image.png')
