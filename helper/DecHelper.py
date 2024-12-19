from typing import Union
from Crypto.Cipher import AES
from Crypto.Cipher import ChaCha20_Poly1305
from base64 import urlsafe_b64decode
from Crypto.Util.Padding import unpad
import subprocess
import os

class DecHelper:
    def __init__(self) -> None:
        self.key = ''
        self.bt_div = ''

    def onepanel_password_decrypt(self,key: str,b64_pwd: str) -> str:
        """
        @key:       解密的密钥
        @b64_pwd:   需要解密的内容，Base64格式
        """
        block_size = 16
        byte_cipher = urlsafe_b64decode(b64_pwd)
        iv = byte_cipher[:block_size]
        cipher_pwd = byte_cipher[block_size:]
        aes = AES.new(key.encode('utf-8'),AES.MODE_CBC,iv)
        decrypted_data = aes.decrypt(cipher_pwd)
        password = unpad(decrypted_data, AES.block_size)
        return password.decode('utf-8')
    
    def decrypt_bt_div(self,div: str) -> str:
        """
        @div:      需要解密的内容，Base64格式
        """
        key = 'Z2B87NEAS2BkxTrh'
        iv = 'WwadH66EGWpeeTT6'
        byte_div = urlsafe_b64decode(div)
        aes = AES.new(key.encode('utf-8'),AES.MODE_CBC,iv.encode('utf-8'))
        decrypted_data = aes.decrypt(byte_div)
        dec_div = unpad(decrypted_data, AES.block_size)
        self.bt_div = dec_div.decode('utf-8')
        return dec_div.decode('utf-8')
    
    def decrypt_bt(self,bt_str: str) -> str:
        """
        @bt_str:   需要解密的内容，Base64格式
        """
        key = '3P+_lN3+jPW6Kgt#'
        iv = self.bt_div
        byte_bt = urlsafe_b64decode(bt_str)
        aes = AES.new(key.encode('utf-8'),AES.MODE_CBC,iv.encode('utf-8'))
        decrypted_data = aes.decrypt(byte_bt)
        dec_bt = unpad(decrypted_data, AES.block_size)
        return dec_bt.decode('utf-8')

    def decrypt_xp_db(self,path: str) -> int:
        """
        @path:      需要解密的数据库路径
        """
        key = 'xp9080'
        sqlite3 = './lib/sqlite3.exe'
        if os.path.exists(sqlite3) and os.path.isfile(sqlite3):
            sqlite3 = os.path.abspath(sqlite3)
        else:
            print('缺少依赖<sqlite3.exe>！')
            return -1
        work_dir = os.getcwd()
        floder = os.path.realpath(path)
        floder = '\\'.join(floder.split('\\')[:-1])
        os.chdir(floder)
        result = subprocess.run([sqlite3,path,f"PRAGMA key = {key};ATTACH DATABASE 'xp.db' AS xp KEY '';SELECT sqlcipher_export('xp');DETACH DATABASE xp;"],capture_output=True, text=True)
        out = result.stdout
        os.chdir(work_dir)
        if out.strip() == 'ok':
            print('解密成功')
            return 1
        return 0

    def XChaCha20Poly1305Decrypt(self, key, ciphertext) -> Union[str, bytes]:
        nonce_size = 24
        over_head = 16
        cipher_data = urlsafe_b64decode(ciphertext)
        cipher = ChaCha20_Poly1305.new(key=key.encode(), nonce=cipher_data[:nonce_size])
        plain_data = cipher.decrypt(cipher_data[nonce_size:])
        try:
            plain_data = plain_data[:-over_head].decode('utf8')
        except UnicodeDecodeError:
            plain_data = str(plain_data[:-over_head])
        return plain_data