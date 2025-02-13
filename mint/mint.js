require('dotenv').config();
const { ethers } = require("hardhat");

async function main() {
    const [owner] = await ethers.getSigners();
    
    const NFT42 = await ethers.getContractFactory("NFT42");
    const nft = await NFT42.attach(process.env.CONTRACT_ADDRESS);

    console.log("Minting NFT...");
    const tx = await nft.mint();
    await tx.wait();
    
    console.log("NFT minted successfully");
}

main()
    .then(() => process.exit(0))
    .catch(error => {
        console.error(error);
        process.exit(1);
    });