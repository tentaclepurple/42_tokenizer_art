require('@nomiclabs/hardhat-waffle');
require('@nomiclabs/hardhat-ethers');
require('dotenv').config();

const PRIVATE_KEY = process.env.PRIVATE_KEY;

module.exports = {
  solidity: "0.8.20",
  networks: {
    amoy: {
      url: "https://rpc-amoy.polygon.technology/",
      accounts: [`0x${PRIVATE_KEY}`]
    }
  },
  paths: {
    sources: "./code",
    tests: "./test",
    cache: "./cache",
    artifacts: "./artifacts"
  }
};