def get_binary(number: int) -> str:
    return bin(number)[2:]

def get_int(binary: str) -> int:
    return int(binary, 2)