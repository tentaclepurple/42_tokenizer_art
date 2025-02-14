import streamlit as st
from PIL import Image
import os
from pinata import upload_to_pinata, get_pinata_content
from interact import run_js_script
import tempfile
import requests





def get_nft_collection():
    result = run_js_script('deployment/getTokenURIs.js')
    
    import json
    try:
        print(result)

        uris = result.replace("Token URIs: ", "")
        uris_string = result.replace("Token URIs: ", "").replace("'", '"')
        uris = json.loads(uris_string)

        valid_nfts = []
        for uri in uris:
            try:
                metadata, image_url = get_pinata_content(uri)

                if 'title' not in metadata or 'artist' not in metadata:
                    print(f"Invalid metadata")
                    continue
                
                # Verificar que la imagen es válida
                response = requests.head(image_url)
                if not response.headers.get('content-type', '').startswith('image/'):
                    print(f"Invalid URL")
                    continue
                
                valid_nfts.append({
                    'title': metadata['title'],
                    'artist': metadata['artist'],
                    'image_url': image_url
                })
                
            except Exception as e:
                print(f"Error processing NFT {uri}: {str(e)}")
                continue
                
        return valid_nfts
        
    except Exception as e:
        print(f"Error processing result: {str(e)}")
        return []


def check_image(image_file):
    MAX_SIZE = 5 * 1024 * 1024  # 5MB
    if image_file.size > MAX_SIZE:
        return False, "Imagen demasiado grande. Máximo 5MB"
    
    try:
        Image.open(image_file)
        return True, "Imagen válida"
    except:
        return False, "Archivo no es una imagen válida"


def mint_nft(image_file, title, artist):
    print("Received image in mintnft:", image_file)

    with tempfile.NamedTemporaryFile(delete=False, suffix='.webp') as tmp_file:
        tmp_file.write(image_file.getvalue())
        tmp_path = tmp_file.name
        print("Temp file:", tmp_path)
        print("printed")

    try:
        metadata = {
            "title": title,
            "artist": artist
        }
        metadata_hash = upload_to_pinata(tmp_path, metadata)
        
        ipfs_uri = f"ipfs://{metadata_hash}"
        run_js_script('mint/mint.js', ipfs_uri)
        
        return True, "NFT minted successfully!"
    except Exception as e:
        return False, f"Error minting NFT: {str(e)}"
    finally:
        os.unlink(tmp_path)


def main():

    st.set_page_config(
    page_title="42 Students Leaderboard",
    page_icon="🚀",
    layout="centered"
    )

    st.title("NFT Minting App")

    tab1, tab2 = st.tabs(["Mint", "Collection"])
    
    with tab1:
        st.header("Create your NFT")
        
        title = st.text_input("Title")
        artist = st.text_input("Artist")
        
        col1, col2 = st.columns(2)
        
        uploaded_image = None
        generated_image = None
        
        with col1:
            st.subheader("Upload Image")
            uploaded_file = st.file_uploader("Choose an image", type=['png', 'jpg', 'jpeg', 'webp'])
            print(type(uploaded_file))
            if uploaded_file:
                valid, msg = check_image(uploaded_file)
                if valid:
                    st.image(uploaded_file)
                    uploaded_image = uploaded_file
                else:
                    st.error(msg)
                
            print("Uploaded image:", uploaded_image)
        
        with col2:
            st.subheader("Generate Image")
            prompt = st.text_input("Enter your prompt for image generation")
            
            if st.button("Generate"):
                if not prompt:
                    st.error("Please enter a prompt")
                    return None

                from generative import generate_image
                with st.spinner('Generating image...'):
                    gen_img_path = generate_image(prompt)
                    if gen_img_path:
                        st.image(gen_img_path)
                        with open(gen_img_path, 'rb') as f:
                            generated_image = f.read()
                    else:
                        st.error("Sorry. Free quota exceeded. Please upload an image.")
            
            print("Generated image:", generated_image)



        if st.button("Mint NFT"):
            print("Bool uploaded", bool(uploaded_image))
            print("Bool generated", bool(generated_image))
            if not title or not artist:
                st.error("Please fill in title and artist")
            elif not (bool(uploaded_image) != bool(generated_image)):
                st.error("Please upload or generate an image")
            else:
                with st.spinner('Minting NFT...'):
                    image_to_use = uploaded_image if uploaded_image else generated_image

                    success, msg = mint_nft(image_to_use, title, artist)
                    if success:
                        st.success(msg)
                    else:
                        st.error(msg)
    
    with tab2:
        st.header("Minted NFTs Showcase")
        
        if st.button("Get Collection"):
            with st.spinner('Calling blockchain...'):
                nfts = get_nft_collection()
                
                if not nfts:
                    st.warning("No valid NFTs found in the collection")
                else:
                    # Mostrar en rejilla (3 columnas)
                    cols = st.columns(3)
                    for idx, nft in enumerate(nfts):
                        with cols[idx % 3]:
                            st.image(nft['image_url'])
                            st.write(f"**{nft['title']}**")
                            st.write(f"*By: {nft['artist']}*")


if __name__ == "__main__":
    main()
