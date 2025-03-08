#Task1
import itertools

# Function to decrypt the message using a particular key (permutation of the alphabet)
def decrypt_with_key(ciphertext, key):
    # Define the alphabet
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    
    # Create a decryption dictionary using the provided key
    decryption_dict = {key[i]: alphabet[i] for i in range(26)}
    
    # Decrypt the ciphertext
    decrypted_message = ''.join([decryption_dict.get(c, c) for c in ciphertext])
    return decrypted_message

# Function to attempt brute-force decryption
def brute_force_monoalphabetic(ciphertext, max_output=5):
    # Define the alphabet
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    
    # Generate all possible permutations of the alphabet
    permutations = itertools.permutations(alphabet)
    
    # Try decrypting the ciphertext with each permutation
    count = 0
    for key in permutations:
        key = ''.join(key)  # Convert the tuple to a string
        decrypted_message = decrypt_with_key(ciphertext, key)
        print(f"Attempt {count+1}: {decrypted_message}")
        count += 1
        
        # Stop after a certain number of outputs (to avoid excessive output)
        if count >= max_output:
            break

# Example usage
if __name__ == "_main_":
    # Encrypted message (all uppercase)
    ciphertext = "YVCCF NFICU"
    
    # Run the brute force decryption
    brute_force_monoalphabetic(ciphertext, max_output=10)

#Task2
from collections import Counter

# Standard English letter frequency (in decreasing order)
ENGLISH_FREQ = "ETAOINSHRDLCUMWFGYPBVKJXQZ"

# Function to perform frequency analysis on the ciphertext
def frequency_analysis(ciphertext):
    # Count the frequency of each letter in the ciphertext
    letter_counts = Counter(ciphertext)
    
    # Sort the letters by frequency (most common first)
    sorted_ciphertext_freq = [pair[0] for pair in letter_counts.most_common()]
    
    # Print frequency analysis results
    print("Ciphertext Letter Frequency (most common first):")
    print(''.join(sorted_ciphertext_freq))
    
    return sorted_ciphertext_freq

# Function to map the most frequent letters in ciphertext to English frequency
def create_decryption_key(ciphertext_freq, english_freq):
    # Map the most frequent ciphertext letters to the most frequent English letters
    decryption_key = {}
    for i in range(len(ciphertext_freq)):
        decryption_key[ciphertext_freq[i]] = english_freq[i]
    
    return decryption_key

# Function to decrypt the ciphertext using the generated decryption key
def decrypt_with_key(ciphertext, decryption_key):
    decrypted_text = ''.join([decryption_key.get(c, c) for c in ciphertext])
    return decrypted_text

# Main cryptanalysis function
def cryptanalysis_monoalphabetic(ciphertext):
    # Step 1: Perform frequency analysis on the ciphertext
    ciphertext_freq = frequency_analysis(ciphertext)
    
    # Step 2: Create a decryption key by mapping ciphertext frequency to English frequency
    decryption_key = create_decryption_key(ciphertext_freq, ENGLISH_FREQ)
    
    # Step 3: Decrypt the ciphertext using the generated key
    decrypted_text = decrypt_with_key(ciphertext, decryption_key)
    
    print("\nDecryption Key (Ciphertext -> English):")
    print(decryption_key)
    
    print("\nDecrypted Text (using frequency analysis):")
    print(decrypted_text)

# Example usage
if __name__ == "_main_":
    # Encrypted message (all uppercase, no spaces or punctuation)
    ciphertext = input("Enter the encrypted text: ").upper().replace(" ", "")
    
    # Perform cryptanalysis using frequency analysis
    cryptanalysis_monoalphabetic(ciphertext)

#Task3
import string

