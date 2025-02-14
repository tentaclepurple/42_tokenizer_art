import streamlit as st
from PIL import Image
import os
from pinata import upload_to_pinata, get_pinata_content
from interact import run_js_script
import tempfile
import requests
import dotenv


from dotenv import load_dotenv

load_dotenv()  

CONTRACT_ADDRESS = os.getenv('CONTRACT_ADDRESS')


def validate_input(title, artist):
    if len(title) < 3 or len(title) > 50:
        return False, "Title must be between 3 and 50 characters"
    if len(artist) < 3 or len(artist) > 30:
        return False, "Artist name must be between 3 and 30 characters"
    return True, ""


def get_nft_collection():
    result = run_js_script('deployment/getTokenURIs.js')
    
    import json
    try:

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


def mint_nft(path, title, artist):

    try:
        metadata = {
            "title": title,
            "artist": artist
        }
        metadata_hash = upload_to_pinata(path, metadata)
        
        ipfs_uri = f"ipfs://{metadata_hash}"
        run_js_script('mint/mint.js', ipfs_uri)
        
        return True, "NFT minted successfully!"
    except Exception as e:
        return False, f"Error minting NFT: {str(e)}"
    finally:
        os.unlink(path)


def main():

    st.set_page_config(
    page_title="Tokenizer Art 52",
    page_icon="🚀",
    layout="centered"
    )

    st.title("TOKENIZER ART 42")
    st.write("Powered by Polygon")

    tab1, tab2 = st.tabs(["Mint", "Collection"])

    if 'gen_img_path' not in st.session_state:
        st.session_state.gen_img_path = None

    if 'minting' not in st.session_state:
        st.session_state.minting = False
    
    with tab1:
        st.header("Create your NFT")

        st.write("")
        
        title = st.text_input("Title")
        artist = st.text_input("Artist")
        
        st.write("")
        st.write("")
        
        col1, col2 = st.columns(2)
        
        tmp_path = None
        gen_img_path = None
        
        with col1:
            st.subheader("Upload Image")
            uploaded_file = st.file_uploader("Choose an image", type=['png', 'jpg', 'jpeg', 'webp'])
            if uploaded_file:
                valid, msg = check_image(uploaded_file)
                if valid:
                    st.image(uploaded_file)
                    uploaded_file = uploaded_file
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.webp') as tmp_file:
                        tmp_file.write(uploaded_file.getvalue())
                        tmp_path = tmp_file.name
                        
                else:
                    st.error(msg)

        
        with col2:
            st.subheader("Generate Image")
            prompt = st.text_input("Enter your prompt for image generation")
            col2_buttons = st.columns([1, 1])
            
            with col2_buttons[0]:
                if 'generating' not in st.session_state:
                    st.session_state.generating = False
                    
                if st.button("Generate", disabled=st.session_state.generating):
                    if not prompt:
                        st.error("Please enter a prompt")
                    else:
                        st.session_state.generating = True
                        from generative import generate_image
                        with st.spinner('Generating image...'):
                            st.session_state.gen_img_path = generate_image(prompt)
                            if st.session_state.gen_img_path:
                                st.image(st.session_state.gen_img_path)
                            else:
                                st.error("Sorry. Free quota exceeded. Please upload an image.")
                        st.session_state.generating = False
                    
            with col2_buttons[1]:
                if st.button("Clear"):
                    st.session_state.gen_img_path = None
                    st.rerun()
        
        st.write("")
        st.write("")
        st.write("")

        if 'minting' not in st.session_state:
            st.session_state.minting = False

        if st.button("Mint NFT", disabled=st.session_state.minting, use_container_width=True):
            valid, msg = validate_input(title, artist)
            if not valid:
                st.error(msg)
            elif not (bool(tmp_path) != bool(st.session_state.gen_img_path)):
                st.error("Please upload or generate an image")
            else:
                st.session_state.minting = True
                with st.spinner('Minting NFT...'):
                    path = tmp_path if tmp_path else st.session_state.gen_img_path
                    success, msg = mint_nft(path, title, artist)
                    if success:
                        st.success(msg)
                    else:
                        st.error(msg)
                st.session_state.minting = False
    with tab2:
        st.header("Minted NFTs Showcase")

        explorer_url = f"https://amoy.polygonscan.com/address/{CONTRACT_ADDRESS}"

        st.markdown(f"[View Contract]({explorer_url}) 🔍")
        st.write("Powered by Polygon Amoy Block Explorer")
        st.write("")
        
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
