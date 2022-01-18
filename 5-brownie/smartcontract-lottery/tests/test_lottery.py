from brownie import Lottery, config, network
from scripts.helpers import get_account
from web3 import Web3


def test_get_entrance_fee():
    account = get_account()
    lottery = Lottery.deploy(
        config["networks"][network.show_active()]["eth_usd_price_feed"],
        {"from": account},
    )

    assert lottery.getEntranceFee() > Web3.toWei(0.015, "ether")
    assert lottery.getEntranceFee() < Web3.toWei(0.020, "ether")
