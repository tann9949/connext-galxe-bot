connext_diamond_abi = [
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "bytes32",
                "name": "key",
                "type": "bytes32"
            },
            {
                "indexed": True,
                "internalType": "bytes32",
                "name": "canonicalId",
                "type": "bytes32"
            },
            {
                "indexed": True,
                "internalType": "uint32",
                "name": "domain",
                "type": "uint32"
            },
            {
                "indexed": False,
                "internalType": "address",
                "name": "adoptedAsset",
                "type": "address"
            },
            {
                "indexed": False,
                "internalType": "address",
                "name": "localAsset",
                "type": "address"
            },
            {
                "indexed": False,
                "internalType": "address",
                "name": "caller",
                "type": "address"
            }
        ],
        "name": "AssetAdded",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "bytes32",
                "name": "key",
                "type": "bytes32"
            },
            {
                "indexed": False,
                "internalType": "address",
                "name": "caller",
                "type": "address"
            }
        ],
        "name": "AssetRemoved",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "bytes32",
                "name": "key",
                "type": "bytes32"
            },
            {
                "indexed": True,
                "internalType": "bytes32",
                "name": "canonicalId",
                "type": "bytes32"
            },
            {
                "indexed": True,
                "internalType": "uint32",
                "name": "domain",
                "type": "uint32"
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "cap",
                "type": "uint256"
            },
            {
                "indexed": False,
                "internalType": "address",
                "name": "caller",
                "type": "address"
            }
        ],
        "name": "LiquidityCapUpdated",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "bytes32",
                "name": "key",
                "type": "bytes32"
            },
            {
                "indexed": True,
                "internalType": "bytes32",
                "name": "canonicalId",
                "type": "bytes32"
            },
            {
                "indexed": True,
                "internalType": "uint32",
                "name": "domain",
                "type": "uint32"
            },
            {
                "indexed": False,
                "internalType": "address",
                "name": "swapPool",
                "type": "address"
            },
            {
                "indexed": False,
                "internalType": "address",
                "name": "caller",
                "type": "address"
            }
        ],
        "name": "StableSwapAdded",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "uint32",
                "name": "domain",
                "type": "uint32"
            },
            {
                "indexed": True,
                "internalType": "bytes32",
                "name": "id",
                "type": "bytes32"
            },
            {
                "indexed": True,
                "internalType": "address",
                "name": "representation",
                "type": "address"
            }
        ],
        "name": "TokenDeployed",
        "type": "event"
    },
    {
        "inputs": [
            {
                "components": [
                    {
                        "internalType": "uint32",
                        "name": "domain",
                        "type": "uint32"
                    },
                    {
                        "internalType": "bytes32",
                        "name": "id",
                        "type": "bytes32"
                    }
                ],
                "internalType": "struct TokenId",
                "name": "_canonical",
                "type": "tuple"
            },
            {
                "internalType": "address",
                "name": "_stableSwapPool",
                "type": "address"
            }
        ],
        "name": "addStableSwapPool",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "_adopted",
                "type": "address"
            }
        ],
        "name": "adoptedToCanonical",
        "outputs": [
            {
                "components": [
                    {
                        "internalType": "uint32",
                        "name": "domain",
                        "type": "uint32"
                    },
                    {
                        "internalType": "bytes32",
                        "name": "id",
                        "type": "bytes32"
                    }
                ],
                "internalType": "struct TokenId",
                "name": "",
                "type": "tuple"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "components": [
                    {
                        "internalType": "uint32",
                        "name": "domain",
                        "type": "uint32"
                    },
                    {
                        "internalType": "bytes32",
                        "name": "id",
                        "type": "bytes32"
                    }
                ],
                "internalType": "struct TokenId",
                "name": "_canonical",
                "type": "tuple"
            }
        ],
        "name": "adoptedToLocalExternalPools",
        "outputs": [
            {
                "internalType": "contract IStableSwap",
                "name": "",
                "type": "address"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "bytes32",
                "name": "_key",
                "type": "bytes32"
            }
        ],
        "name": "adoptedToLocalExternalPools",
        "outputs": [
            {
                "internalType": "contract IStableSwap",
                "name": "",
                "type": "address"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "bytes32",
                "name": "_key",
                "type": "bytes32"
            }
        ],
        "name": "approvedAssets",
        "outputs": [
            {
                "internalType": "bool",
                "name": "",
                "type": "bool"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "components": [
                    {
                        "internalType": "uint32",
                        "name": "domain",
                        "type": "uint32"
                    },
                    {
                        "internalType": "bytes32",
                        "name": "id",
                        "type": "bytes32"
                    }
                ],
                "internalType": "struct TokenId",
                "name": "_canonical",
                "type": "tuple"
            }
        ],
        "name": "approvedAssets",
        "outputs": [
            {
                "internalType": "bool",
                "name": "",
                "type": "bool"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "bytes32",
                "name": "_key",
                "type": "bytes32"
            }
        ],
        "name": "canonicalToAdopted",
        "outputs": [
            {
                "internalType": "address",
                "name": "",
                "type": "address"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "components": [
                    {
                        "internalType": "uint32",
                        "name": "domain",
                        "type": "uint32"
                    },
                    {
                        "internalType": "bytes32",
                        "name": "id",
                        "type": "bytes32"
                    }
                ],
                "internalType": "struct TokenId",
                "name": "_canonical",
                "type": "tuple"
            }
        ],
        "name": "canonicalToAdopted",
        "outputs": [
            {
                "internalType": "address",
                "name": "",
                "type": "address"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "bytes32",
                "name": "_key",
                "type": "bytes32"
            }
        ],
        "name": "canonicalToRepresentation",
        "outputs": [
            {
                "internalType": "address",
                "name": "",
                "type": "address"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "components": [
                    {
                        "internalType": "uint32",
                        "name": "domain",
                        "type": "uint32"
                    },
                    {
                        "internalType": "bytes32",
                        "name": "id",
                        "type": "bytes32"
                    }
                ],
                "internalType": "struct TokenId",
                "name": "_canonical",
                "type": "tuple"
            }
        ],
        "name": "canonicalToRepresentation",
        "outputs": [
            {
                "internalType": "address",
                "name": "",
                "type": "address"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "bytes32",
                "name": "_key",
                "type": "bytes32"
            }
        ],
        "name": "getCustodiedAmount",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "bytes32",
                "name": "_id",
                "type": "bytes32"
            },
            {
                "internalType": "uint32",
                "name": "_domain",
                "type": "uint32"
            }
        ],
        "name": "getLocalAndAdoptedToken",
        "outputs": [
            {
                "internalType": "address",
                "name": "",
                "type": "address"
            },
            {
                "internalType": "address",
                "name": "",
                "type": "address"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "_candidate",
                "type": "address"
            }
        ],
        "name": "getTokenId",
        "outputs": [
            {
                "components": [
                    {
                        "internalType": "uint32",
                        "name": "domain",
                        "type": "uint32"
                    },
                    {
                        "internalType": "bytes32",
                        "name": "id",
                        "type": "bytes32"
                    }
                ],
                "internalType": "struct TokenId",
                "name": "",
                "type": "tuple"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "components": [
                    {
                        "internalType": "uint32",
                        "name": "domain",
                        "type": "uint32"
                    },
                    {
                        "internalType": "bytes32",
                        "name": "id",
                        "type": "bytes32"
                    }
                ],
                "internalType": "struct TokenId",
                "name": "_canonical",
                "type": "tuple"
            },
            {
                "internalType": "address",
                "name": "_adoptedAssetId",
                "type": "address"
            },
            {
                "internalType": "address",
                "name": "_representation",
                "type": "address"
            }
        ],
        "name": "removeAssetId",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "bytes32",
                "name": "_key",
                "type": "bytes32"
            },
            {
                "internalType": "address",
                "name": "_adoptedAssetId",
                "type": "address"
            },
            {
                "internalType": "address",
                "name": "_representation",
                "type": "address"
            }
        ],
        "name": "removeAssetId",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "_representation",
                "type": "address"
            }
        ],
        "name": "representationToCanonical",
        "outputs": [
            {
                "components": [
                    {
                        "internalType": "uint32",
                        "name": "domain",
                        "type": "uint32"
                    },
                    {
                        "internalType": "bytes32",
                        "name": "id",
                        "type": "bytes32"
                    }
                ],
                "internalType": "struct TokenId",
                "name": "",
                "type": "tuple"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "components": [
                    {
                        "internalType": "uint32",
                        "name": "domain",
                        "type": "uint32"
                    },
                    {
                        "internalType": "bytes32",
                        "name": "id",
                        "type": "bytes32"
                    }
                ],
                "internalType": "struct TokenId",
                "name": "_canonical",
                "type": "tuple"
            },
            {
                "internalType": "uint8",
                "name": "_canonicalDecimals",
                "type": "uint8"
            },
            {
                "internalType": "string",
                "name": "_representationName",
                "type": "string"
            },
            {
                "internalType": "string",
                "name": "_representationSymbol",
                "type": "string"
            },
            {
                "internalType": "address",
                "name": "_adoptedAssetId",
                "type": "address"
            },
            {
                "internalType": "address",
                "name": "_stableSwapPool",
                "type": "address"
            },
            {
                "internalType": "uint256",
                "name": "_cap",
                "type": "uint256"
            }
        ],
        "name": "setupAsset",
        "outputs": [
            {
                "internalType": "address",
                "name": "_local",
                "type": "address"
            }
        ],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "components": [
                    {
                        "internalType": "uint32",
                        "name": "domain",
                        "type": "uint32"
                    },
                    {
                        "internalType": "bytes32",
                        "name": "id",
                        "type": "bytes32"
                    }
                ],
                "internalType": "struct TokenId",
                "name": "_canonical",
                "type": "tuple"
            },
            {
                "internalType": "address",
                "name": "_representation",
                "type": "address"
            },
            {
                "internalType": "address",
                "name": "_adoptedAssetId",
                "type": "address"
            },
            {
                "internalType": "address",
                "name": "_stableSwapPool",
                "type": "address"
            }
        ],
        "name": "setupAssetWithDeployedRepresentation",
        "outputs": [
            {
                "internalType": "address",
                "name": "",
                "type": "address"
            }
        ],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "components": [
                    {
                        "internalType": "uint32",
                        "name": "domain",
                        "type": "uint32"
                    },
                    {
                        "internalType": "bytes32",
                        "name": "id",
                        "type": "bytes32"
                    }
                ],
                "internalType": "struct TokenId",
                "name": "_canonical",
                "type": "tuple"
            },
            {
                "internalType": "string",
                "name": "_name",
                "type": "string"
            },
            {
                "internalType": "string",
                "name": "_symbol",
                "type": "string"
            }
        ],
        "name": "updateDetails",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "components": [
                    {
                        "internalType": "uint32",
                        "name": "domain",
                        "type": "uint32"
                    },
                    {
                        "internalType": "bytes32",
                        "name": "id",
                        "type": "bytes32"
                    }
                ],
                "internalType": "struct TokenId",
                "name": "_canonical",
                "type": "tuple"
            },
            {
                "internalType": "uint256",
                "name": "_updated",
                "type": "uint256"
            }
        ],
        "name": "updateLiquidityCap",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "bytes32",
                "name": "transferId",
                "type": "bytes32"
            },
            {
                "indexed": True,
                "internalType": "address",
                "name": "router",
                "type": "address"
            },
            {
                "indexed": False,
                "internalType": "address",
                "name": "asset",
                "type": "address"
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "amount",
                "type": "uint256"
            }
        ],
        "name": "AavePortalMintUnbacked",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "bytes32",
                "name": "transferId",
                "type": "bytes32"
            },
            {
                "indexed": True,
                "internalType": "address",
                "name": "to",
                "type": "address"
            },
            {
                "indexed": True,
                "internalType": "address",
                "name": "asset",
                "type": "address"
            },
            {
                "components": [
                    {
                        "components": [
                            {
                                "internalType": "uint32",
                                "name": "originDomain",
                                "type": "uint32"
                            },
                            {
                                "internalType": "uint32",
                                "name": "destinationDomain",
                                "type": "uint32"
                            },
                            {
                                "internalType": "uint32",
                                "name": "canonicalDomain",
                                "type": "uint32"
                            },
                            {
                                "internalType": "address",
                                "name": "to",
                                "type": "address"
                            },
                            {
                                "internalType": "address",
                                "name": "delegate",
                                "type": "address"
                            },
                            {
                                "internalType": "bool",
                                "name": "receiveLocal",
                                "type": "bool"
                            },
                            {
                                "internalType": "bytes",
                                "name": "callData",
                                "type": "bytes"
                            },
                            {
                                "internalType": "uint256",
                                "name": "slippage",
                                "type": "uint256"
                            },
                            {
                                "internalType": "address",
                                "name": "originSender",
                                "type": "address"
                            },
                            {
                                "internalType": "uint256",
                                "name": "bridgedAmt",
                                "type": "uint256"
                            },
                            {
                                "internalType": "uint256",
                                "name": "normalizedIn",
                                "type": "uint256"
                            },
                            {
                                "internalType": "uint256",
                                "name": "nonce",
                                "type": "uint256"
                            },
                            {
                                "internalType": "bytes32",
                                "name": "canonicalId",
                                "type": "bytes32"
                            }
                        ],
                        "internalType": "struct TransferInfo",
                        "name": "params",
                        "type": "tuple"
                    },
                    {
                        "internalType": "address[]",
                        "name": "routers",
                        "type": "address[]"
                    },
                    {
                        "internalType": "bytes[]",
                        "name": "routerSignatures",
                        "type": "bytes[]"
                    },
                    {
                        "internalType": "address",
                        "name": "sequencer",
                        "type": "address"
                    },
                    {
                        "internalType": "bytes",
                        "name": "sequencerSignature",
                        "type": "bytes"
                    }
                ],
                "indexed": False,
                "internalType": "struct ExecuteArgs",
                "name": "args",
                "type": "tuple"
            },
            {
                "indexed": False,
                "internalType": "address",
                "name": "local",
                "type": "address"
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "amount",
                "type": "uint256"
            },
            {
                "indexed": False,
                "internalType": "address",
                "name": "caller",
                "type": "address"
            }
        ],
        "name": "Executed",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "bytes32",
                "name": "transferId",
                "type": "bytes32"
            },
            {
                "indexed": False,
                "internalType": "bool",
                "name": "success",
                "type": "bool"
            },
            {
                "indexed": False,
                "internalType": "bytes",
                "name": "returnData",
                "type": "bytes"
            }
        ],
        "name": "ExternalCalldataExecuted",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "bytes32",
                "name": "transferId",
                "type": "bytes32"
            }
        ],
        "name": "ForceReceiveLocal",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "uint32",
                "name": "domain",
                "type": "uint32"
            },
            {
                "indexed": False,
                "internalType": "address",
                "name": "remote",
                "type": "address"
            },
            {
                "indexed": False,
                "internalType": "address",
                "name": "caller",
                "type": "address"
            }
        ],
        "name": "RemoteAdded",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "address",
                "name": "sequencer",
                "type": "address"
            },
            {
                "indexed": False,
                "internalType": "address",
                "name": "caller",
                "type": "address"
            }
        ],
        "name": "SequencerAdded",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "address",
                "name": "sequencer",
                "type": "address"
            },
            {
                "indexed": False,
                "internalType": "address",
                "name": "caller",
                "type": "address"
            }
        ],
        "name": "SequencerRemoved",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "bytes32",
                "name": "transferId",
                "type": "bytes32"
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "slippage",
                "type": "uint256"
            }
        ],
        "name": "SlippageUpdated",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "bytes32",
                "name": "transferId",
                "type": "bytes32"
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "increase",
                "type": "uint256"
            },
            {
                "indexed": False,
                "internalType": "address",
                "name": "caller",
                "type": "address"
            }
        ],
        "name": "TransferRelayerFeesIncreased",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "address",
                "name": "updated",
                "type": "address"
            },
            {
                "indexed": False,
                "internalType": "address",
                "name": "caller",
                "type": "address"
            }
        ],
        "name": "XAppConnectionManagerSet",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "bytes32",
                "name": "transferId",
                "type": "bytes32"
            },
            {
                "indexed": True,
                "internalType": "uint256",
                "name": "nonce",
                "type": "uint256"
            },
            {
                "indexed": True,
                "internalType": "bytes32",
                "name": "messageHash",
                "type": "bytes32"
            },
            {
                "components": [
                    {
                        "internalType": "uint32",
                        "name": "originDomain",
                        "type": "uint32"
                    },
                    {
                        "internalType": "uint32",
                        "name": "destinationDomain",
                        "type": "uint32"
                    },
                    {
                        "internalType": "uint32",
                        "name": "canonicalDomain",
                        "type": "uint32"
                    },
                    {
                        "internalType": "address",
                        "name": "to",
                        "type": "address"
                    },
                    {
                        "internalType": "address",
                        "name": "delegate",
                        "type": "address"
                    },
                    {
                        "internalType": "bool",
                        "name": "receiveLocal",
                        "type": "bool"
                    },
                    {
                        "internalType": "bytes",
                        "name": "callData",
                        "type": "bytes"
                    },
                    {
                        "internalType": "uint256",
                        "name": "slippage",
                        "type": "uint256"
                    },
                    {
                        "internalType": "address",
                        "name": "originSender",
                        "type": "address"
                    },
                    {
                        "internalType": "uint256",
                        "name": "bridgedAmt",
                        "type": "uint256"
                    },
                    {
                        "internalType": "uint256",
                        "name": "normalizedIn",
                        "type": "uint256"
                    },
                    {
                        "internalType": "uint256",
                        "name": "nonce",
                        "type": "uint256"
                    },
                    {
                        "internalType": "bytes32",
                        "name": "canonicalId",
                        "type": "bytes32"
                    }
                ],
                "indexed": False,
                "internalType": "struct TransferInfo",
                "name": "params",
                "type": "tuple"
            },
            {
                "indexed": False,
                "internalType": "address",
                "name": "asset",
                "type": "address"
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "amount",
                "type": "uint256"
            },
            {
                "indexed": False,
                "internalType": "address",
                "name": "local",
                "type": "address"
            },
            {
                "indexed": False,
                "internalType": "bytes",
                "name": "messageBody",
                "type": "bytes"
            }
        ],
        "name": "XCalled",
        "type": "event"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "_sequencer",
                "type": "address"
            }
        ],
        "name": "addSequencer",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "_sequencer",
                "type": "address"
            }
        ],
        "name": "approvedSequencers",
        "outputs": [
            {
                "internalType": "bool",
                "name": "",
                "type": "bool"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "bytes32",
                "name": "_transferId",
                "type": "bytes32"
            }
        ],
        "name": "bumpTransfer",
        "outputs": [],
        "stateMutability": "payable",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "domain",
        "outputs": [
            {
                "internalType": "uint32",
                "name": "",
                "type": "uint32"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint32",
                "name": "_domain",
                "type": "uint32"
            },
            {
                "internalType": "bytes32",
                "name": "_router",
                "type": "bytes32"
            }
        ],
        "name": "enrollRemoteRouter",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "components": [
                    {
                        "components": [
                            {
                                "internalType": "uint32",
                                "name": "originDomain",
                                "type": "uint32"
                            },
                            {
                                "internalType": "uint32",
                                "name": "destinationDomain",
                                "type": "uint32"
                            },
                            {
                                "internalType": "uint32",
                                "name": "canonicalDomain",
                                "type": "uint32"
                            },
                            {
                                "internalType": "address",
                                "name": "to",
                                "type": "address"
                            },
                            {
                                "internalType": "address",
                                "name": "delegate",
                                "type": "address"
                            },
                            {
                                "internalType": "bool",
                                "name": "receiveLocal",
                                "type": "bool"
                            },
                            {
                                "internalType": "bytes",
                                "name": "callData",
                                "type": "bytes"
                            },
                            {
                                "internalType": "uint256",
                                "name": "slippage",
                                "type": "uint256"
                            },
                            {
                                "internalType": "address",
                                "name": "originSender",
                                "type": "address"
                            },
                            {
                                "internalType": "uint256",
                                "name": "bridgedAmt",
                                "type": "uint256"
                            },
                            {
                                "internalType": "uint256",
                                "name": "normalizedIn",
                                "type": "uint256"
                            },
                            {
                                "internalType": "uint256",
                                "name": "nonce",
                                "type": "uint256"
                            },
                            {
                                "internalType": "bytes32",
                                "name": "canonicalId",
                                "type": "bytes32"
                            }
                        ],
                        "internalType": "struct TransferInfo",
                        "name": "params",
                        "type": "tuple"
                    },
                    {
                        "internalType": "address[]",
                        "name": "routers",
                        "type": "address[]"
                    },
                    {
                        "internalType": "bytes[]",
                        "name": "routerSignatures",
                        "type": "bytes[]"
                    },
                    {
                        "internalType": "address",
                        "name": "sequencer",
                        "type": "address"
                    },
                    {
                        "internalType": "bytes",
                        "name": "sequencerSignature",
                        "type": "bytes"
                    }
                ],
                "internalType": "struct ExecuteArgs",
                "name": "_args",
                "type": "tuple"
            }
        ],
        "name": "execute",
        "outputs": [
            {
                "internalType": "bytes32",
                "name": "",
                "type": "bytes32"
            }
        ],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "components": [
                    {
                        "internalType": "uint32",
                        "name": "originDomain",
                        "type": "uint32"
                    },
                    {
                        "internalType": "uint32",
                        "name": "destinationDomain",
                        "type": "uint32"
                    },
                    {
                        "internalType": "uint32",
                        "name": "canonicalDomain",
                        "type": "uint32"
                    },
                    {
                        "internalType": "address",
                        "name": "to",
                        "type": "address"
                    },
                    {
                        "internalType": "address",
                        "name": "delegate",
                        "type": "address"
                    },
                    {
                        "internalType": "bool",
                        "name": "receiveLocal",
                        "type": "bool"
                    },
                    {
                        "internalType": "bytes",
                        "name": "callData",
                        "type": "bytes"
                    },
                    {
                        "internalType": "uint256",
                        "name": "slippage",
                        "type": "uint256"
                    },
                    {
                        "internalType": "address",
                        "name": "originSender",
                        "type": "address"
                    },
                    {
                        "internalType": "uint256",
                        "name": "bridgedAmt",
                        "type": "uint256"
                    },
                    {
                        "internalType": "uint256",
                        "name": "normalizedIn",
                        "type": "uint256"
                    },
                    {
                        "internalType": "uint256",
                        "name": "nonce",
                        "type": "uint256"
                    },
                    {
                        "internalType": "bytes32",
                        "name": "canonicalId",
                        "type": "bytes32"
                    }
                ],
                "internalType": "struct TransferInfo",
                "name": "_params",
                "type": "tuple"
            }
        ],
        "name": "forceReceiveLocal",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "components": [
                    {
                        "internalType": "uint32",
                        "name": "originDomain",
                        "type": "uint32"
                    },
                    {
                        "internalType": "uint32",
                        "name": "destinationDomain",
                        "type": "uint32"
                    },
                    {
                        "internalType": "uint32",
                        "name": "canonicalDomain",
                        "type": "uint32"
                    },
                    {
                        "internalType": "address",
                        "name": "to",
                        "type": "address"
                    },
                    {
                        "internalType": "address",
                        "name": "delegate",
                        "type": "address"
                    },
                    {
                        "internalType": "bool",
                        "name": "receiveLocal",
                        "type": "bool"
                    },
                    {
                        "internalType": "bytes",
                        "name": "callData",
                        "type": "bytes"
                    },
                    {
                        "internalType": "uint256",
                        "name": "slippage",
                        "type": "uint256"
                    },
                    {
                        "internalType": "address",
                        "name": "originSender",
                        "type": "address"
                    },
                    {
                        "internalType": "uint256",
                        "name": "bridgedAmt",
                        "type": "uint256"
                    },
                    {
                        "internalType": "uint256",
                        "name": "normalizedIn",
                        "type": "uint256"
                    },
                    {
                        "internalType": "uint256",
                        "name": "nonce",
                        "type": "uint256"
                    },
                    {
                        "internalType": "bytes32",
                        "name": "canonicalId",
                        "type": "bytes32"
                    }
                ],
                "internalType": "struct TransferInfo",
                "name": "_params",
                "type": "tuple"
            },
            {
                "internalType": "uint256",
                "name": "_slippage",
                "type": "uint256"
            }
        ],
        "name": "forceUpdateSlippage",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "nonce",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint32",
                "name": "_domain",
                "type": "uint32"
            }
        ],
        "name": "remote",
        "outputs": [
            {
                "internalType": "address",
                "name": "",
                "type": "address"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "_sequencer",
                "type": "address"
            }
        ],
        "name": "removeSequencer",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "bytes32",
                "name": "_transferId",
                "type": "bytes32"
            }
        ],
        "name": "routedTransfers",
        "outputs": [
            {
                "internalType": "address[]",
                "name": "",
                "type": "address[]"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "_xAppConnectionManager",
                "type": "address"
            }
        ],
        "name": "setXAppConnectionManager",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "bytes32",
                "name": "_transferId",
                "type": "bytes32"
            }
        ],
        "name": "transferStatus",
        "outputs": [
            {
                "internalType": "enum DestinationTransferStatus",
                "name": "",
                "type": "uint8"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "xAppConnectionManager",
        "outputs": [
            {
                "internalType": "address",
                "name": "",
                "type": "address"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint32",
                "name": "_destination",
                "type": "uint32"
            },
            {
                "internalType": "address",
                "name": "_to",
                "type": "address"
            },
            {
                "internalType": "address",
                "name": "_asset",
                "type": "address"
            },
            {
                "internalType": "address",
                "name": "_delegate",
                "type": "address"
            },
            {
                "internalType": "uint256",
                "name": "_amount",
                "type": "uint256"
            },
            {
                "internalType": "uint256",
                "name": "_slippage",
                "type": "uint256"
            },
            {
                "internalType": "bytes",
                "name": "_callData",
                "type": "bytes"
            }
        ],
        "name": "xcall",
        "outputs": [
            {
                "internalType": "bytes32",
                "name": "",
                "type": "bytes32"
            }
        ],
        "stateMutability": "payable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint32",
                "name": "_destination",
                "type": "uint32"
            },
            {
                "internalType": "address",
                "name": "_to",
                "type": "address"
            },
            {
                "internalType": "address",
                "name": "_asset",
                "type": "address"
            },
            {
                "internalType": "address",
                "name": "_delegate",
                "type": "address"
            },
            {
                "internalType": "uint256",
                "name": "_amount",
                "type": "uint256"
            },
            {
                "internalType": "uint256",
                "name": "_slippage",
                "type": "uint256"
            },
            {
                "internalType": "bytes",
                "name": "_callData",
                "type": "bytes"
            }
        ],
        "name": "xcallIntoLocal",
        "outputs": [
            {
                "internalType": "bytes32",
                "name": "",
                "type": "bytes32"
            }
        ],
        "stateMutability": "payable",
        "type": "function"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "uint64",
                "name": "originAndNonce",
                "type": "uint64"
            },
            {
                "indexed": True,
                "internalType": "address",
                "name": "token",
                "type": "address"
            },
            {
                "indexed": True,
                "internalType": "address",
                "name": "recipient",
                "type": "address"
            },
            {
                "indexed": False,
                "internalType": "address",
                "name": "liquidityProvider",
                "type": "address"
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "amount",
                "type": "uint256"
            }
        ],
        "name": "Receive",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "bytes32",
                "name": "transferId",
                "type": "bytes32"
            },
            {
                "indexed": True,
                "internalType": "uint32",
                "name": "originDomain",
                "type": "uint32"
            },
            {
                "indexed": True,
                "internalType": "address",
                "name": "local",
                "type": "address"
            },
            {
                "indexed": False,
                "internalType": "address[]",
                "name": "routers",
                "type": "address[]"
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "amount",
                "type": "uint256"
            },
            {
                "indexed": False,
                "internalType": "address",
                "name": "caller",
                "type": "address"
            }
        ],
        "name": "Reconciled",
        "type": "event"
    },
    {
        "inputs": [
            {
                "internalType": "uint32",
                "name": "_origin",
                "type": "uint32"
            },
            {
                "internalType": "uint32",
                "name": "_nonce",
                "type": "uint32"
            },
            {
                "internalType": "bytes32",
                "name": "_sender",
                "type": "bytes32"
            },
            {
                "internalType": "bytes",
                "name": "_message",
                "type": "bytes"
            }
        ],
        "name": "handle",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "address",
                "name": "admin",
                "type": "address"
            }
        ],
        "name": "AssignRoleAdmin",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "address",
                "name": "router",
                "type": "address"
            }
        ],
        "name": "AssignRoleRouter",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "address",
                "name": "watcher",
                "type": "address"
            }
        ],
        "name": "AssignRoleWatcher",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "address",
                "name": "proposedOwner",
                "type": "address"
            }
        ],
        "name": "OwnershipProposed",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "address",
                "name": "previousOwner",
                "type": "address"
            },
            {
                "indexed": True,
                "internalType": "address",
                "name": "newOwner",
                "type": "address"
            }
        ],
        "name": "OwnershipTransferred",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [],
        "name": "Paused",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "address",
                "name": "revokedAddress",
                "type": "address"
            },
            {
                "indexed": False,
                "internalType": "enum Role",
                "name": "revokedRole",
                "type": "uint8"
            }
        ],
        "name": "RevokeRole",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "timestamp",
                "type": "uint256"
            }
        ],
        "name": "RouterAllowlistRemovalProposed",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "bool",
                "name": "renounced",
                "type": "bool"
            }
        ],
        "name": "RouterAllowlistRemoved",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [],
        "name": "Unpaused",
        "type": "event"
    },
    {
        "inputs": [],
        "name": "acceptProposedOwner",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "_admin",
                "type": "address"
            }
        ],
        "name": "assignRoleAdmin",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "_router",
                "type": "address"
            }
        ],
        "name": "assignRoleRouterAdmin",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "_watcher",
                "type": "address"
            }
        ],
        "name": "assignRoleWatcher",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "delay",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "owner",
        "outputs": [
            {
                "internalType": "address",
                "name": "",
                "type": "address"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "pause",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "paused",
        "outputs": [
            {
                "internalType": "bool",
                "name": "",
                "type": "bool"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "newlyProposed",
                "type": "address"
            }
        ],
        "name": "proposeNewOwner",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "proposeRouterAllowlistRemoval",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "proposed",
        "outputs": [
            {
                "internalType": "address",
                "name": "",
                "type": "address"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "proposedTimestamp",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "_role",
                "type": "address"
            }
        ],
        "name": "queryRole",
        "outputs": [
            {
                "internalType": "enum Role",
                "name": "",
                "type": "uint8"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "removeRouterAllowlist",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "_revoke",
                "type": "address"
            }
        ],
        "name": "revokeRole",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "routerAllowlistRemoved",
        "outputs": [
            {
                "internalType": "bool",
                "name": "",
                "type": "bool"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "routerAllowlistTimestamp",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "unpause",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "address",
                "name": "updated",
                "type": "address"
            },
            {
                "indexed": False,
                "internalType": "address",
                "name": "caller",
                "type": "address"
            }
        ],
        "name": "AavePoolUpdated",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "updated",
                "type": "uint256"
            },
            {
                "indexed": False,
                "internalType": "address",
                "name": "caller",
                "type": "address"
            }
        ],
        "name": "AavePortalFeeUpdated",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "bytes32",
                "name": "transferId",
                "type": "bytes32"
            },
            {
                "indexed": False,
                "internalType": "address",
                "name": "asset",
                "type": "address"
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "amount",
                "type": "uint256"
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "fee",
                "type": "uint256"
            },
            {
                "indexed": False,
                "internalType": "address",
                "name": "caller",
                "type": "address"
            }
        ],
        "name": "AavePortalRepayment",
        "type": "event"
    },
    {
        "inputs": [],
        "name": "aavePool",
        "outputs": [
            {
                "internalType": "address",
                "name": "",
                "type": "address"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "aavePortalFee",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "bytes32",
                "name": "_transferId",
                "type": "bytes32"
            }
        ],
        "name": "getAavePortalDebt",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "bytes32",
                "name": "_transferId",
                "type": "bytes32"
            }
        ],
        "name": "getAavePortalFeeDebt",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "components": [
                    {
                        "internalType": "uint32",
                        "name": "originDomain",
                        "type": "uint32"
                    },
                    {
                        "internalType": "uint32",
                        "name": "destinationDomain",
                        "type": "uint32"
                    },
                    {
                        "internalType": "uint32",
                        "name": "canonicalDomain",
                        "type": "uint32"
                    },
                    {
                        "internalType": "address",
                        "name": "to",
                        "type": "address"
                    },
                    {
                        "internalType": "address",
                        "name": "delegate",
                        "type": "address"
                    },
                    {
                        "internalType": "bool",
                        "name": "receiveLocal",
                        "type": "bool"
                    },
                    {
                        "internalType": "bytes",
                        "name": "callData",
                        "type": "bytes"
                    },
                    {
                        "internalType": "uint256",
                        "name": "slippage",
                        "type": "uint256"
                    },
                    {
                        "internalType": "address",
                        "name": "originSender",
                        "type": "address"
                    },
                    {
                        "internalType": "uint256",
                        "name": "bridgedAmt",
                        "type": "uint256"
                    },
                    {
                        "internalType": "uint256",
                        "name": "normalizedIn",
                        "type": "uint256"
                    },
                    {
                        "internalType": "uint256",
                        "name": "nonce",
                        "type": "uint256"
                    },
                    {
                        "internalType": "bytes32",
                        "name": "canonicalId",
                        "type": "bytes32"
                    }
                ],
                "internalType": "struct TransferInfo",
                "name": "_params",
                "type": "tuple"
            },
            {
                "internalType": "uint256",
                "name": "_backingAmount",
                "type": "uint256"
            },
            {
                "internalType": "uint256",
                "name": "_feeAmount",
                "type": "uint256"
            },
            {
                "internalType": "uint256",
                "name": "_maxIn",
                "type": "uint256"
            }
        ],
        "name": "repayAavePortal",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "components": [
                    {
                        "internalType": "uint32",
                        "name": "originDomain",
                        "type": "uint32"
                    },
                    {
                        "internalType": "uint32",
                        "name": "destinationDomain",
                        "type": "uint32"
                    },
                    {
                        "internalType": "uint32",
                        "name": "canonicalDomain",
                        "type": "uint32"
                    },
                    {
                        "internalType": "address",
                        "name": "to",
                        "type": "address"
                    },
                    {
                        "internalType": "address",
                        "name": "delegate",
                        "type": "address"
                    },
                    {
                        "internalType": "bool",
                        "name": "receiveLocal",
                        "type": "bool"
                    },
                    {
                        "internalType": "bytes",
                        "name": "callData",
                        "type": "bytes"
                    },
                    {
                        "internalType": "uint256",
                        "name": "slippage",
                        "type": "uint256"
                    },
                    {
                        "internalType": "address",
                        "name": "originSender",
                        "type": "address"
                    },
                    {
                        "internalType": "uint256",
                        "name": "bridgedAmt",
                        "type": "uint256"
                    },
                    {
                        "internalType": "uint256",
                        "name": "normalizedIn",
                        "type": "uint256"
                    },
                    {
                        "internalType": "uint256",
                        "name": "nonce",
                        "type": "uint256"
                    },
                    {
                        "internalType": "bytes32",
                        "name": "canonicalId",
                        "type": "bytes32"
                    }
                ],
                "internalType": "struct TransferInfo",
                "name": "_params",
                "type": "tuple"
            },
            {
                "internalType": "address",
                "name": "_portalAsset",
                "type": "address"
            },
            {
                "internalType": "uint256",
                "name": "_backingAmount",
                "type": "uint256"
            },
            {
                "internalType": "uint256",
                "name": "_feeAmount",
                "type": "uint256"
            }
        ],
        "name": "repayAavePortalFor",
        "outputs": [],
        "stateMutability": "payable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "_aavePool",
                "type": "address"
            }
        ],
        "name": "setAavePool",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "_aavePortalFeeNumerator",
                "type": "uint256"
            }
        ],
        "name": "setAavePortalFee",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "address",
                "name": "relayer",
                "type": "address"
            },
            {
                "indexed": False,
                "internalType": "address",
                "name": "caller",
                "type": "address"
            }
        ],
        "name": "RelayerAdded",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "address",
                "name": "oldVault",
                "type": "address"
            },
            {
                "indexed": False,
                "internalType": "address",
                "name": "newVault",
                "type": "address"
            },
            {
                "indexed": False,
                "internalType": "address",
                "name": "caller",
                "type": "address"
            }
        ],
        "name": "RelayerFeeVaultUpdated",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "address",
                "name": "relayer",
                "type": "address"
            },
            {
                "indexed": False,
                "internalType": "address",
                "name": "caller",
                "type": "address"
            }
        ],
        "name": "RelayerRemoved",
        "type": "event"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "_relayer",
                "type": "address"
            }
        ],
        "name": "addRelayer",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "_relayer",
                "type": "address"
            }
        ],
        "name": "approvedRelayers",
        "outputs": [
            {
                "internalType": "bool",
                "name": "",
                "type": "bool"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "relayerFeeVault",
        "outputs": [
            {
                "internalType": "address",
                "name": "",
                "type": "address"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "_relayer",
                "type": "address"
            }
        ],
        "name": "removeRelayer",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "_relayerFeeVault",
                "type": "address"
            }
        ],
        "name": "setRelayerFeeVault",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "liquidityFeeNumerator",
                "type": "uint256"
            },
            {
                "indexed": False,
                "internalType": "address",
                "name": "caller",
                "type": "address"
            }
        ],
        "name": "LiquidityFeeNumeratorUpdated",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "maxRoutersPerTransfer",
                "type": "uint256"
            },
            {
                "indexed": False,
                "internalType": "address",
                "name": "caller",
                "type": "address"
            }
        ],
        "name": "MaxRoutersPerTransferUpdated",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "address",
                "name": "router",
                "type": "address"
            },
            {
                "indexed": False,
                "internalType": "address",
                "name": "caller",
                "type": "address"
            }
        ],
        "name": "RouterAdded",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "address",
                "name": "router",
                "type": "address"
            },
            {
                "indexed": False,
                "internalType": "address",
                "name": "caller",
                "type": "address"
            }
        ],
        "name": "RouterApprovedForPortal",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "address",
                "name": "router",
                "type": "address"
            }
        ],
        "name": "RouterInitialized",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "address",
                "name": "router",
                "type": "address"
            },
            {
                "indexed": False,
                "internalType": "address",
                "name": "local",
                "type": "address"
            },
            {
                "indexed": False,
                "internalType": "bytes32",
                "name": "key",
                "type": "bytes32"
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "amount",
                "type": "uint256"
            },
            {
                "indexed": False,
                "internalType": "address",
                "name": "caller",
                "type": "address"
            }
        ],
        "name": "RouterLiquidityAdded",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "address",
                "name": "router",
                "type": "address"
            },
            {
                "indexed": False,
                "internalType": "address",
                "name": "to",
                "type": "address"
            },
            {
                "indexed": False,
                "internalType": "address",
                "name": "local",
                "type": "address"
            },
            {
                "indexed": False,
                "internalType": "bytes32",
                "name": "key",
                "type": "bytes32"
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "amount",
                "type": "uint256"
            },
            {
                "indexed": False,
                "internalType": "address",
                "name": "caller",
                "type": "address"
            }
        ],
        "name": "RouterLiquidityRemoved",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "address",
                "name": "router",
                "type": "address"
            },
            {
                "indexed": True,
                "internalType": "address",
                "name": "prevOwner",
                "type": "address"
            },
            {
                "indexed": True,
                "internalType": "address",
                "name": "newOwner",
                "type": "address"
            }
        ],
        "name": "RouterOwnerAccepted",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "address",
                "name": "router",
                "type": "address"
            },
            {
                "indexed": True,
                "internalType": "address",
                "name": "prevProposed",
                "type": "address"
            },
            {
                "indexed": True,
                "internalType": "address",
                "name": "newProposed",
                "type": "address"
            }
        ],
        "name": "RouterOwnerProposed",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "address",
                "name": "router",
                "type": "address"
            },
            {
                "indexed": True,
                "internalType": "address",
                "name": "prevRecipient",
                "type": "address"
            },
            {
                "indexed": True,
                "internalType": "address",
                "name": "newRecipient",
                "type": "address"
            }
        ],
        "name": "RouterRecipientSet",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "address",
                "name": "router",
                "type": "address"
            },
            {
                "indexed": False,
                "internalType": "address",
                "name": "caller",
                "type": "address"
            }
        ],
        "name": "RouterRemoved",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "address",
                "name": "router",
                "type": "address"
            },
            {
                "indexed": False,
                "internalType": "address",
                "name": "caller",
                "type": "address"
            }
        ],
        "name": "RouterUnapprovedForPortal",
        "type": "event"
    },
    {
        "inputs": [],
        "name": "LIQUIDITY_FEE_DENOMINATOR",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "pure",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "LIQUIDITY_FEE_NUMERATOR",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "_router",
                "type": "address"
            }
        ],
        "name": "acceptProposedRouterOwner",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "_amount",
                "type": "uint256"
            },
            {
                "internalType": "address",
                "name": "_local",
                "type": "address"
            }
        ],
        "name": "addRouterLiquidity",
        "outputs": [],
        "stateMutability": "payable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "_amount",
                "type": "uint256"
            },
            {
                "internalType": "address",
                "name": "_local",
                "type": "address"
            },
            {
                "internalType": "address",
                "name": "_router",
                "type": "address"
            }
        ],
        "name": "addRouterLiquidityFor",
        "outputs": [],
        "stateMutability": "payable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "_router",
                "type": "address"
            }
        ],
        "name": "approveRouter",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "_router",
                "type": "address"
            }
        ],
        "name": "approveRouterForPortal",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "_router",
                "type": "address"
            }
        ],
        "name": "getProposedRouterOwner",
        "outputs": [
            {
                "internalType": "address",
                "name": "",
                "type": "address"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "_router",
                "type": "address"
            }
        ],
        "name": "getProposedRouterOwnerTimestamp",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "_router",
                "type": "address"
            }
        ],
        "name": "getRouterApproval",
        "outputs": [
            {
                "internalType": "bool",
                "name": "",
                "type": "bool"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "_router",
                "type": "address"
            }
        ],
        "name": "getRouterApprovalForPortal",
        "outputs": [
            {
                "internalType": "bool",
                "name": "",
                "type": "bool"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "_router",
                "type": "address"
            }
        ],
        "name": "getRouterOwner",
        "outputs": [
            {
                "internalType": "address",
                "name": "",
                "type": "address"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "_router",
                "type": "address"
            }
        ],
        "name": "getRouterRecipient",
        "outputs": [
            {
                "internalType": "address",
                "name": "",
                "type": "address"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "_owner",
                "type": "address"
            },
            {
                "internalType": "address",
                "name": "_recipient",
                "type": "address"
            }
        ],
        "name": "initializeRouter",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "maxRoutersPerTransfer",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "_router",
                "type": "address"
            },
            {
                "internalType": "address",
                "name": "_proposed",
                "type": "address"
            }
        ],
        "name": "proposeRouterOwner",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "components": [
                    {
                        "internalType": "uint32",
                        "name": "domain",
                        "type": "uint32"
                    },
                    {
                        "internalType": "bytes32",
                        "name": "id",
                        "type": "bytes32"
                    }
                ],
                "internalType": "struct TokenId",
                "name": "_canonical",
                "type": "tuple"
            },
            {
                "internalType": "uint256",
                "name": "_amount",
                "type": "uint256"
            },
            {
                "internalType": "address payable",
                "name": "_to",
                "type": "address"
            }
        ],
        "name": "removeRouterLiquidity",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "components": [
                    {
                        "internalType": "uint32",
                        "name": "domain",
                        "type": "uint32"
                    },
                    {
                        "internalType": "bytes32",
                        "name": "id",
                        "type": "bytes32"
                    }
                ],
                "internalType": "struct TokenId",
                "name": "_canonical",
                "type": "tuple"
            },
            {
                "internalType": "uint256",
                "name": "_amount",
                "type": "uint256"
            },
            {
                "internalType": "address payable",
                "name": "_to",
                "type": "address"
            },
            {
                "internalType": "address",
                "name": "_router",
                "type": "address"
            }
        ],
        "name": "removeRouterLiquidityFor",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "_router",
                "type": "address"
            },
            {
                "internalType": "address",
                "name": "_asset",
                "type": "address"
            }
        ],
        "name": "routerBalances",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "_numerator",
                "type": "uint256"
            }
        ],
        "name": "setLiquidityFeeNumerator",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint256",
                "name": "_newMaxRouters",
                "type": "uint256"
            }
        ],
        "name": "setMaxRoutersPerTransfer",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "_router",
                "type": "address"
            },
            {
                "internalType": "address",
                "name": "_recipient",
                "type": "address"
            }
        ],
        "name": "setRouterRecipient",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "_router",
                "type": "address"
            }
        ],
        "name": "unapproveRouter",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "_router",
                "type": "address"
            }
        ],
        "name": "unapproveRouterForPortal",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "bytes32",
                "name": "key",
                "type": "bytes32"
            },
            {
                "indexed": True,
                "internalType": "address",
                "name": "provider",
                "type": "address"
            },
            {
                "indexed": False,
                "internalType": "uint256[]",
                "name": "tokenAmounts",
                "type": "uint256[]"
            },
            {
                "indexed": False,
                "internalType": "uint256[]",
                "name": "fees",
                "type": "uint256[]"
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "invariant",
                "type": "uint256"
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "lpTokenSupply",
                "type": "uint256"
            }
        ],
        "name": "AddLiquidity",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "bytes32",
                "name": "key",
                "type": "bytes32"
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "newAdminFee",
                "type": "uint256"
            }
        ],
        "name": "NewAdminFee",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "bytes32",
                "name": "key",
                "type": "bytes32"
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "newSwapFee",
                "type": "uint256"
            }
        ],
        "name": "NewSwapFee",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "bytes32",
                "name": "key",
                "type": "bytes32"
            },
            {
                "indexed": True,
                "internalType": "address",
                "name": "provider",
                "type": "address"
            },
            {
                "indexed": False,
                "internalType": "uint256[]",
                "name": "tokenAmounts",
                "type": "uint256[]"
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "lpTokenSupply",
                "type": "uint256"
            }
        ],
        "name": "RemoveLiquidity",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "bytes32",
                "name": "key",
                "type": "bytes32"
            },
            {
                "indexed": True,
                "internalType": "address",
                "name": "provider",
                "type": "address"
            },
            {
                "indexed": False,
                "internalType": "uint256[]",
                "name": "tokenAmounts",
                "type": "uint256[]"
            },
            {
                "indexed": False,
                "internalType": "uint256[]",
                "name": "fees",
                "type": "uint256[]"
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "invariant",
                "type": "uint256"
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "lpTokenSupply",
                "type": "uint256"
            }
        ],
        "name": "RemoveLiquidityImbalance",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "bytes32",
                "name": "key",
                "type": "bytes32"
            },
            {
                "indexed": True,
                "internalType": "address",
                "name": "provider",
                "type": "address"
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "lpTokenAmount",
                "type": "uint256"
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "lpTokenSupply",
                "type": "uint256"
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "boughtId",
                "type": "uint256"
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "tokensBought",
                "type": "uint256"
            }
        ],
        "name": "RemoveLiquidityOne",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "bytes32",
                "name": "key",
                "type": "bytes32"
            },
            {
                "indexed": True,
                "internalType": "address",
                "name": "buyer",
                "type": "address"
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "tokensSold",
                "type": "uint256"
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "tokensBought",
                "type": "uint256"
            },
            {
                "indexed": False,
                "internalType": "uint128",
                "name": "soldId",
                "type": "uint128"
            },
            {
                "indexed": False,
                "internalType": "uint128",
                "name": "boughtId",
                "type": "uint128"
            }
        ],
        "name": "TokenSwap",
        "type": "event"
    },
    {
        "inputs": [
            {
                "internalType": "bytes32",
                "name": "key",
                "type": "bytes32"
            },
            {
                "internalType": "uint256[]",
                "name": "amounts",
                "type": "uint256[]"
            },
            {
                "internalType": "uint256",
                "name": "minToMint",
                "type": "uint256"
            },
            {
                "internalType": "uint256",
                "name": "deadline",
                "type": "uint256"
            }
        ],
        "name": "addSwapLiquidity",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "bytes32",
                "name": "key",
                "type": "bytes32"
            },
            {
                "internalType": "uint256",
                "name": "amount",
                "type": "uint256"
            }
        ],
        "name": "calculateRemoveSwapLiquidity",
        "outputs": [
            {
                "internalType": "uint256[]",
                "name": "",
                "type": "uint256[]"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "bytes32",
                "name": "key",
                "type": "bytes32"
            },
            {
                "internalType": "uint256",
                "name": "tokenAmount",
                "type": "uint256"
            },
            {
                "internalType": "uint8",
                "name": "tokenIndex",
                "type": "uint8"
            }
        ],
        "name": "calculateRemoveSwapLiquidityOneToken",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "availableTokenAmount",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "bytes32",
                "name": "key",
                "type": "bytes32"
            },
            {
                "internalType": "uint8",
                "name": "tokenIndexFrom",
                "type": "uint8"
            },
            {
                "internalType": "uint8",
                "name": "tokenIndexTo",
                "type": "uint8"
            },
            {
                "internalType": "uint256",
                "name": "dx",
                "type": "uint256"
            }
        ],
        "name": "calculateSwap",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "bytes32",
                "name": "key",
                "type": "bytes32"
            },
            {
                "internalType": "uint256[]",
                "name": "amounts",
                "type": "uint256[]"
            },
            {
                "internalType": "bool",
                "name": "deposit",
                "type": "bool"
            }
        ],
        "name": "calculateSwapTokenAmount",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "bytes32",
                "name": "key",
                "type": "bytes32"
            }
        ],
        "name": "getSwapA",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "bytes32",
                "name": "key",
                "type": "bytes32"
            }
        ],
        "name": "getSwapAPrecise",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "bytes32",
                "name": "key",
                "type": "bytes32"
            },
            {
                "internalType": "uint256",
                "name": "index",
                "type": "uint256"
            }
        ],
        "name": "getSwapAdminBalance",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "bytes32",
                "name": "key",
                "type": "bytes32"
            }
        ],
        "name": "getSwapLPToken",
        "outputs": [
            {
                "internalType": "address",
                "name": "",
                "type": "address"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "bytes32",
                "name": "key",
                "type": "bytes32"
            }
        ],
        "name": "getSwapStorage",
        "outputs": [
            {
                "components": [
                    {
                        "internalType": "bytes32",
                        "name": "key",
                        "type": "bytes32"
                    },
                    {
                        "internalType": "uint256",
                        "name": "initialA",
                        "type": "uint256"
                    },
                    {
                        "internalType": "uint256",
                        "name": "futureA",
                        "type": "uint256"
                    },
                    {
                        "internalType": "uint256",
                        "name": "initialATime",
                        "type": "uint256"
                    },
                    {
                        "internalType": "uint256",
                        "name": "futureATime",
                        "type": "uint256"
                    },
                    {
                        "internalType": "uint256",
                        "name": "swapFee",
                        "type": "uint256"
                    },
                    {
                        "internalType": "uint256",
                        "name": "adminFee",
                        "type": "uint256"
                    },
                    {
                        "internalType": "contract LPToken",
                        "name": "lpToken",
                        "type": "address"
                    },
                    {
                        "internalType": "contract IERC20[]",
                        "name": "pooledTokens",
                        "type": "address[]"
                    },
                    {
                        "internalType": "uint256[]",
                        "name": "tokenPrecisionMultipliers",
                        "type": "uint256[]"
                    },
                    {
                        "internalType": "uint256[]",
                        "name": "balances",
                        "type": "uint256[]"
                    },
                    {
                        "internalType": "uint256[]",
                        "name": "adminFees",
                        "type": "uint256[]"
                    },
                    {
                        "internalType": "bool",
                        "name": "disabled",
                        "type": "bool"
                    },
                    {
                        "internalType": "uint256",
                        "name": "removeTime",
                        "type": "uint256"
                    }
                ],
                "internalType": "struct SwapUtils.Swap",
                "name": "",
                "type": "tuple"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "bytes32",
                "name": "key",
                "type": "bytes32"
            },
            {
                "internalType": "uint8",
                "name": "index",
                "type": "uint8"
            }
        ],
        "name": "getSwapToken",
        "outputs": [
            {
                "internalType": "contract IERC20",
                "name": "",
                "type": "address"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "bytes32",
                "name": "key",
                "type": "bytes32"
            },
            {
                "internalType": "uint8",
                "name": "index",
                "type": "uint8"
            }
        ],
        "name": "getSwapTokenBalance",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "bytes32",
                "name": "key",
                "type": "bytes32"
            },
            {
                "internalType": "address",
                "name": "tokenAddress",
                "type": "address"
            }
        ],
        "name": "getSwapTokenIndex",
        "outputs": [
            {
                "internalType": "uint8",
                "name": "",
                "type": "uint8"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "bytes32",
                "name": "key",
                "type": "bytes32"
            }
        ],
        "name": "getSwapVirtualPrice",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "bytes32",
                "name": "key",
                "type": "bytes32"
            },
            {
                "internalType": "uint256",
                "name": "amount",
                "type": "uint256"
            },
            {
                "internalType": "uint256[]",
                "name": "minAmounts",
                "type": "uint256[]"
            },
            {
                "internalType": "uint256",
                "name": "deadline",
                "type": "uint256"
            }
        ],
        "name": "removeSwapLiquidity",
        "outputs": [
            {
                "internalType": "uint256[]",
                "name": "",
                "type": "uint256[]"
            }
        ],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "bytes32",
                "name": "key",
                "type": "bytes32"
            },
            {
                "internalType": "uint256[]",
                "name": "amounts",
                "type": "uint256[]"
            },
            {
                "internalType": "uint256",
                "name": "maxBurnAmount",
                "type": "uint256"
            },
            {
                "internalType": "uint256",
                "name": "deadline",
                "type": "uint256"
            }
        ],
        "name": "removeSwapLiquidityImbalance",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "bytes32",
                "name": "key",
                "type": "bytes32"
            },
            {
                "internalType": "uint256",
                "name": "tokenAmount",
                "type": "uint256"
            },
            {
                "internalType": "uint8",
                "name": "tokenIndex",
                "type": "uint8"
            },
            {
                "internalType": "uint256",
                "name": "minAmount",
                "type": "uint256"
            },
            {
                "internalType": "uint256",
                "name": "deadline",
                "type": "uint256"
            }
        ],
        "name": "removeSwapLiquidityOneToken",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "bytes32",
                "name": "key",
                "type": "bytes32"
            },
            {
                "internalType": "uint8",
                "name": "tokenIndexFrom",
                "type": "uint8"
            },
            {
                "internalType": "uint8",
                "name": "tokenIndexTo",
                "type": "uint8"
            },
            {
                "internalType": "uint256",
                "name": "dx",
                "type": "uint256"
            },
            {
                "internalType": "uint256",
                "name": "minDy",
                "type": "uint256"
            },
            {
                "internalType": "uint256",
                "name": "deadline",
                "type": "uint256"
            }
        ],
        "name": "swap",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "bytes32",
                "name": "key",
                "type": "bytes32"
            },
            {
                "internalType": "uint256",
                "name": "amountIn",
                "type": "uint256"
            },
            {
                "internalType": "address",
                "name": "assetIn",
                "type": "address"
            },
            {
                "internalType": "address",
                "name": "assetOut",
                "type": "address"
            },
            {
                "internalType": "uint256",
                "name": "minAmountOut",
                "type": "uint256"
            },
            {
                "internalType": "uint256",
                "name": "deadline",
                "type": "uint256"
            }
        ],
        "name": "swapExact",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "bytes32",
                "name": "key",
                "type": "bytes32"
            },
            {
                "internalType": "uint256",
                "name": "amountOut",
                "type": "uint256"
            },
            {
                "internalType": "address",
                "name": "assetIn",
                "type": "address"
            },
            {
                "internalType": "address",
                "name": "assetOut",
                "type": "address"
            },
            {
                "internalType": "uint256",
                "name": "maxAmountIn",
                "type": "uint256"
            },
            {
                "internalType": "uint256",
                "name": "deadline",
                "type": "uint256"
            }
        ],
        "name": "swapExactOut",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "bytes32",
                "name": "key",
                "type": "bytes32"
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "newAdminFee",
                "type": "uint256"
            },
            {
                "indexed": False,
                "internalType": "address",
                "name": "caller",
                "type": "address"
            }
        ],
        "name": "AdminFeesSet",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "bytes32",
                "name": "key",
                "type": "bytes32"
            },
            {
                "indexed": False,
                "internalType": "address",
                "name": "caller",
                "type": "address"
            }
        ],
        "name": "AdminFeesWithdrawn",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "address",
                "name": "oldAddress",
                "type": "address"
            },
            {
                "indexed": False,
                "internalType": "address",
                "name": "newAddress",
                "type": "address"
            },
            {
                "indexed": False,
                "internalType": "address",
                "name": "caller",
                "type": "address"
            }
        ],
        "name": "LPTokenTargetUpdated",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "bytes32",
                "name": "key",
                "type": "bytes32"
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "futureA",
                "type": "uint256"
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "futureTime",
                "type": "uint256"
            },
            {
                "indexed": False,
                "internalType": "address",
                "name": "caller",
                "type": "address"
            }
        ],
        "name": "RampAStarted",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "bytes32",
                "name": "key",
                "type": "bytes32"
            },
            {
                "indexed": False,
                "internalType": "address",
                "name": "caller",
                "type": "address"
            }
        ],
        "name": "RampAStopped",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "bytes32",
                "name": "key",
                "type": "bytes32"
            },
            {
                "indexed": False,
                "internalType": "address",
                "name": "caller",
                "type": "address"
            }
        ],
        "name": "SwapDisabled",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "bytes32",
                "name": "key",
                "type": "bytes32"
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "newSwapFee",
                "type": "uint256"
            },
            {
                "indexed": False,
                "internalType": "address",
                "name": "caller",
                "type": "address"
            }
        ],
        "name": "SwapFeesSet",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "bytes32",
                "name": "key",
                "type": "bytes32"
            },
            {
                "components": [
                    {
                        "internalType": "bytes32",
                        "name": "key",
                        "type": "bytes32"
                    },
                    {
                        "internalType": "uint256",
                        "name": "initialA",
                        "type": "uint256"
                    },
                    {
                        "internalType": "uint256",
                        "name": "futureA",
                        "type": "uint256"
                    },
                    {
                        "internalType": "uint256",
                        "name": "initialATime",
                        "type": "uint256"
                    },
                    {
                        "internalType": "uint256",
                        "name": "futureATime",
                        "type": "uint256"
                    },
                    {
                        "internalType": "uint256",
                        "name": "swapFee",
                        "type": "uint256"
                    },
                    {
                        "internalType": "uint256",
                        "name": "adminFee",
                        "type": "uint256"
                    },
                    {
                        "internalType": "contract LPToken",
                        "name": "lpToken",
                        "type": "address"
                    },
                    {
                        "internalType": "contract IERC20[]",
                        "name": "pooledTokens",
                        "type": "address[]"
                    },
                    {
                        "internalType": "uint256[]",
                        "name": "tokenPrecisionMultipliers",
                        "type": "uint256[]"
                    },
                    {
                        "internalType": "uint256[]",
                        "name": "balances",
                        "type": "uint256[]"
                    },
                    {
                        "internalType": "uint256[]",
                        "name": "adminFees",
                        "type": "uint256[]"
                    },
                    {
                        "internalType": "bool",
                        "name": "disabled",
                        "type": "bool"
                    },
                    {
                        "internalType": "uint256",
                        "name": "removeTime",
                        "type": "uint256"
                    }
                ],
                "indexed": False,
                "internalType": "struct SwapUtils.Swap",
                "name": "swap",
                "type": "tuple"
            },
            {
                "indexed": False,
                "internalType": "address",
                "name": "caller",
                "type": "address"
            }
        ],
        "name": "SwapInitialized",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": True,
                "internalType": "bytes32",
                "name": "key",
                "type": "bytes32"
            },
            {
                "indexed": False,
                "internalType": "address",
                "name": "caller",
                "type": "address"
            }
        ],
        "name": "SwapRemoved",
        "type": "event"
    },
    {
        "inputs": [
            {
                "internalType": "bytes32",
                "name": "_key",
                "type": "bytes32"
            }
        ],
        "name": "disableSwap",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "bytes32",
                "name": "_key",
                "type": "bytes32"
            },
            {
                "internalType": "contract IERC20[]",
                "name": "_pooledTokens",
                "type": "address[]"
            },
            {
                "internalType": "uint8[]",
                "name": "decimals",
                "type": "uint8[]"
            },
            {
                "internalType": "string",
                "name": "lpTokenName",
                "type": "string"
            },
            {
                "internalType": "string",
                "name": "lpTokenSymbol",
                "type": "string"
            },
            {
                "internalType": "uint256",
                "name": "_a",
                "type": "uint256"
            },
            {
                "internalType": "uint256",
                "name": "_fee",
                "type": "uint256"
            },
            {
                "internalType": "uint256",
                "name": "_adminFee",
                "type": "uint256"
            }
        ],
        "name": "initializeSwap",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "bytes32",
                "name": "key",
                "type": "bytes32"
            }
        ],
        "name": "isDisabled",
        "outputs": [
            {
                "internalType": "bool",
                "name": "",
                "type": "bool"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "lpTokenTargetAddress",
        "outputs": [
            {
                "internalType": "address",
                "name": "",
                "type": "address"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "bytes32",
                "name": "key",
                "type": "bytes32"
            },
            {
                "internalType": "uint256",
                "name": "futureA",
                "type": "uint256"
            },
            {
                "internalType": "uint256",
                "name": "futureTime",
                "type": "uint256"
            }
        ],
        "name": "rampA",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "bytes32",
                "name": "_key",
                "type": "bytes32"
            }
        ],
        "name": "removeSwap",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "bytes32",
                "name": "key",
                "type": "bytes32"
            },
            {
                "internalType": "uint256",
                "name": "newAdminFee",
                "type": "uint256"
            }
        ],
        "name": "setSwapAdminFee",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "bytes32",
                "name": "key",
                "type": "bytes32"
            },
            {
                "internalType": "uint256",
                "name": "newSwapFee",
                "type": "uint256"
            }
        ],
        "name": "setSwapFee",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "bytes32",
                "name": "key",
                "type": "bytes32"
            }
        ],
        "name": "stopRampA",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "newAddress",
                "type": "address"
            }
        ],
        "name": "updateLpTokenTarget",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "bytes32",
                "name": "key",
                "type": "bytes32"
            }
        ],
        "name": "withdrawSwapAdminFees",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "components": [
                    {
                        "internalType": "address",
                        "name": "facetAddress",
                        "type": "address"
                    },
                    {
                        "internalType": "enum IDiamondCut.FacetCutAction",
                        "name": "action",
                        "type": "uint8"
                    },
                    {
                        "internalType": "bytes4[]",
                        "name": "functionSelectors",
                        "type": "bytes4[]"
                    }
                ],
                "indexed": False,
                "internalType": "struct IDiamondCut.FacetCut[]",
                "name": "_diamondCut",
                "type": "tuple[]"
            },
            {
                "indexed": False,
                "internalType": "address",
                "name": "_init",
                "type": "address"
            },
            {
                "indexed": False,
                "internalType": "bytes",
                "name": "_calldata",
                "type": "bytes"
            }
        ],
        "name": "DiamondCut",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "components": [
                    {
                        "internalType": "address",
                        "name": "facetAddress",
                        "type": "address"
                    },
                    {
                        "internalType": "enum IDiamondCut.FacetCutAction",
                        "name": "action",
                        "type": "uint8"
                    },
                    {
                        "internalType": "bytes4[]",
                        "name": "functionSelectors",
                        "type": "bytes4[]"
                    }
                ],
                "indexed": False,
                "internalType": "struct IDiamondCut.FacetCut[]",
                "name": "_diamondCut",
                "type": "tuple[]"
            },
            {
                "indexed": False,
                "internalType": "address",
                "name": "_init",
                "type": "address"
            },
            {
                "indexed": False,
                "internalType": "bytes",
                "name": "_calldata",
                "type": "bytes"
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "deadline",
                "type": "uint256"
            }
        ],
        "name": "DiamondCutProposed",
        "type": "event"
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "components": [
                    {
                        "internalType": "address",
                        "name": "facetAddress",
                        "type": "address"
                    },
                    {
                        "internalType": "enum IDiamondCut.FacetCutAction",
                        "name": "action",
                        "type": "uint8"
                    },
                    {
                        "internalType": "bytes4[]",
                        "name": "functionSelectors",
                        "type": "bytes4[]"
                    }
                ],
                "indexed": False,
                "internalType": "struct IDiamondCut.FacetCut[]",
                "name": "_diamondCut",
                "type": "tuple[]"
            },
            {
                "indexed": False,
                "internalType": "address",
                "name": "_init",
                "type": "address"
            },
            {
                "indexed": False,
                "internalType": "bytes",
                "name": "_calldata",
                "type": "bytes"
            }
        ],
        "name": "DiamondCutRescinded",
        "type": "event"
    },
    {
        "inputs": [
            {
                "components": [
                    {
                        "internalType": "address",
                        "name": "facetAddress",
                        "type": "address"
                    },
                    {
                        "internalType": "enum IDiamondCut.FacetCutAction",
                        "name": "action",
                        "type": "uint8"
                    },
                    {
                        "internalType": "bytes4[]",
                        "name": "functionSelectors",
                        "type": "bytes4[]"
                    }
                ],
                "internalType": "struct IDiamondCut.FacetCut[]",
                "name": "_diamondCut",
                "type": "tuple[]"
            },
            {
                "internalType": "address",
                "name": "_init",
                "type": "address"
            },
            {
                "internalType": "bytes",
                "name": "_calldata",
                "type": "bytes"
            }
        ],
        "name": "diamondCut",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "components": [
                    {
                        "internalType": "address",
                        "name": "facetAddress",
                        "type": "address"
                    },
                    {
                        "internalType": "enum IDiamondCut.FacetCutAction",
                        "name": "action",
                        "type": "uint8"
                    },
                    {
                        "internalType": "bytes4[]",
                        "name": "functionSelectors",
                        "type": "bytes4[]"
                    }
                ],
                "internalType": "struct IDiamondCut.FacetCut[]",
                "name": "_diamondCut",
                "type": "tuple[]"
            },
            {
                "internalType": "address",
                "name": "_init",
                "type": "address"
            },
            {
                "internalType": "bytes",
                "name": "_calldata",
                "type": "bytes"
            }
        ],
        "name": "getAcceptanceTime",
        "outputs": [
            {
                "internalType": "uint256",
                "name": "",
                "type": "uint256"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "components": [
                    {
                        "internalType": "address",
                        "name": "facetAddress",
                        "type": "address"
                    },
                    {
                        "internalType": "enum IDiamondCut.FacetCutAction",
                        "name": "action",
                        "type": "uint8"
                    },
                    {
                        "internalType": "bytes4[]",
                        "name": "functionSelectors",
                        "type": "bytes4[]"
                    }
                ],
                "internalType": "struct IDiamondCut.FacetCut[]",
                "name": "_diamondCut",
                "type": "tuple[]"
            },
            {
                "internalType": "address",
                "name": "_init",
                "type": "address"
            },
            {
                "internalType": "bytes",
                "name": "_calldata",
                "type": "bytes"
            }
        ],
        "name": "proposeDiamondCut",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "components": [
                    {
                        "internalType": "address",
                        "name": "facetAddress",
                        "type": "address"
                    },
                    {
                        "internalType": "enum IDiamondCut.FacetCutAction",
                        "name": "action",
                        "type": "uint8"
                    },
                    {
                        "internalType": "bytes4[]",
                        "name": "functionSelectors",
                        "type": "bytes4[]"
                    }
                ],
                "internalType": "struct IDiamondCut.FacetCut[]",
                "name": "_diamondCut",
                "type": "tuple[]"
            },
            {
                "internalType": "address",
                "name": "_init",
                "type": "address"
            },
            {
                "internalType": "bytes",
                "name": "_calldata",
                "type": "bytes"
            }
        ],
        "name": "rescindDiamondCut",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "uint32",
                "name": "_domain",
                "type": "uint32"
            },
            {
                "internalType": "address",
                "name": "_xAppConnectionManager",
                "type": "address"
            },
            {
                "internalType": "uint256",
                "name": "_acceptanceDelay",
                "type": "uint256"
            },
            {
                "internalType": "address",
                "name": "_lpTokenTargetAddress",
                "type": "address"
            }
        ],
        "name": "init",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "bytes4",
                "name": "_functionSelector",
                "type": "bytes4"
            }
        ],
        "name": "facetAddress",
        "outputs": [
            {
                "internalType": "address",
                "name": "facetAddress_",
                "type": "address"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "facetAddresses",
        "outputs": [
            {
                "internalType": "address[]",
                "name": "facetAddresses_",
                "type": "address[]"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "address",
                "name": "_facet",
                "type": "address"
            }
        ],
        "name": "facetFunctionSelectors",
        "outputs": [
            {
                "internalType": "bytes4[]",
                "name": "facetFunctionSelectors_",
                "type": "bytes4[]"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [],
        "name": "facets",
        "outputs": [
            {
                "components": [
                    {
                        "internalType": "address",
                        "name": "facetAddress",
                        "type": "address"
                    },
                    {
                        "internalType": "bytes4[]",
                        "name": "functionSelectors",
                        "type": "bytes4[]"
                    }
                ],
                "internalType": "struct IDiamondLoupe.Facet[]",
                "name": "facets_",
                "type": "tuple[]"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    },
    {
        "inputs": [
            {
                "internalType": "bytes4",
                "name": "_interfaceId",
                "type": "bytes4"
            }
        ],
        "name": "supportsInterface",
        "outputs": [
            {
                "internalType": "bool",
                "name": "",
                "type": "bool"
            }
        ],
        "stateMutability": "view",
        "type": "function"
    }
]