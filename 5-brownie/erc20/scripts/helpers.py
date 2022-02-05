from brownie import (
    accounts,
    config,
    network,
)

LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]
FORKED_LOCAL_ENVIRONMENTS = ["mainnet-fork", "mainnet-fork-dev"]


def get_account(index=None, id=None):
    if index:
        return accounts[index]

    if id:
        accounts.load(id)  # from brownie accounts list

    active_network = network.show_active()
    if (
        active_network in LOCAL_BLOCKCHAIN_ENVIRONMENTS
        or active_network in FORKED_LOCAL_ENVIRONMENTS
    ):
        # Brownie's mainnet-fork don't have these pre-created accounts. So you can create your custom mainnet fork
        return accounts[0]

    return accounts.add(config["wallets"]["from_key"])
