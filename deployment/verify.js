require('dotenv').config();
const { ethers } = require("hardhat");

async function main() {
    const NFT42 = await ethers.getContractFactory("NFT42");
    const nft = await NFT42.attach(process.env.CONTRACT_ADDRESS);

    // Verify token from 0 to 4
    for(let i = 0; i < 5; i++) {
        try {
            const owner = await nft.ownerOf(i);
            console.log(`Token ${i} - Owner: ${owner}`);
        } catch(e) {
            console.log(`Token ${i} no existe`);
        }
    }
}

main();