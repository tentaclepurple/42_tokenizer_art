import streamlit as st
from PIL import Image
import os
from pinata import upload_to_pinata, get_pinata_content
from interact import run_js_script
import tempfile


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
    # Guardar temporalmente el archivo subido
    with tempfile.NamedTemporaryFile(delete=False, suffix='.webp') as tmp_file:
        tmp_file.write(image_file.getvalue())
        tmp_path = tmp_file.name

    try:
        # Subir a IPFS con metadata
        metadata = {
            "title": title,
            "artist": artist
        }
        metadata_hash = upload_to_pinata(tmp_path, metadata)
        
        # Mint en blockchain
        ipfs_uri = f"ipfs://{metadata_hash}"
        run_js_script('mint/mint.js', ipfs_uri)
        
        return True, "NFT minted successfully!"
    except Exception as e:
        return False, f"Error minting NFT: {str(e)}"
    finally:
        os.unlink(tmp_path)  # Limpiar archivo temporal


def main():
    st.title("NFT42 Collection")
    
    tab1, tab2 = st.tabs(["Mint NFT", "Collection"])
    
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
            
            if uploaded_file:
                valid, msg = check_image(uploaded_file)
                if valid:
                    st.image(uploaded_file)
                    uploaded_image = uploaded_file
                else:
                    st.error(msg)
        
        with col2:
            st.subheader("Generate Image")
            if st.button("Generate"):
                st.write("Coming soon...")
        
        if st.button("Mint NFT"):
            if not title or not artist:
                st.error("Please fill in title and artist")
            elif not uploaded_image:
                st.error("Please upload or generate an image")
            else:
                with st.spinner('Minting NFT...'):
                    success, msg = mint_nft(uploaded_image, title, artist)
                    if success:
                        st.success(msg)
                    else:
                        st.error(msg)
    
    with tab2:
        st.header("Collection")


if __name__ == "__main__":
    main()
