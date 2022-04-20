

from distutils.command.config import config
from brownie import accounts,network

LOCAL_BLOCKCHAIN = ['mainnet-fork','development']

def get_account(index=None,id=None):
    if index:
        return accounts[index]
    if id:
        return accounts.load(id)
    if network.show_active() in LOCAL_BLOCKCHAIN:
        account = accounts[0]
        return account
    

def main():
    get_account()