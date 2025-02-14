const { ethers } = require("hardhat");

async function main() {
    const [deployer] = await ethers.getSigners();
    console.log("Deploying contract with account:", deployer.address);

    const NFT42 = await ethers.getContractFactory("NFT42");
    const nft = await NFT42.deploy();
    await nft.deployed();

    console.log("NFT42 contract deployed at:", nft.address);
}

main()
    .then(() => process.exit(0))
    .catch((error) => {
        console.error(error);
        process.exit(1);
    });