// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract VulnerableContract {
    mapping(address => uint256) public balances;

    // Deposit Ether into the contract
    function deposit() external payable {
        balances[msg.sender] += msg.value;
    }

    // Withdraw Ether from the contract
    function withdraw(uint256 _amount) external {
        require(balances[msg.sender] >= _amount, "Insufficient balance");

        // Send Ether to the user (vulnerable point)
        (bool success, ) = msg.sender.call{value: _amount}("");
        require(success, "Transfer failed");

        // Update the balance (happens after the call)
        balances[msg.sender] -= _amount;
    }

    // Helper function to check contract's balance
    function getContractBalance() external view returns (uint256) {
        return address(this).balance;
    }
}
