# Morse code dictionary for letters and digits
MORSE_CODE_DICT = {
    'A': '01', 'B': '1000', 'C': '1010', 'D': '100', 'E': '0', 'F': '0010',
    'G': '110', 'H': '0000', 'I': '00', 'J': '0111', 'K': '101', 'L': '0100',
    'M': '11', 'N': '10', 'O': '111', 'P': '0110', 'Q': '1101', 'R': '010',
    'S': '000', 'T': '1', 'U': '001', 'V': '0001', 'W': '011', 'X': '1001',
    'Y': '1011', 'Z': '1100', '0': '11111', '1': '01111', '2': '00111',
    '3': '00011', '4': '00001', '5': '00000', '6': '10000', '7': '11000',
    '8': '11100', '9': '11110'
}

# Reverse Morse code dictionary for decryption
REVERSE_MORSE_CODE_DICT = {v: k for k, v in MORSE_CODE_DICT.items()}

# Convert text to Morse code binary
def text_to_morse(text):
    morse_binary = []
    for letter in text.upper():
        if letter in MORSE_CODE_DICT:
            morse_binary.append(MORSE_CODE_DICT[letter])
    return '2'.join(morse_binary)  # Use '2' as separator between Morse characters

# Convert Morse code back to text
def morse_to_text(morse_code):
    letters = morse_code.split('2')  # Split by '2' (letter separator)
    plain_text = []

    for letter in letters:
        if letter in REVERSE_MORSE_CODE_DICT:
            plain_text.append(REVERSE_MORSE_CODE_DICT[letter])

    return ''.join(plain_text)

# Helper function to convert a base 10 integer to a base 3 string
def base_convert(number, base):
    if number == 0:
        return "0"
    digits = []
    while number:
        digits.append(int(number % base))
        number //= base
    return ''.join(str(x) for x in digits[::-1])

# Function to convert base 3 string to base 16 string
def base3_to_base16(base3_str):
    # Convert base 3 string to base 10 integer
    base10_int = int(base3_str, 3)
    # Convert base 10 integer to base 16 (hex) string
    return hex(base10_int)[2:]  # Remove the '0x' prefix

# Function to convert base 16 string back to base 3 string
def base16_to_base3(base16_str):
    # Convert base 16 (hex) string to base 10 integer
    base10_int = int(base16_str, 16)
    # Convert base 10 integer back to base 3 string
    return base_convert(base10_int, 3)

# Vigenère cipher encryption (mod 3) for Morse code
def vigenere_cipher(morse_text, morse_key):
    encrypted = []
    key_len = len(morse_key)
    
    key_index = 0
    for i, char in enumerate(morse_text):
        text_val = int(char)  # Convert the current character (0, 1, or 2) to an integer
        key_val = int(morse_key[key_index % key_len])  # Get the key value (mod key length)
        result = (text_val + key_val) % 3  # Add mod 3
        encrypted.append(str(result))  # Append the resulting value (0, 1, or 2)
        key_index += 1  # Increment the key index for the next character
    
    return ''.join(encrypted)

# Vigenère cipher decryption (mod 3) for Morse code
def vigenere_decipher(encrypted_text, morse_key):
    decrypted = []
    key_len = len(morse_key)
    
    key_index = 0
    for i, char in enumerate(encrypted_text):
        enc_val = int(char)  # Convert the current character (0, 1, or 2) to an integer
        key_val = int(morse_key[key_index % key_len])  # Get the key value (mod key length)
        result = (enc_val - key_val + 3) % 3  # Subtract mod 3 (ensuring non-negative result)
        decrypted.append(str(result))  # Append the resulting value (0, 1, or 2)
        key_index += 1  # Increment the key index for the next character

    return ''.join(decrypted)

# Encrypt function (combining Morse code + Vigenère)
def encrypt(plaintext, key):
    morse_text = text_to_morse(plaintext)  # Convert plaintext to Morse code
    morse_key = text_to_morse(key).replace('2', '')  # Convert key to Morse code, remove separators
    encrypted_text = vigenere_cipher(morse_text, morse_key)  # Encrypt Morse code with Vigenère cipher
    # Convert the base 3 ciphertext to base 16 for compression
    compressed_ciphertext = base3_to_base16(encrypted_text)
    
    return compressed_ciphertext

# Decrypt function (combining Vigenère + Morse code)
def decrypt(encrypted_message, key):
    base3_ciphertext = base16_to_base3(encrypted_message)
    morse_key = text_to_morse(key).replace('2', '')  # Convert key to Morse code, remove separators
    decrypted_morse = vigenere_decipher(base3_ciphertext, morse_key)  # Decrypt Morse code with Vigenère cipher
    decrypted_text = morse_to_text(decrypted_morse)  # Convert Morse code back to plain text
    return decrypted_text

plaintext = "Our company is facing financial instability due to mismanagement by senior executives. Over the past year, they’ve diverted funds from key projects into personal accounts, leaving us unable to meet operational costs. R&D has been underfunded, delaying critical product launches. Additionally, safety violations have been covered up to avoid regulatory scrutiny, which could result in major fines. We need to act immediately to prevent this from becoming public, as it could severely damage our reputation and future."

key = "SABROSA"
key = 'T' + key #Fixes edge case of leading zero since T maps to 1 in morse code
encrypted_message = encrypt(plaintext, key)
decrypted_message = decrypt(encrypted_message, key)

print("Original message: ", plaintext)
print("Encrypted message: ", encrypted_message)
print("Decrypted message: ",  decrypted_message)
