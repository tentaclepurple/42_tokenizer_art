const { ethers } = require("hardhat");

async function main() {
    const [deployer] = await ethers.getSigners();
    console.log("Deploying contract with account:", deployer.address);

    // IPFS base URI where the metadata is stored
    const baseURI = "ipfs://bafybeiecl7myvuveviqzi3lrpy2r3i5ijkdhkunimyc6gyzrrcck7c375m/";

    const NFT42 = await ethers.getContractFactory("NFT42");
    const nft = await NFT42.deploy(baseURI);
    await nft.deployed();

    console.log("NFT42 contract:", nft.address);

    const mintTx = await nft.mint();
    await mintTx.wait();
    console.log("NFT minted successfully");
}

main()
    .then(() => process.exit(0))
    .catch((error) => {
        console.error(error);
        process.exit(1);
    });