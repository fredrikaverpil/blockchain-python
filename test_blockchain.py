from blockchain import Block
from blockchain import Blockchain
from time import time


def test():
    chain = Blockchain()
    chain.append(data={"from": "John", "to": "Bob", "amount": 100})
    chain.append(data={"from": "Bob", "to": "John", "amount": 50})

    print(chain)


if __name__ == "__main__":
    test()
