from asyncore import read
from brownie import accounts, config, network, SimpleStorage


def read_contract():
    simple_storage = SimpleStorage[-1]  # most recent deployment of SimpleStorage
    print(simple_storage.retrieve())


def main():
    read_contract()
