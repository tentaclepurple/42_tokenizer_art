require('dotenv').config();
const { ethers } = require("hardhat");

async function main() {
    const NFT42 = await ethers.getContractFactory("NFT42");
    const nft = await NFT42.attach(process.env.CONTRACT_ADDRESS);
    
    const tokenId = await nft.getCurrentTokenId();
    console.log("Current Token ID:", tokenId.toString());
}

main();