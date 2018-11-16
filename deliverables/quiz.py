from cryptography.fernet import Fernet

key = 'TluxwB3fV_GWuLkR1_BzGs1Zk90TYAuhNMZP_0q4WyM='

# Oh no! The code is going over the edge! What are you going to do?
message = b'gAAAAABb6ea30CsXNK-_10FB_cAyyzdaE1eY8b957HDuDQYLD6v6O2d0jMGbxy27RC_F9VFF0wLHCWThIkrLqCSDs8K7YDv2PYr6k4vjatctmy_ZnyobZAEhMet0hQEKv894jX1Bo4vlSWJA6hf2fLkYGj-dq7Xmx75xTz7z1_vrKx20Sxil62c='

def main():
    f = Fernet(key)
    print(f.decrypt(message))


if __name__ == "__main__":
    main()
