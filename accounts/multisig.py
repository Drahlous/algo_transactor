from algosdk import account, transaction

# Multisig accounts provide extra security
# Requires multiple accounts to authorize spending
# but they are less convenient

# generate three accounts
private_key_1, account_1 = account.generate_account()
private_key_2, account_2 = account.generate_account()
private_key_3, account_3 = account.generate_account()
print("Account 1:", account_1)
print("Account 2", account_2)
print("Account 3:", account_3)

# create a multisig account
version = 1  # multisig version
threshold = 2  # how many signatures are necessary
msig = transaction.Multisig(version, threshold, [account_1, account_2])
print("Multisig Address: ", msig.address())