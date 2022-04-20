
import imp
from scripts.used_functions import (get_account,)
from brownie import accounts, network, config , interface

def transfer_Eth_to_WETH():
    account = get_account()
    weth = interface.IWETH(config["networks"][network.show_active()]["weth_token"])
    tx = weth.deposit({"from":account,"value":0.1 * 10 **18})
    tx.wait(1)
    print("Converted to eth")


def main():
    transfer_Eth_to_WETH()