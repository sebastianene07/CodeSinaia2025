import hashlib
import secrets
import os

# pip install pycryptodome
from Crypto.Cipher import AES

filename = "encrypted.bin"
choice = input("Choose action ? {decrypt | update_password | encrypt}")
if choice == "decrypt":
    # Simulate booting the device again
    with open(filename, "rb") as f:
        salt = f.read(16)
        encrypted_dek = f.read(16)
        encrypted_payload = f.read()

    password = input("Enter your password: ").encode('utf-8')
    if not password:
        print("Password cannot be empty.")
        exit(1)

    # Calculate IK1
    ik1 = hashlib.scrypt(
        password=password,
        salt=salt,
        n=16384,
        r=8,
        p=1,
        dklen=32
    )

    # Decrypt DEK
    cipher = AES.new(ik1[:16], AES.MODE_CBC, iv=ik1[16:32])
    dek = cipher.decrypt(encrypted_dek)
    print("[*] DEK decrypted successfully:", dek.hex())

    # Decrypt payload
    cipher2 = AES.new(dek, AES.MODE_CBC, iv=salt)
    decrypted_payload = cipher2.decrypt(encrypted_payload)

    print("[*] Payload decrypted successfully:", decrypted_payload)
    print("[*] Your secret was:", decrypted_payload.decode('utf-8').rstrip('\x00'))

elif choice == "update_password":
    # Simulate booting the device with a new use account
    password = input("Enter your previous password: ").encode('utf-8')
    if not password:
        print("Password cannot be empty.")
        exit(1)
    new_password = input("Enter your new password: ").encode('utf-8')
        
    with open(filename, "rb") as f:
        salt = f.read(16)
        encrypted_dek = f.read(16)
        encrypted_payload = f.read()

    # Calculate IK1
    ik1 = hashlib.scrypt(
        password=password,
        salt=salt,
        n=16384,
        r=8,
        p=1,
        dklen=32
    )

    # Decrypt DEK
    cipher = AES.new(ik1[:16], AES.MODE_CBC, iv=ik1[16:32])
    dek = cipher.decrypt(encrypted_dek)
    print("[*] DEK decrypted successfully:", dek.hex())

    # Derive new key using new password
    ik1_new = hashlib.scrypt(
        password=new_password,
        salt=salt,
        n=16384,
        r=8,
        p=1,
        dklen=32
    ) 

    cipher = AES.new(ik1_new[:16], AES.MODE_CBC, iv=ik1_new[16:32])
    encrypted_dek = cipher.encrypt(dek)
    print("[*] Encrypted DEK with NEW_IK1:", encrypted_dek.hex())

    with open(filename, "wb") as f:
        f.write(salt) # Store the salt
        f.write(encrypted_dek) # Store the encrypted DEK
        f.write(encrypted_payload) # Store the encrypted payload

elif choice == "encrypt":
    # Simulate first time boot of a device
    password = b"default_password"
    salt = secrets.token_bytes(16)
    dek = secrets.token_bytes(16)

    print("[*] Generating salt{" + salt.hex() + "} and DEK{" + dek.hex() + "}")

    # Derive a key using scrypt
    ik1 = hashlib.scrypt(
        password=password,
        salt=salt,
        n=16384,  # CPU/memory cost factor
        r=8,      # Block size
        p=1,      # Parallelization factor
        dklen=32
    )

    print("[*] Derivated key IK1:", ik1.hex())

    cipher = AES.new(ik1[:16], AES.MODE_CBC, iv=ik1[16:32])
    encrypted_dek = cipher.encrypt(dek)
    print("[*] Encrypted DEK with IK1:", encrypted_dek.hex())

    my_payload = input("What is your little secret?")
    cipher2 = AES.new(dek, AES.MODE_CBC, iv=salt)
    encrypted_payload = cipher2.encrypt(my_payload.encode('utf-8') + b'\x00'* ((16 - len(my_payload) % 16) % 16))  # Padding to block size

    print("[*] Payload encrypted successfully:", encrypted_payload.hex())

    with open(filename, "wb") as f:
        f.write(salt) # Store the salt
        f.write(encrypted_dek) # Store the encrypted DEK
        f.write(encrypted_payload) # Store the encrypted payload
