import random
from testing_functions import execTime
import time


#function to test if a given number is prime
def isPrime(n):
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True

#returns the greatest common factor of two numbers
def gcd(x, y):
    while x != 0:
        x, y = y % x, x
    return y

#returns the mod inverse of x
def modInverse(x, y):
    if gcd(x, y) != 1:
        return None
    u1, u2, u3 = 1, 0, x
    v1, v2, v3 = 0, 1, y

    while v3 != 0:
        q = u3 // v3
        v1, v2, v3, u1, u2, u3 = (u1 - q * v1), (u2 - q * v2), (u3 - q * v3), v1, v2, v3
    return u1 % y

#returns a random number based on a key size
def randNum(keySize):
    return (random.randrange(2**(keySize-1)+1, 2**keySize-1))

#returns a small prime within the range of primes generated in cached_primes
def smallPrime(keySize):
    while True:
        #getting a random number based on key size
        pc = randNum(keySize)
        # list of cached primes up to 1000 to be used for isMillerRabin()
        minPrime = 2
        maxPrime = 1000
        cached_primes = [i for i in range(minPrime, maxPrime) if isPrime(i)]

        for divisor in cached_primes:
            if pc % divisor == 0 and divisor**2 <= pc:
                break
        else:
            return pc

#both randNum() and smallPrime() are anachronistic and no longer needed. they ere kept here to show evolution of the program.
#they were originally used before makeLargePrime() was implemented.

#tests if a given number is a "miller rabin" number, which is required
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

def isPrimeExt(n):
    # list of cached primes up to 1000 to be used for isMillerRabin()\
    minPrime = 2
    maxPrime = 1000
    cached_primes = [i for i in range(minPrime, maxPrime) if isPrime(i)]

    #testing if a number is prime. if a number is small enough then it can be directly teted, otherwise it must be inferred
    #using isMillerRabin()
    if n < 2:
        return False
    if n in cached_primes:
        return True
    for primeNumber in cached_primes:
        if n % primeNumber == 0:
            return False
    return isMillerRabin(n)

def makeLargePrime(keySize):
    while True:
        n = random.randrange(2**(keySize-1), 2**(keySize))
        if isPrime(n):
            return n

def genKeys(keySize):
    #making p, q, n
    p = makeLargePrime(keySize)
    q = makeLargePrime(keySize)
    n = p * q

    #make e
    #variable called phi in place of (p-1) * (q-1)
    phi = (p - 1) * (q - 1)
    while True:
        #generating e
        e = random.randrange(2 ** (keySize - 1), 2**(keySize))
        #testing if coprime
        if gcd(e, phi) == 1:
            break

    #make d (mod inverse of e)
    d = modInverse(e, phi)
    #making the keys and returning them in a tuple of tuples
    publicKey = (n, e)
    privateKey = (n, d)
    #print("pubkey: ", publicKey)        #for testing
    #print("privkey: ", privateKey)      #for testing
    return(publicKey, privateKey)

#encrypts a string
def RSAEnc(publickKey, message):
    n, e = publickKey
    encrypted = []
    encryptedCharacter = 0
    for i in message:
        encryptedCharacter = ((ord(i)**e) % n)
        encrypted.append(encryptedCharacter)
    return encrypted

#decrypts a list of encrypted characters
def RSADec(privateKey, encrypted):
    n, d = privateKey
    decrypted = ""
    decryptedCharacter = ''
    decryptedInteger = 0
    for i in encrypted:
        #print("iteration")                         #for testing
        decryptedInteger = (int(i)**d) % n
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


def test_functionality(keySize):
    print("testing key size of ", keySize)
    keys = genKeys(keySize)
    publicKey, privateKey = keys
    message = "hello world"
    print("message: ", message)
    print("encrypted = ")
    encrypted = RSAEnc(publicKey, message)
    print(encrypted)
    print("decrypted = ")
    print(RSADec(privateKey, encrypted))


