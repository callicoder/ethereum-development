from scripts.helpers import get_account
from brownie import OurToken, network, config
from web3 import Web3

initial_supply = Web3.toWei(1000, "ether")


def deploy_token():
    account = get_account()
    our_token = OurToken.deploy(initial_supply, {"from": account})

    print(f"Deployed {our_token.name()}")


def main():
    deploy_token()
