from solathon import Client, Keypair

client = Client("https://api.testnet.solana.com")

def create_wallet():
    keypair = Keypair()
    public_key = keypair.public_key
    private_key = keypair.private_key

    return public_key, private_key