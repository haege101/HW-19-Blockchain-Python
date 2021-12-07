# Import dependencies
import subprocess
import json
import os
from dotenv import load_dotenv
from bit import PrivateKeyTestnet
from bit.network import NetworkAPI
from web3 import Web3
from eth_account import Account
from constants import *

w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
# Load and set environment variables
load_dotenv()
mnemonic=os.getenv("mnemonic")

# Create a function called `derive_wallets`
def derive_wallets(mnemonic, coin, numderive):
    command = 'php derive -g --mnemonic="'+str(mnemonic)+'" --numderive='+str(numderive)+' --coin='+str(coin)+' --format=jsonpretty'
    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    output, err = p.communicate()
    p_status = p.wait()
    return json.loads(output)

# Create a dictionary object called coins to store the output from `derive_wallets`.
coins = {'ETH', 'BTC'}


# Create a function called `priv_key_to_account` that converts privkey strings to account objects.
def priv_key_to_account(coin, priv_key):
    if coin =="ETH":
        return Account.privateKeyToAccount(priv_key)
    if  coin == "BTC":
        return PrivateKeyTestnet(priv_key)

# Create a function called `create_tx` that creates an unsigned transaction appropriate metadata.
def create_tx(coin, account, recipient, amount):
    if coin == ETH:
        gasEstimate = w3.eth.estimateGas(
            {"from": account.address, "to": recipient, "value": amount}
        )
        return {
            "to": recipient,
            "from": account.address,
            "value": amount,
            "gasPrice": w3.eth.gasPrice,
            "gas": gasEstimate,
            "nonce": w3.eth.getTransactionCount(account.address)
        }

    if coin == BTC:
        return PrivateKeyTestnet.prepare_transaction(account.address, [(recipient, amount, BTC)])


# Create a function called `send_tx` that calls `create_tx`, signs and sends the transaction.

def create_raw_tx(coin, account, recipient, amount):
    if coin == "ETH":
        gasEstimate = w3.eth.estimateGas(
            {"from": account.address, "to": recipient, "value": amount}
        )
        return {
            "from": account.address,
            "to": recipient,
            "value": amount,
            "gasPrice": w3.eth.gasPrice,
            "gas": gasEstimate,
            "nonce": w3.eth.getTransactionCount(account.address),
        }
    elif coin == "BTC":
        return PrivateKeyTestnet.prepare_transaction(account.address, [to, amount, BTC] )


    def send_tx(coin, account, recipient, amount):
        if coin =="ETH":
            tx = create_raw_tx("ETH", account, recipient, amount)
            signed_tx = account.sign_transaction(tx)
            result = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
            print(result.hex())
            return result.hex()
        elif coin == "BTC":
            tx = create_raw_tx("BTC", account, recipient, amount)
            signed_tx = account.sign_transaction(tx)
            result = NetworkAPI.broadcast_tx_testnet(signed)
