// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

contract NFT42 is ERC721URIStorage, Ownable {
    uint256 private _tokenIdCounter;

    constructor() ERC721("NFT42", "NFT42") Ownable() {}

    function mint(string memory tokenURI) public onlyOwner {
        uint256 tokenId = _tokenIdCounter;
        _safeMint(msg.sender, tokenId);
        _setTokenURI(tokenId, tokenURI);
        _tokenIdCounter++;
    }

    function getCurrentTokenId() public view returns (uint256) {
        return _tokenIdCounter;
    }

    function getTokenURIs() public view returns (string[] memory) {
        string[] memory uris = new string[](_tokenIdCounter);
        for (uint256 i = 0; i < _tokenIdCounter; i++) {
            uris[i] = tokenURI(i);
        }
        return uris;
    }
}