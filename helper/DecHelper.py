from Crypto.Cipher import AES
from base64 import b64decode
from Crypto.Util.Padding import unpad
import subprocess
import os

class DecHelper:
    def __init__(self) -> None:
        self.key = ''

    def onepanel_password_decrypt(self,key: str,b64_pwd: str) -> str:
        """
        @key:       解密的密钥
        @b64_pwd:   需要解密的内容，Base64格式
        """
        block_size = 16
        byte_cipher = b64decode(b64_pwd)
        iv = byte_cipher[:block_size]
        cipher_pwd = byte_cipher[block_size:]
        aes = AES.new(key.encode('utf-8'),AES.MODE_CBC,iv)
        decrypted_data = aes.decrypt(cipher_pwd)
        password = unpad(decrypted_data, AES.block_size)
        return password.decode('utf-8')
    
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