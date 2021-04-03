from algosdk.future.transaction import PaymentTxn
from algosdk.v2client import algod
from algosdk import account, mnemonic
import json
import base64

# ==============
# Create Client
# ==============


algod_address = "http://localhost:4001"
algod_token = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
algod_client = algod.AlgodClient(algod_token, algod_address)


# Check node status
status = algod_client.status()
print(json.dumps(status, indent=4))


# Check the suggested transaction params
try:
  params = algod_client.suggested_params()
  print(json.dumps(vars(params), indent=4))
except Exception as e:
  print(e)



# ==============
# Generate Wallet
# ==============

# Helper function, generate an address and private key
def generate_algorand_keypair():
  private_key, address = account.generate_account()
  print("Address: {}".format(address))
  print("Passphrase: {}".format(mnemonic.from_private_key(private_key)))

# 25-word mnemonic passphrase
passphrase = "box spread enforce suspect unit immense stove exact palace window effort wide urge need switch leisure write lab drum mistake penalty they uniform above immense"

# Create address
private_key =   mnemonic.to_private_key(passphrase)
my_address  =   mnemonic.to_public_key(passphrase)
print("Wallet Address: {}".format(my_address))

# Create a client using the address
account_info = algod_client.account_info(my_address)
print("Account Balance: {} micro_algos".format(account_info.get('amount')))




# ==============
# Constructing Transactions
# ==============

# Create a wallet to receive funds
receiving_passphrase = "actor purpose funny fetch shadow fox heavy police side snack silent purse illness average whip marble rookie useless mouse dutch involve stick penalty absent step"
receiving_address = "GD64YIY3TWGDMCNPP553DZPPR6LDUSFQOIJVFDPPXWEG3FVOJCCDBBHU5A"


# Set transaction params
# Use Suggested fees for now, uncomment for custom fees
params = algod_client.suggested_params()
# params.flat_fee = True
# params.fee = 1000


note = "Welcome to Algorand!".encode()


# Generate Transaction: Address, Params, Receiver, Amount, Close_remainder_to=None, note, lease=None, Rekey_to=None
# close_remainder_to: We close this account and send all of our ALGOs
# note: up to 1kb of sender-supplied arbitrary data
# lease: No other transactions with this sender-lease pair will be processed this round (anti-double-spend)
# rekey_to: rekey the sender to this address (point to that wallet)
unsigned_txn = PaymentTxn(my_address, params, receiving_address, 1000000, None, note)

# Sign the transaction
signed_txn = unsigned_txn.sign(mnemonic.to_private_key(passphrase))

# Submit transaction to the chain
txid = algod_client.send_transaction(signed_txn)
print("Successfully sent transaction with txID: {}".format(txid))


# ==============
# ! Always wait for the transaction to be confirmed by the network
# ! Transaction will be confirmed within 1 block
# ! Read back the transaction before proceeding
# ==============

# utility for waiting on a transaction confirmation
def wait_for_confirmation(client, transaction_id, timeout):
  """
  Wait until the transaction is confirmed or rejected, or until 'timeout'
  number of rounds have passed.
  Args:
    transaction_id (str): the transaction to wait for
    timeout (int): maximum number of rounds to wait
  Returns:
    dict: pending transaction information, or throws an error if the transaction
      is not confirmed or rejected in the next timeout rounds
  """
  start_round = client.status()["last-round"] + 1
  current_round = start_round

  while current_round < start_round + timeout:
    try:
      pending_txn = client.pending_transaction_info(transaction_id)
    except Exception:
      return
    if pending_txn.get("confirmed-round", 0) > 0:
      return pending_txn
    elif pending_txn["pool-error"]:
      raise Exception('pool error: {}'.format(pending_txn["pool-error"]))
    client.status_after_block(current_round)
    current_round += 1
  raise Exception('pending tx not found in timeout rounds, timeout value = : {}'.format(timeout))
 
# wait for confirmation
try:
  confirmed_txn = wait_for_confirmation(algod_client, txid, 4)
except Exception as err:
  print(err)

print("Transaction information: {}".format(json.dumps(confirmed_txn, indent=4)))
print("Decoded note: {}".format(base64.b64decode(confirmed_txn["txn"]["txn"]["note"]).decode()))


quit()