require('dotenv').config();
const { ethers } = require("hardhat");

async function main() {
    const NFT42 = await ethers.getContractFactory("NFT42");
    const nft = await NFT42.attach(process.env.CONTRACT_ADDRESS);

    const uris = await nft.getTokenURIs();
    console.log("Token URIs:", uris);
}

main()
    .then(() => process.exit(0))
    .catch(error => {
        console.error(error);
        process.exit(1);
    });