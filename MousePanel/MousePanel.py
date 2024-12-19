from helper.DBHelper import DBHelper
from helper.DecHelper import DecHelper
import json
import yaml

class MousePanel:
    def __init__(self) -> None:
        self.db_path = ''
        self.cipher = DecHelper()
        self.key = ''
        self.users_sql = 'select username,password,email,created_at,updated_at,deleted_at from users'
        self.users_name = ['用户名', '密码哈希', '邮箱', '创建时间', '修改时间', '删除时间']
        self.tasks_sql = 'select name,status,shell,log,created_at,updated_at from tasks'
        self.tasks_name = ['任务名', '状态', '命令', '日志文件路径','创建时间','修改时间']
        self.sites_sql = 'select id,name,status,path,https,remark,created_at,updated_at from websites'
        self.sites_name = ['ID','网站名称', '状态', '路径', '是否开启HTTPS', '备注', '创建时间', '修改时间']
        self.databases_sql = 'select id,name,type,host,port,username,password,remark,created_at,updated_at from database_servers'
        self.databases_name = ['ID','数据库名', '类型', '主机', '端口', '用户名','密码', '备注', '创建时间', '修改时间']
        self.dbuser_sql = 'select server_id,username,password,host,remark,created_at,updated_at from database_users'
        self.dbuser_name = ['数据库ID','用户名','密码','主机','备注','创建时间','修改时间']
        self.crontab_sql = 'select name,status,type,time,shell,log,created_at,updated_at from crons'
        self.crontab_name = ['任务名', '状态', '类型', 'cron表达式', '执行文件', '日志文件','创建时间','修改时间']
        self.ssh_sql = 'select name,host,port,config,remark,created_at,updated_at from sshes'
        self.ssh_name = ['连接名', '主机', '端口','认证方式','主机端口','用户名','密码','私钥','备注','创建时间','修改时间']
        self.certs_sql = 'select account_id,website_id,dns_id,type,domains,auto_renew,cert_url,cert,key,created_at,updated_at from certs'
        self.certs_name = ['账户ID','网站ID','DNSID','类型','域名','自动续期','证书地址','证书','密钥','创建时间','修改时间']
        self.cert_accounts_sql = 'select id,email,ca,kid,hmac_encoded,private_key,key_type,created_at,updated_at from cert_accounts'
        self.cert_accounts_name = ['ID','邮箱','CA','KID','HMAC_ENCODED','私钥','私钥类型','创建时间','修改时间']
        self.cert_dns_sql = 'select id,name,type,data,created_at,updated_at from cert_dns'
        self.cert_dns_name = ['ID','名称','类型','配置','创建时间','修改时间']

    def set_path(self, path: dict) -> None:
        """
        @path:      下载下来待分析的文件路径字典
        """
        self.db_path = path.get('app.db')
        self.config_path = path.get('config.yml')
        self.get_key()

    def connect(self) -> None:
        self.conn = DBHelper(self.db_path)

    def close(self) -> None:
        self.conn.close()

    def get_users(self) -> tuple:
        users = self.conn.select(self.users_sql)
        users = [list(t) for t in users]
        return (self.users_name, users)

    def get_tasks(self) -> tuple:
        tasks = self.conn.select(self.tasks_sql)
        tasks = [list(t) for t in tasks]
        return (self.tasks_name, tasks)

    def get_sites(self) -> tuple:
        sites = self.conn.select(self.sites_sql)
        sites = [list(t) for t in sites]
        return (self.sites_name, sites)

    def get_databases(self) -> tuple:
        databases = self.conn.select(self.databases_sql)
        ret = []
        for v in databases:
            tmp = list(v)
            try:
                tmp[6] = self.cipher.XChaCha20Poly1305Decrypt(self.key,tmp[6])
            except:
                pass
            ret.append(tmp)
        return (self.databases_name, ret)

    def get_dbusers(self) -> tuple:
        dbusers = self.conn.select(self.dbuser_sql)
        ret = []
        for v in dbusers:
            tmp = list(v)
            try:
                tmp[2] = self.cipher.XChaCha20Poly1305Decrypt(self.key,tmp[2])
            except:
                pass
            ret.append(tmp)
        return (self.dbuser_name, ret)

    def get_crontab(self) -> tuple:
        crontab = self.conn.select(self.crontab_sql)
        crontab = [list(t) for t in crontab]
        return (self.crontab_name, crontab)

    def get_config(self) -> tuple:
        with open(self.config_path, 'r', encoding='utf-8') as f:
            try:
                configs = []
                names = []
                data = yaml.load(f, Loader=yaml.FullLoader)
                configs.append(data['app']['key'])
                names.append('全局解密密钥')
                configs.append(data['app']['timezone'])
                names.append('时区')
                configs.append(data['app']['root'])
                names.append('安装路径')
                configs.append(data['http']['port'])
                names.append('面板端口')
                configs.append(data['http']['entrance'])
                names.append('面板入口')
                configs.append(data['http']['tls'])
                names.append('开启https')
            except:
                return ('无',[['']])
        return (names, [configs])

    def get_ssh(self) -> tuple:
        ssh = self.conn.select(self.ssh_sql)
        # config字段是json
        ret = []
        for i,v in enumerate(ssh):
            tmp = []
            tmp.extend(v[:3])
            data = json.loads(v[3])
            try:
                tmp.append(data['auth_method'])
                tmp.append(data['host'])
                tmp.append(data['user'])
                tmp.append(self.cipher.XChaCha20Poly1305Decrypt(self.key,data['password']))
                tmp.append(self.cipher.XChaCha20Poly1305Decrypt(self.key,data['key']))
            except:
                self.ssh_name = ['连接名', '主机', '端口', '配置', '备注',
                                 '创建时间', '修改时间']
                tmp.append(v[3])
            tmp.extend(v[4:])
            ret.append(tmp)
        return (self.ssh_name, ret)

    def get_certs(self) -> tuple:
        certs = self.conn.select(self.certs_sql)
        certs = [list(t) for t in certs]
        return (self.certs_name, certs)

    def get_cert_accounts(self) -> tuple:
        cert_accounts = self.conn.select(self.cert_accounts_sql)
        cert_accounts = [list(t) for t in cert_accounts]
        return (self.cert_accounts_name, cert_accounts)

    def get_cert_dns(self) -> tuple:
        cert_dns = self.conn.select(self.cert_dns_sql)
        cert_dns = [list(t) for t in cert_dns]
        return (self.cert_dns_name, cert_dns)

    def get_key(self):
        with open(self.config_path, 'r', encoding='utf-8') as f:
            try:
                data = yaml.load(f, Loader=yaml.FullLoader)
                self.key = data['app']['key']
            except:
                pass