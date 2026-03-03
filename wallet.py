import hashlib
import secrets


class Wallet:
    """
    Simple wallet simulation generating pseudo public/private keys.
    """

    def __init__(self):
        self.private_key = secrets.token_hex(32)
        self.public_key = hashlib.sha256(self.private_key.encode()).hexdigest()

    def get_address(self) -> str:
        """
        Returns wallet address (public key).
        """
        return self.public_key


if __name__ == "__main__":
    wallet = Wallet()
    print("Private Key:", wallet.private_key)
    print("Public Address:", wallet.get_address())
