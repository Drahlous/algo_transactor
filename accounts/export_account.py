from algosdk import kmd, mnemonic
from algosdk.wallet import Wallet

kmd_token = "<kmd-token>"
kmd_address = "<kmd-address>"

# create a kmd client
kcl = kmd.KMDClient(kmd_token, kmd_address)

walletid = None
wallets = kcl.list_wallets()
for arrayitem in wallets:
    if arrayitem.get("name") == "MyTestWallet2":
        walletid = arrayitem.get("id")
        break

wallethandle = kcl.init_wallet_handle(walletid, "testpassword")
accountkey = kcl.export_key(wallethandle, "testpassword", "<account address>" )
mn = mnemonic.from_private_key(accountkey)
print("Account Mnemonic: ", mn)