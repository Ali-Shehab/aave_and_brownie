def deposit():
    account = get_account()
    erc20_address = config["networks"][network.show_active()]["weth_token"]
    if network.show_active() in ["mainnet-fork"]:
        transfer_Eth_to_WETH()
    lending_p = lending_pool()
    approve_tx = approve_erc20( lending_p.address,AMOUNT, erc20_address, account)
    print("Depositing...")
    tx = lending_p.deposit(
        erc20_address, AMOUNT, account.address, 0, {"from": account}
    )
    tx.wait(1)
    print("Deposited!")
    # ...how much?
    borrowable_eth, total_debt = get_borrowable_data(lending_p, account)
    print("Let's borrow!")
    # DAI in terms of ETH
    dai_eth_price = get_latest_price()
    amount_dai_to_borrow = (1 / dai_eth_price) * (borrowable_eth * 0.95)
    print(f"We are going to borrow {amount_dai_to_borrow} DAI")
    dai_address = config["networks"][network.show_active()]["dai_token"]
    borrow_tx = lending_p.borrow(dai_address,Web3.toWei(amount_dai_to_borrow, "ether"),1,0,account.address,{"from": account},)
    borrow_tx.wait(1)
    print("We borrowed some DAI!")
    get_borrowable_data(lending_p, account)
    # I made an oopsie in the video with this!!
    repay_all(Web3.toWei(amount_dai_to_borrow, "ether"), lending_p, account)
    get_borrowable_data(lending_p, account)
    print(
        "You just deposited, borrowed, and repayed with Aave, Brownie, and Chainlink!"
    )


def repay_all(amount, lending_pool, account):
    approve_erc20(lending_pool,Web3.toWei(amount, "ether"),config["networks"][network.show_active()]["dai_token"],account,)
    repay_tx = lending_pool.repay(config["networks"][network.show_active()]["dai_token"],amount,1,account.address,{"from": account}, )
    repay_tx.wait(1)

    print("Repaid!")
