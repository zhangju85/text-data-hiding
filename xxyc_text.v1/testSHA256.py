import hashlib
hash=hashlib.sha256();
hash.update(bytes('taylorswift',encoding='utf-8'))
print(hash.hexdigest())