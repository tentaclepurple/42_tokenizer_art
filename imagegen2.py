from gradio_client import Client
import requests
import shutil


client = Client("stabilityai/stable-diffusion-3.5-large")
result = client.predict(
		prompt="A rocket with the number 42",
		negative_prompt="Hello!!",
		seed=0,
		randomize_seed=True,
		width=250,
		height=250,
		guidance_scale=4.5,
		num_inference_steps=40,
		api_name="/infer"
)

print(result)


image_path = result[0]  # La ruta de la imagen generada

# Ahora puedes mover o copiar la imagen si lo deseas


# Copiar la imagen a otro directorio o guardarla con otro nombre
shutil.copy(image_path, 'generated_image.png')

print(f"Imagen guardada en 'generated_image.webp'")