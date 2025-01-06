// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract RandomNumber {
    // Function to generate a pseudo-random number
    function getRandomNumber() public view returns (uint256) {
        // Using block.timestamp and blockhash as the randomness source
        return
            uint256(
                keccak256(
                    abi.encodePacked(
                        block.timestamp,
                        blockhash(block.number - 1),
                        msg.sender
                    )
                )
            );
    }
}
