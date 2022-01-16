from solcx import compile_standard
from solcx import install_solc
from web3 import Web3
from dotenv import load_dotenv
import json
import os

load_dotenv()

with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()

# Compile our solidity
install_solc("0.8.0")
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
            }
        },
    },
    solc_version="0.8.0",
)

with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

# get bytecode
bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
    "bytecode"
]["object"]

# get abi
abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]

# connect to the blockchain
endpoint = "https://kovan.infura.io/v3/b1a8c63042d941fabccb89eca4edaa13"  # "http://127.0.0.1:8545" (for Ganache)
w3 = Web3(Web3.HTTPProvider(endpoint))
chain_id = 42  # 1337 (for Ganache)
account_address = "0x4ae110382de86cfC3ac59c06856DE9CBFB096bba"  # Metamask account address for the selected network or Ganache account address
my_address = w3.toChecksumAddress(account_address)

# Don't keep your private key in code. Otherwise, it can be stolen from your github repository.
# You should keep private key in environment variable.
# Brownie has a better way for private key management.
private_key = os.getenv("PRIVATE_KEY")

# create the contract in python
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)

# get the latest transaction
nonce = w3.eth.getTransactionCount(my_address)

# 1. build the transaction
transaction = SimpleStorage.constructor().buildTransaction(
    {
        "gasPrice": w3.eth.gas_price,
        "chainId": chain_id,
        "from": my_address,
        "nonce": nonce,
    }
)

# 2. sign the transaction
signed_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)

# 3. send this signed transaction
print("Deploying contract...")
txn_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)

# wait for block confirmations
txn_receipt = w3.eth.wait_for_transaction_receipt(txn_hash)
print("Deployed!")

# working with the contract => need contract address and abi
simple_storage = w3.eth.contract(address=txn_receipt.contractAddress, abi=abi)

# Two ways to interact with a contract => Call vs Transact
# Call => Simulate making the call and getting a return value. Calls don't make a state change
# Transact => Actually make a state change. Even if you use Transact on a view function, it won't make a state change
print(simple_storage.functions.retrieve().call({"from": my_address}))
print(
    simple_storage.functions.store(15).call({"from": my_address})
)  # Only simulates the store call. If you do retrieve after this, it will still return zero.
print(simple_storage.functions.retrieve().call({"from": my_address}))

# Now let's actually transact and make a state change
print("Updating contract...")
store_transaction = simple_storage.functions.store(15).buildTransaction(
    {
        "gasPrice": w3.eth.gas_price,
        "chainId": chain_id,
        "from": my_address,
        "nonce": nonce + 1,
    }
)
signed_store_txn = w3.eth.account.sign_transaction(
    store_transaction, private_key=private_key
)
store_txn_hash = w3.eth.send_raw_transaction(signed_store_txn.rawTransaction)
store_txn_receipt = w3.eth.wait_for_transaction_receipt(store_txn_hash)
print("Updated!")
print(simple_storage.functions.retrieve().call({"from": my_address}))
