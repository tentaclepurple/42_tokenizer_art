// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract NFT42 is ERC721, Ownable {
    string private _baseTokenURI;
    uint256 private _tokenIdCounter;

    constructor(string memory baseURI) ERC721("NFT42", "NFT42") Ownable() {
        _baseTokenURI = baseURI;
    }

    function mint() public onlyOwner {
        uint256 tokenId = _tokenIdCounter;
        _safeMint(msg.sender, tokenId);
        _tokenIdCounter++;
    }

    function _baseURI() internal view override returns (string memory) {
        return _baseTokenURI;
    }

    function setBaseURI(string memory baseURI) public onlyOwner {
        _baseTokenURI = baseURI;
    }

    function getCurrentTokenId() public view returns (uint256) {
        return _tokenIdCounter;
    }
}