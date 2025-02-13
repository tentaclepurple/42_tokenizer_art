require('dotenv').config();
const { ethers } = require("hardhat");

async function main() {
    const [owner] = await ethers.getSigners();
    
    const NFT42 = await ethers.getContractFactory("NFT42");
    const nft = await NFT42.attach(process.env.CONTRACT_ADDRESS);

    // Obtener la URI de la variable de entorno
    const tokenURI = process.env.TOKEN_URI;
    if (!tokenURI) {
        console.error("Por favor, proporciona una URI de token.");
        process.exit(1);
    }

    // Minting a new NFT with the provided IPFS URI
    console.log(`Minting NFT...`);
    const mintTx = await nft.mint(tokenURI);
    await mintTx.wait();
    console.log(`NFT minted with URI: ${tokenURI}`);
}

main()
    .then(() => process.exit(0))
    .catch(error => {
        console.error(error);
        process.exit(1);
    });