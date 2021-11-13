from blockchain import Blockchain

chain = Blockchain()
chain.append(data={"from": "John", "to": "Bob", "amount": 100})
chain.append(data={"from": "Bob", "to": "John", "amount": 50})

print(chain)

assert chain.is_valid()
