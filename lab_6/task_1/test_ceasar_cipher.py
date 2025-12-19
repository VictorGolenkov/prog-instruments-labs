# test_ceasar_cipher.py
import ceasar_cipher


class TestCaesarCipher:
    
    def test_caesar_encrypt_basic(self):
        result = ceasar_cipher.caesar_encrypt("hello", 3, "abcdefghijklmnopqrstuvwxyz")
        assert result == "khoor"
    
    def test_caesar_encrypt_with_uppercase(self):
        result = ceasar_cipher.caesar_encrypt("Hello World", 3, "abcdefghijklmnopqrstuvwxyz")
        assert result == "Khoor Zruog"
    
    def test_caesar_encrypt_decrypt_symmetry(self):
        original = "Test Message"
        key = 7
        alphabet = "abcdefghijklmnopqrstuvwxyz"
        
        encrypted = ceasar_cipher.caesar_encrypt(original, key, alphabet)
        decrypted = ceasar_cipher.ceasar_decrypt(encrypted, key, alphabet)
        
        assert decrypted == original