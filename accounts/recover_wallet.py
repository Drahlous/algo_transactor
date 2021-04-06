from algosdk import kmd, mnemonic

kmd_token = "<kmd-token>"
kmd_address = "<kmd-address>"

# create a kmd client
kcl = kmd.KMDClient(kmd_token, kmd_address)

# get the master derivation key from the mnemonic
backup = "<wallet-mnemonic>"
mdk = mnemonic.to_master_derivation_key(backup)

# recover the wallet by passing mdk when creating a wallet
new_wallet = kcl.create_wallet("MyTestWallet2", "testpassword", master_deriv_key=mdk)

walletid = new_wallet.get("id")
print("Created Wallet: ", walletid)

wallethandle = kcl.init_wallet_handle(walletid, "testpassword")
print("Got wallet handle:", wallethandle)

rec_addr = kcl.generate_key(wallethandle)
print("Recovered account:", rec_addr)