# CodeSinaia2025
Examples for CodeSinaia2025

### Full disk encryption example

Prerequisites: Python3 and pip with pycryptodome

Run example:

```
Choose action ? {decrypt | update_password | encrypt}encrypt
[*] Generating salt{efd3742e3259f7f8d4479c0ea4d7d18d} and DEK{70ad0f0ca5ae2c2f5efce8b2fdd9a091}
[*] Derivated key IK1: 85f0bf47b84595c466711fd771f47c52b12834021bedbcefb615f95dd3e2cd8d
[*] Encrypted DEK with IK1: 13e7c6457a7f330cf995393ea786ad0d
What is your little secret?I love icecream
[*] Payload encrypted successfully: d0240d478e171aa8612a745f73395d53
 
Choose action ? {decrypt | update_password | encrypt}update_password
Enter your previous password: default_password
Enter your new password: HardToBreakPassword
[*] DEK decrypted successfully: 70ad0f0ca5ae2c2f5efce8b2fdd9a091
[*] Encrypted DEK with NEW_IK1: d708a415968e3308fa0c720a983d4977

Choose action ? {decrypt | update_password | encrypt}decrypt
Enter your password: HardToBreakPassword
[*] DEK decrypted successfully: 70ad0f0ca5ae2c2f5efce8b2fdd9a091
[*] Payload decrypted successfully: b'I love icecream\x00'
[*] Your secret was: I love icecream
PS C:\Users\sebas\CodeSinaia2025\CodeSinaia2025>
```