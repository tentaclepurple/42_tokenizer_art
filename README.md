# TokenizerArt42 - Achievement NFTs

## Overview
TokenizerArt42 is an NFT platform designed to recognize and commemorate 42 students' academic achievements through unique digital badges. Built on Polygon Network, it allows staff to mint NFTs that represent significant academic milestones.

## Technical Stack
- **Blockchain**: Polygon (MATIC) - Chosen for its low transaction costs and Ethereum compatibility
- **Token Standard**: ERC721 - Industry standard for non-fungible tokens
- **Storage**: IPFS via Pinata - Decentralized storage for NFT images and metadata
- **Frontend**: Streamlit - Simple and powerful UI for minting and viewing NFTs
- **Smart Contract**: Solidity 0.8.20 - Latest stable version with security features

## Project Structure

/
├── app/                    # Streamlit application
├── code/                   # Smart contracts
├── deployment/             # Deployment scripts
├── documentation/          # Detailed documentation
├── mint/                   # Minting scripts
└── README.md


## Setup and Installation
1. Clone the repository
2. Create .env file with required keys:
   - PRIVATE_KEY
   - CONTRACT_ADDRESS
   - PINATA_API_KEY
   - PINATA_SECRET
3. Build Containers
    Make
4. Interact with contract
    Make exec
    Make compile
    Make deploy
5. Launch app
    streamlit run app/app.py

Features

NFT minting with image upload or AI generation
Metadata storage on IPFS
Collection viewer
Integration with Polygon blockchain



TOKEN_URI=ipfs://bafybeiecl7myvuveviqzi3lrpy2r3i5ijkdhkunimyc6gyzrrcck7c375m npx hardhat run mint/mint.js --network amoy



https://huggingface.co/spaces/KingNish/Realtime-FLUX
https://huggingface.co/spaces/stabilityai/stable-diffusion-3.5-large