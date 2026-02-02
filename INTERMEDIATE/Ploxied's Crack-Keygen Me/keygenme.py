def keygen(username: str) -> str:
    if len(username) > 8:
        raise ValueError("Username must be <= 8 characters")

    # XOR with 0x0D
    xored = bytes([ord(c) ^ 0x0D for c in username])

    # Reverse
    reversed_bytes = xored[::-1]

    # Hex encode (uppercase)
    password = ''.join(f"{b:02X}" for b in reversed_bytes)

    return password


if __name__ == "__main__":
    user = input("Username: ")
    print("Password:", keygen(user))
