from gradio_client import Client
import shutil


def generate_image(prompt):
	client = Client("KingNish/Realtime-FLUX")
	result = client.predict(
		prompt=prompt,
		seed=42,
		width=512,
		height=512,
		api_name="/generate_image"
	)
	image_path = result[0]
	
	shutil.copy(image_path, 'generated_image.png')
	return 'generated_image.png'



