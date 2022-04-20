from brownie import network,config,interface, web3
from scripts.used_functions import (get_account,)
from scripts.transfer_Eth_to_WETH import (transfer_Eth_to_WETH,)
from web3 import Web3


VALUE = Web3.toWei(0.1,"ether")
def depositing_weth():
    account = get_account()
    erc20_address = config["networks"][network.show_active()]["weth_token"]
    if network.show_active() in ["mainnet-fork"]:
        transfer_Eth_to_WETH()
    lending_p = lending_pool()
    approve_erc20( lending_p.address,VALUE, erc20_address, account)
    print("Depositing...")
    tx = lending_p.deposit(
        erc20_address, VALUE, account.address, 0, {"from": account}
    )
    tx.wait(1)
    print("Deposited!")
    borrowable_eth ,total_debt = get_borrowable_data(lending_p, account)
    print("Let us borrow some DIA")
    dai_to_eth_price = get_latest_price()
    dai = (1 / dai_to_eth_price) * (borrowable_eth * 0.95)
    print(f"We are going to borrow {dai} DAI")
    dai_address = config["networks"][network.show_active()]["dai_token"]
    borrow_tx = lending_p.borrow(dai_address,Web3.toWei(dai,"ether"),1,0,account.address,{"from":account})
    borrow_tx.wait(1)
    print("Borrowed")
    get_borrowable_data(lending_p,account)
    print("Repaying...")
    approve_erc20(lending_p,Web3.toWei(VALUE, "ether"),config["networks"][network.show_active()]["dai_token"],account,)
    repay_tx = lending_p.repay(config["networks"][network.show_active()]["dai_token"],VALUE,1,account.address,{"from": account},)
    repay_tx.wait(1)
    print("Repaid!")
    get_borrowable_data(lending_p,account)

def get_borrowable_data(lending_pool, account):
    (
        total_collateral_eth,
        total_debt_eth,
        available_borrow_eth,
        current_liquidation_threshold,
        ltv,
        health_factor,
    ) = lending_pool.getUserAccountData(account.address)
    available_borrow_eth = Web3.fromWei(available_borrow_eth, "ether")
    total_collateral_eth = Web3.fromWei(total_collateral_eth, "ether")
    total_debt_eth = Web3.fromWei(total_debt_eth, "ether")
    print(f"You have {total_collateral_eth} worth of ETH deposited.")
    print(f"You have {total_debt_eth} worth of ETH borrowed.")
    print(f"You can borrow {available_borrow_eth} worth of ETH.")
    return (float(available_borrow_eth), float(total_debt_eth))

def get_latest_price():
    dai_eth_priceFeed = interface.AggregatorV3Interface(config["networks"][network.show_active()]["dai_eth_price_feed"])
    latest_price = dai_eth_priceFeed.latestRoundData()[1]
    converted_latest_price = Web3.fromWei(latest_price, "ether")
    print(f"The DAI/ETH price is {converted_latest_price}")
    return float(converted_latest_price)

def lending_pool():
    lending_pool_address_provider = interface.ILendingPoolAddressesProvider(
        config["networks"][network.show_active()]["lending_pool_addresses_provider"]
    )
    lending_pool_address = lending_pool_address_provider.getLendingPool()
    lending_pool = interface.ILendingPool(lending_pool_address)
    return lending_pool

def approve_erc20(spender, value ,erc_20_address, account):
    print("Approving ERC20...")
    approving = interface.IERC20(erc_20_address)
    approve = approving.approve(spender,value,{"from":account})
    approve.wait(1)
    print("Approved")
    return approve

def main():
    depositing_weth()