# Function to create the 5x5 Playfair matrix
def create_playfair_matrix(keyword):
    # Remove duplicates and merge 'I' and 'J'
    keyword = ''.join(sorted(set(keyword), key=keyword.index)).upper().replace('J', 'I')
    
    # Create the Playfair matrix
    matrix = []
    alphabet = 'ABCDEFGHIKLMNOPQRSTUVWXYZ'  # 'J' is merged with 'I'
    
    for char in keyword:
        if char not in matrix:
            matrix.append(char)
    
    for char in alphabet:
        if char not in matrix:
            matrix.append(char)
    
    # Convert to 5x5 grid
    matrix_5x5 = [matrix[i:i + 5] for i in range(0, 25, 5)]
    return matrix_5x5

# Function to find position of a character in the Playfair matrix
def find_position(matrix, char):
    for row in range(5):
        for col in range(5):
            if matrix[row][col] == char:
                return row, col
    return None

# Function to process digraphs for encryption/decryption
def process_digraphs(matrix, digraphs, mode='encrypt'):
    result = []
    for digraph in digraphs:
        row1, col1 = find_position(matrix, digraph[0])
        row2, col2 = find_position(matrix, digraph[1])
        
        if row1 == row2:  # Same row: shift right (encrypt) or left (decrypt)
            if mode == 'encrypt':
                result.append(matrix[row1][(col1 + 1) % 5] + matrix[row2][(col2 + 1) % 5])
            else:
                result.append(matrix[row1][(col1 - 1) % 5] + matrix[row2][(col2 - 1) % 5])
        elif col1 == col2:  # Same column: shift down (encrypt) or up (decrypt)
            if mode == 'encrypt':
                result.append(matrix[(row1 + 1) % 5][col1] + matrix[(row2 + 1) % 5][col2])
            else:
                result.append(matrix[(row1 - 1) % 5][col1] + matrix[(row2 - 1) % 5][col2])
        else:  # Rectangle rule: swap columns
            result.append(matrix[row1][col2] + matrix[row2][col1])
    return ''.join(result)

# Function to prepare text for encryption/decryption by creating digraphs
def prepare_text(text):
    text = text.upper().replace('J', 'I').replace(' ', '')
    digraphs = []
    i = 0
    while i < len(text):
        if i + 1 < len(text):
            if text[i] == text[i + 1]:
                digraphs.append(text[i] + 'X')
                i += 1
            else:
                digraphs.append(text[i] + text[i + 1])
                i += 2
        else:
            digraphs.append(text[i] + 'X')
            i += 1
    return digraphs

# Function to display the Playfair matrix
def display_matrix(matrix):
    print("Playfair Cipher 5x5 Matrix:")
    for row in matrix:
        print(' '.join(row))

# Encryption function
def encrypt_playfair(plaintext, matrix):
    digraphs = prepare_text(plaintext)
    return process_digraphs(matrix, digraphs, mode='encrypt')

# Decryption function
def decrypt_playfair(ciphertext, matrix):
    digraphs = prepare_text(ciphertext)
    return process_digraphs(matrix, digraphs, mode='decrypt')

# Main function for the Playfair cipher program
def playfair_cipher():
    print("Welcome to the Playfair Cipher Program!")
    
    # Input the keyword from the user
    keyword = input("Enter the keyword: ").strip()
    
    # Create the Playfair matrix
    matrix = create_playfair_matrix(keyword)
    
    # Display the 5x5 matrix
    display_matrix(matrix)
    
    while True:
        # Ask user for encryption or decryption
        choice = input("\nWould you like to (e)ncrypt, (d)ecrypt, or (q)uit? ").lower()
        if choice == 'e':
            plaintext = input("Enter the plaintext: ").strip()
            ciphertext = encrypt_playfair(plaintext, matrix)
            print(f"Encrypted Text: {ciphertext}")
        elif choice == 'd':
            ciphertext = input("Enter the ciphertext: ").strip()
            plaintext = decrypt_playfair(ciphertext, matrix)
            print(f"Decrypted Text: {plaintext}")
        elif choice == 'q':
            print("Exiting the Playfair Cipher Program. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 'e' for encrypt, 'd' for decrypt, or 'q' to quit.")

# Run the program
if __name__ == "_main_":
    playfair_cipher()