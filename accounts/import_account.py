from algosdk import kmd, mnemonic

kmd_token = "<kmd-token>"
kmd_address = "http://" + "<kmd-address>"

# create a kmd client
kcl = kmd.KMDClient(kmd_token, kmd_address)

walletid = None
wallets = kcl.list_wallets()
for arrayitem in wallets:
    if arrayitem.get("name") == "MyTestWallet2":
        walletid = arrayitem.get("id")
        break
print("Got Wallet ID:", walletid)

wallethandle = kcl.init_wallet_handle(walletid, "testpassword")
print("Got Wallet Handle:", wallethandle)

private_key, address = "account.generate_account()"
print("Account:", address)

mn = mnemonic.from_private_key(private_key)
print("Mnemonic", mn)

importedaccount = kcl.import_key(wallethandle, private_key)
print("Account successfully imported: ", importedaccount)
