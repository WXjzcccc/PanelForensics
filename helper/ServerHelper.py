import paramiko
import os
import time

class ServerHelper:
    def __init__(self,host: str,port: int,username: str,password: str) -> None:
        self.username = username
        self.host = host
        self.port = port
        self.password = password
        self.client = paramiko.SSHClient()

    def connect(self) -> None:
        try:
            self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.client.connect(self.host, self.port, self.username, self.password)
        except Exception as e:
            print(f'SSH 连接错误！{e}')
            self.client = None

    def close(self) -> None:
        self.client.close()

    def exec_command(self,command: str) -> str:
        """
        @command:       要执行的命令
        """
        stdin, stdout, stderr = self.client.exec_command(command)
        return stdout.read().decode().strip()

    def get_file(self,remote_file: str,local_path: str) -> str:
        """
        @remote_file:       服务器上的文件绝对路径
        @local_path:        下载下来的文件路径
        """
        sftp = self.client.open_sftp()
        floder = '/'.join(local_path.split('/')[:-1])
        if not os.path.exists(floder):
            os.mkdir(floder)
        try:
            sftp.get(remote_file,local_path)
        except Exception as e:
            open(local_path,'w').write('')
        sftp.close()
        return os.path.abspath(local_path)

    def detect_bt(self) -> bool:
        cmd1 = 'test -d /www/server/panel && echo "目录存在" || echo "目录不存在"'
        cmd2 = 'test -f /usr/bin/bt && echo "文件存在" || echo "文件不存在"'
        out1 = self.exec_command(cmd1)
        out2 = self.exec_command(cmd2)
        if out1 == '目录存在' and out2 == '文件存在':
            return True
        return False

    def detect_one(self) -> bool:
        cmd1 = 'test -f /usr/bin/1panel && echo "文件存在" || echo "文件不存在"'
        cmd2 = 'test -f /usr/bin/1pctl && echo "文件存在" || echo "文件不存在"'
        out1 = self.exec_command(cmd1)
        out2 = self.exec_command(cmd2)
        if out1 == '文件存在' and out2 == '文件存在':
            return True
        return False
    
    def detect_xp(self) -> bool:
        cmd1 = 'test -f /usr/bin/xp && echo "文件存在" || echo "文件不存在"'
        cmd2 = 'test -f /usr/local/phpstudy/system/phpstudy && echo "文件存在" || echo "文件不存在"'
        out1 = self.exec_command(cmd1)
        out2 = self.exec_command(cmd2)
        if out1 == '文件存在' and out2 == '文件存在':
            return True
        return False

    def detect_panel(self) -> str:
        if self.client == None:
            return '连接失败'
        if self.detect_bt():
            return 'bt'
        if self.detect_one():
            return 'one'
        if self.detect_xp():
            return 'xp'
        return '未找到任何面板'
    
    def download_bt(self) -> dict:
        date = int(time.time())
        target_path = f'./tmp/BTPanel/{date}/'
        dic = {}
        dic.update({'default.db':self.get_file('/www/server/panel/data/default.db',f'{target_path}default.db')})
        dic.update({'default.pl':self.get_file('/www/server/panel/default.pl',f'{target_path}default.pl')})
        dic.update({'admin_path.pl':self.get_file('/www/server/panel/data/admin_path.pl',f'{target_path}admin_path.pl')})
        dic.update({'port.pl':self.get_file('/www/server/panel/data/port.pl',f'{target_path}port.pl')})
        dic.update({'userInfo.json':self.get_file('/www/server/panel/data/userInfo.json',f'{target_path}userInfo.json')})
        dic.update({'limitip.conf':self.get_file('/www/server/panel/data/limitip.conf',f'{target_path}limitip.conf')})
        dic.update({'basic_auth.json':self.get_file('/www/server/panel/config/basic_auth.json',f'{target_path}basic_auth.json')})
        return dic

    def download_one(self) -> dict:
        date = int(time.time())
        target_path = f'./tmp/OnePanel/{date}/'
        dic = {}
        try:
            dic.update({'1Panel.db':self.get_file('/opt/1panel/db/1Panel.db',f'{target_path}1Panel.db')})
            dic.update({'1Panel.db-shm':self.get_file('/opt/1panel/db/1Panel.db-shm',f'{target_path}1Panel.db-shm')})
            dic.update({'1Panel.db-wal':self.get_file('/opt/1panel/db/1Panel.db-wal',f'{target_path}1Panel.db-wal')})
        except:
            pass
        return dic
    
    def download_xp(self) -> dict:
        date = int(time.time())
        target_path = f'./tmp/XPanel/{date}/'
        dic = {}
        try:
            dic.update({'encdb':self.get_file('/usr/local/phpstudy/system/depends/libc.so.1.0.1',f'{target_path}libc.so.1.0.1')})
            dic.update({'install.result':self.get_file('/usr/local/phpstudy/install.result',f'{target_path}install.result')})
            dic.update({'decdb':f'{target_path}xp.db'})
        except:
            pass
        return dic