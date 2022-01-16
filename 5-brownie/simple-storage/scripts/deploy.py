from brownie import accounts, config, network, SimpleStorage


def deploy_simple_storage():
    # account = accounts[0]  # first account from the default ganache blockchain
    # print(account)

    # account = accounts.load("metamask-kovan") # Added using brownie accounts new metamask-kovan
    # print(account)

    # account = accounts.add(os.getenv("PRIVATE_KEY"))
    # account = accounts.add(config["wallets"]["from_key"])

    account = get_account()
    simple_storage = SimpleStorage.deploy({"from": account})
    stored_value = simple_storage.retrieve()
    print(stored_value)

    transaction = simple_storage.store(15, {"from": account})
    transaction.wait(1)
    updated_stored_value = simple_storage.retrieve()
    print(updated_stored_value)


def get_account():
    if network.show_active() == "development":
        return accounts[0]
    return accounts.add(config["wallets"]["from_key"])


def main():
    deploy_simple_storage()
