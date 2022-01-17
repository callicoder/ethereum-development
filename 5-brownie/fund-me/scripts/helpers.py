from brownie import accounts, config, network, MockV3Aggregator
from web3 import Web3

DECIMALS = 8
STARTING_PRICE = 2000_00000000
LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]
FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork", "mainnet-fork-dev"]


def get_account():
    active_network = network.show_active()
    if (
        active_network in LOCAL_BLOCKCHAIN_ENVIRONMENTS
        or active_network in FORKED_LOCAL_ENVIRONMENTS
    ):
        # Brownie's mainnet-fork don't have these pre-created accounts. So you can create your custom mainnet fork
        return accounts[0]
    return accounts.add(config["wallets"]["from_key"])


def get_price_feed_address():
    active_network = network.show_active()
    if active_network not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        price_feed_address = config["networks"][active_network]["eth_usd_price_feed"]
    else:
        deploy_mocks()
        price_feed_address = MockV3Aggregator[-1].address
    return price_feed_address


def deploy_mocks():
    active_network = network.show_active()
    print(f"The active network is {active_network}")
    print("Deploying mocks...")
    if len(MockV3Aggregator) == 0:
        MockV3Aggregator.deploy(
            DECIMALS, Web3.toWei(STARTING_PRICE, "ether"), {"from": get_account()}
        )
    print("Mocks deployed!")
