import RSALIB
from testing_functions import execTime

@execTime
def encrypt(publicKey, message):
    encrypted = RSALIB.RSAEnc(publicKey, message)
    return encrypted

@execTime
def decrypt(privateKey, encrypted):
    return RSALIB.RSADec(privateKey, encrypted)

@execTime
def test_functionality(keySize, message):
    print("testing key size of ", keySize)
    keys = RSALIB.genKeys(keySize)
    publicKey, privateKey = keys
    print("message: ", message)
    print("encrypted = ")
    encrypted = encrypt(publicKey, message)
    print(encrypted)
    print("decrypted = ")
    print(decrypt(privateKey, encrypted))

for i in range(5, 20):
    try:
        test_functionality(i, "hello world")
        print("")
    except:
        print("Error")
        print("")

