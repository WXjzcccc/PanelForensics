from helper.DBHelper import DBHelper
import json
import ast

class BTPanel:
    def __init__(self) -> None:
        self.db_path = ''

        self.users_sql = 'select username,password,login_ip,login_time,email,salt from users'
        self.users_name = ['用户名','密码','登录IP','登录时间','邮箱','盐值']
        self.tasks_sql = 'select name,type,addtime,execstr from tasks'
        self.tasks_name = ['任务名','类型','添加时间','内容']
        self.sites_sql = 'select s.name,path,ps,s.addtime,d.name,d.port from sites s left join domain d on d.pid = s.id'
        self.sites_name = ['网站名称','路径','备注','添加时间','域名','端口']
        self.logs_sql = 'select type,log,addtime,username from logs'
        self.logs_name = ['类型','详情','操作时间','操作人']
        self.ftps_sql = 'select name,password,path,ps,addtime from ftps'
        self.ftps_name = ['用户名','密码','路径','备注','添加时间']
        self.firewall_sql = 'select port,ps,addtime from firewall'
        self.firewall_name = ['端口','备注','添加时间']
        self.databases_sql = 'select name,username,password,accept,ps,addtime from databases'
        self.databases_name = ['数据库名','用户名','密码','访问权限','备注','添加时间']
        self.crontab_sql = 'select name,type,where1,where_hour,where_minute,echo,addtime,backupTo,sBody,sType,urladdress from crontab'
        self.crontab_name = ['任务名','周期','条件1','时','分','执行文件','添加时间','备份至','执行内容','任务类型','请求URL']
        self.config_sql = 'select webserver,backup_path,sites_path,mysql_root from config'
        self.config_name = ['WEB容器','备份路径','网站路径','MySQL管理员密码']
        self.backup_sql = 'select name1,filename,addtime,ps from backup'
        self.backup_name = ['文件名','文件路径','备份时间','备注']

    def set_path(self,path: dict) -> None:
        """
        @path:      下载下来待分析的文件路径字典
        """
        self.db_path = path.get('default.db')
        self.admin_path = path.get('admin_path.pl')
        self.default_path = path.get('default.pl')
        self.port_path = path.get('port.pl')
        self.user_path = path.get('userInfo.json')
        self.history_path = []
        for key in path:
            if key.endswith('_history.pl'):
                self.history_path.append(path.get(key))
        self.limitip_path = ''
        self.basic_auth_path = ''
        if 'limitip.conf' in path.keys():
            self.limitip_path = path.get('limitip.conf')
        if 'basic_auth.json' in path.keys():
            self.basic_auth_path = path.get('basic_auth.json')

    def connect(self) -> None:
        self.conn = DBHelper(self.db_path)

    def close(self) -> None:
        self.conn.close()

    def get_users(self) -> tuple:
        users = self.conn.select(self.users_sql)
        users = [list(t) for t in users]
        return (self.users_name,users)

    def get_tasks(self) -> tuple:
        tasks = self.conn.select(self.tasks_sql)
        tasks = [list(t) for t in tasks]
        return (self.tasks_name,tasks)

    def get_history(self) -> tuple:
        import datetime
        history = []
        for history_path in self.history_path:
            with open(history_path,'r',encoding='utf-8') as f:
                data = f.readlines()
                for line in data:
                    t = ast.literal_eval(line.strip())
                    t.extend([history_path.split('\\')[-1].split('_')[0]])
                    t[0] = datetime.datetime.fromtimestamp(int(t[0])).strftime("%Y-%m-%d %H:%M:%S")
                    history.append(t)
        return (['时间', '本地IP', '用户', '命令', '连接IP'],history)

    def get_sites(self) -> tuple:
        sites = self.conn.select(self.sites_sql)
        sites = [list(t) for t in sites]
        return (self.sites_name,sites)
    
    def get_logs(self) -> tuple:
        logs = self.conn.select(self.logs_sql)
        logs = [list(t) for t in logs]
        return (self.logs_name,logs)
    
    def get_ftps(self) -> tuple:
        ftps = self.conn.select(self.ftps_sql)
        ftps = [list(t) for t in ftps]
        return (self.ftps_name,ftps)
    
    def get_firewall(self) -> tuple:
        firewall = self.conn.select(self.firewall_sql)
        firewall = [list(t) for t in firewall]
        return (self.firewall_name,firewall)
    
    def get_databases(self) -> tuple:
        databases = self.conn.select(self.databases_sql)
        databases = [list(t) for t in databases]
        return (self.databases_name,databases)
    
    def get_crontab(self) -> tuple:
        crontab = self.conn.select(self.crontab_sql)
        crontab = [list(t) for t in crontab]
        return (self.crontab_name,crontab)
    
    def get_config(self) -> tuple:
        config = self.conn.select(self.config_sql)
        config = [list(t) for t in config]
        return (self.config_name,config)
    
    def get_backup(self) -> tuple:
        backup = self.conn.select(self.backup_sql)
        backup = [list(t) for t in backup]
        return (self.backup_name,backup)

    def get_settings(self) -> tuple:
        settings = []
        name = []
        with open(self.admin_path,'r') as fr:
            try:
                settings.append(fr.read().strip())
                name.append('安全入口')
            except:
                settings.append('admin_path.pl提取异常')
                name.append('Warning')
        with open(self.default_path,'r') as fr:
            try:
                settings.append(fr.read().strip())
                name.append('默认密码')
            except:
                settings.append('default.pl提取异常')
                name.append('Warning')
        with open(self.limitip_path,'r') as fr:
            try:
                settings.append(fr.read().strip())
                name.append('限制IP')
            except:
                settings.append('limitip.conf提取异常')
                name.append('Warning')
        with open(self.port_path,'r') as fr:
            try:
                settings.append(fr.read().strip())
                name.append('访问端口')
            except:
                settings.append('port.pl提取异常')
                name.append('Warning')
        with open(self.basic_auth_path,'r') as fr:
            try:
                data = json.load(fr)
                settings.append(data['basic_user'])
                name.append('basic_auth用户名')
                settings.append(data['basic_pwd'])
                name.append('basic_auth密码')
                settings.append(data['open'])
                name.append('basic_auth开关')
            except:
                settings.append('basic_auth文件不存在')
                name.append('Warning')
        with open(self.user_path,'r') as fr:
            try:
                data = json.load(fr)
                settings.append(data['uid'])
                name.append('用户ID')
                settings.append(data['address'])
                name.append('IP地址')
                settings.append(data['access_key'])
                name.append('access_key')
                settings.append(data['secret_key'])
                name.append('secret_key')
                settings.append(data['addtime'])
                name.append('添加时间')
                settings.append(data['username'])
                name.append('用户名')
                settings.append(data['idc_code'])
                name.append('idc_code')
                settings.append(data['ukey'])
                name.append('ukey')
                settings.append(data['serverid'])
                name.append('serverid')
            except:
                settings.append('userInfo提取异常')
                name.append('Warning')
        return (name,[settings])
