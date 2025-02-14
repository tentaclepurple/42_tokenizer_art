from gradio_client import Client
import shutil


def generate_image(prompt):
	image_path = None
	
	client = Client("KingNish/Realtime-FLUX")
	result = client.predict(
		prompt=f"{prompt} with the number 42",
		seed=42,
		width=512,
		height=512,
		api_name="/generate_image"
	)
	if result:
		image_path = result[0]
		shutil.copy(image_path, 'assets/generated.webp')

	return image_path



