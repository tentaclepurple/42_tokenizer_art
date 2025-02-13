const { ethers } = require("hardhat");

async function main() {

    const baseURI = "ipfs://bafybeiecl7myvuveviqzi3lrpy2r3i5ijkdhkunimyc6gyzrrcck7c375m/";
    const abiCoder = new ethers.utils.AbiCoder();
    const encodedParameters = abiCoder.encode(["string"], [baseURI]);
    console.log("Constructor Arguments:", encodedParameters);
}

main();