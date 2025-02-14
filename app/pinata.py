# app/pinata.py


import requests
import json
import os


PINATA_API_KEY = os.getenv('PINATA_API_KEY')
PINATA_SECRET = os.getenv('PINATA_SECRET')

def upload_to_pinata(image_path, metadata):

    print("pinata key", PINATA_API_KEY)
    files = {'file': open(image_path, 'rb')}
    headers = {
        'pinata_api_key': PINATA_API_KEY,
        'pinata_secret_api_key': PINATA_SECRET
    }
    image_response = requests.post(
        "https://api.pinata.cloud/pinning/pinFileToIPFS",
        files=files,
        headers=headers
    )
    image_hash = image_response.json()['IpfsHash']
    
    metadata['image'] = f"ipfs://{image_hash}"
    json_response = requests.post(
        "https://api.pinata.cloud/pinning/pinJSONToIPFS",
        json=metadata,
        headers=headers
    )
    metadata_hash = json_response.json()['IpfsHash']
    
    #print(f"Image: ipfs://{image_hash}")
    #print(f"Metadata: ipfs://{metadata_hash}")
    return metadata_hash


def get_pinata_content(ipfs_hash):
    clean_hash = ipfs_hash.replace('ipfs://', '')
    
    gateway_url = "https://silver-big-wren-685.mypinata.cloud/ipfs"
    
    metadata_url = f"{gateway_url}/{clean_hash}"
    response = requests.get(metadata_url)
    
    if response.status_code != 200:
        raise Exception(f"Error: {response.status_code}")
    
    metadata = response.json()
    image_hash = metadata.get('image').replace('ipfs://', '')
    
    image_url = f"{gateway_url}/{image_hash}"

    return metadata, image_url


def main():
   test_image = "assets/image1.webp"
   test_metadata = {
       "title": "42rocket",
       "artist": "imontero"
      }
   
   try:
        ipfs_uri = upload_to_pinata(test_image, test_metadata)
        
        metadata, image_url = get_pinata_content(ipfs_uri)
            
        print("Metadata:", metadata)
        print("Image URL:", image_url) 
   except Exception as e:
       print(f"Error: {e}")

if __name__ == "__main__":
   main()