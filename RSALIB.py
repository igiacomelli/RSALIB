import random

def isPrime(n):
    for i in range(2, int(n**0.5)  + 1):
        if n % i == 0:
            return False
    return True

def gcd(x, y):
    while x != 0:
        x, y = y % x, x
    return y

def modInverse(x, y):
    if gcd(x, y) != 1:
        return None
    u1, u2, u3 = 1, 0, x
    v1, v2, v3 = 0, 1, y

    while v3 != 0:
        q = u3 // v3
        v1, v2, v3, u1, u2, u3 = (u1 - q * v1), (u2 - q * v2), (u3 - q * v3), v1, v2, v3
    return u1 % y


#first, cache primes
minPrime = 2
maxPrime = 1000
cached_primes = [i for i in range(minPrime, maxPrime) if isPrime(i)]

def randNum(keySize):
    return (random.randrange(2**(keySize-1)+1, 2**keySize-1))

def smallPrime(keySize):
    while True:
        pc = randNum(keySize)

        for divisor in cached_primes:
            if pc % divisor == 0 and divisor**2 <= pc:
                break
        else:
            return pc

def isMillerRabin(n):
    count = 0
    m = n - 1

    while count % 2 == 0:
        m = m // 2
        count += 1
    for candidates in range(5):
        a = random.randrange(2, n - 1)
        v = pow(a, m, n)
        if v != 1:
            i = 0
            while v != (n - 1):
                if i == (count - 1):
                    return False
                else:
                    i += 1
                    v = (v**2) % n
    return True

def makeLargePrime(keySize):
    while True:
        n = random.randrange(2**(keySize-1), 2**(keySize))
        if isPrime(n):
            return n

def genKeys(keySize):
    #making p, q, n
    p = random.choice([i for i in cached_primes])
    q = random.choice([i for i in cached_primes if i != p])
    n = p * q

    #make e
    phi = (p - 1) * (q - 1)
    while True:
        e = random.randrange(2 ** (keySize - 1), 2**(keySize))
        if gcd(e, phi) == 1:
            break

    #make d (mod inverse of e)
    d = modInverse(e, phi)
    publicKey = (n, e)
    privateKey = (n, d)
    print("pubkey: ", publicKey)        #for testing
    print("privkey: ", privateKey)      #for testing
    return(publicKey, privateKey)

def RSAEnc(publickKey, message):
    n, e = publickKey
    encrypted = []
    encryptedCharacter = 0
    for i in message:
        encryptedCharacter = ((ord(i) ** e) % n)
        encrypted.append(encryptedCharacter)
    return encrypted

def RSADec(privateKey, encrypted):
    n, d = privateKey
    decrypted = ""
    decryptedCharacter = ''
    decryptedInteger = 0
    for i in encrypted:
        decryptedInteger = (int(i) ** d) % n
        decryptedCharacter = chr(decryptedInteger)
        decrypted += decryptedCharacter
    return decrypted

def convertToBytes(tuple):
    string = str(tuple)
    bytes = string.encode()
    return bytes

def convertFromBytes(bytes):
    string = bytes.decode()
    slicedString = string[1:-1]
    tuples = tuple(map(int, slicedString.split(', ')))
    return tuples

#statement below demonstrating functionality

keys = genKeys(256)
publicKey, privateKey = keys
message = "wtf"
print(message)
print("encrypted = ")
encrypted = RSAEnc(publicKey, message)
print(encrypted)
print("decrypted = ")
print(RSADec(privateKey, encrypted))
