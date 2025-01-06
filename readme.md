# ChainCheck

made by [Melis34](https://github.com/Melis34) @
[Melis IT Solutions](https://melisitsolutions.com/)
\
 Opensource prototype of a closed source automatic web3 vulnerabilty scanner for smart contract audits and bug bounties
## use
Start using:
\
`python3 main.py`
\
Automatically targets all files in testContracts folder, but this can be changed with use of options.

## options:

| flag                   | use                            |
| ---------------------- | ------------------------------ |
| -h, --help             | show help message and exit     |
| -file, -f              | Creates output txt file        |
| -dir, -directory DIR   | Set directory to be scanned    |
| -contract, -c CONTRACT | Set contract to be scanned     |
| -t, -terminal          | dont print results to terminal |

## Dependencies

Requires the solidity language:
https://docs.soliditylang.org/en/latest/installing-solidity.html#installing-solidity
