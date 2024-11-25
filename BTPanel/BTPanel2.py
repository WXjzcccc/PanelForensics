from helper.DBHelper import DBHelper
from helper.DecHelper import DecHelper
import json
import datetime
import ast

class BTPanel2:
    def __init__(self) -> None:
        self.cipher = DecHelper()
        self.backup_db = ''
        self.client_db = ''
        self.crontab_db = ''
        self.database_db = ''
        self.default_db = ''
        self.docker_db = ''
        self.firewall_db = ''
        self.ftp_db = ''
        self.log_db = ''
        self.panel_db = ''
        self.site_db = ''
        self.task_db = ''
        self.users_sql = 'select username,password,login_ip,login_time,email,salt from users'
        self.users_sql2 = 'select username,password,login_ip,login_time,email from users'
        self.users_name = ['用户名','密码','登录IP','登录时间','邮箱','盐值']
        self.tasks_sql = 'select name,type,addtime,datetime(start,"unixepoch"),datetime(end,"unixepoch"),execstr from tasks'
        self.tasks_name = ['任务名','类型','添加时间','开始时间(UTC0)','结束时间(UTC0)','内容']
        self.sites_sql = 'select s.name,path,ps,s.addtime,d.name,d.port from sites s left join domain d on d.pid = s.id'
        self.sites_name = ['网站名称','路径','备注','添加时间','域名','端口']
        self.logs_sql = 'select type,log,addtime,username from logs'
        self.logs_name = ['类型','详情','操作时间','操作人']
        self.ftps_sql = 'select name,password,path,ps,addtime from ftps'
        self.ftps_name = ['用户名','密码','路径','备注','添加时间']
        self.firewall_sql = 'select port,ps,addtime from firewall'
        self.firewall_name = ['端口','备注','添加时间']
        self.firewall_trans_sql = 'select start_port,ended_ip,ended_port,protocol,addtime from firewall_trans'
        self.firewall_trans_name = ['起始端口','目标IP','目标端口','协议','添加时间']
        self.firewall_ip_sql = 'select types,address,brief,addtime from firewall_ip'
        self.firewall_ip_name = ['类型','地址','备注','添加时间']
        self.databases_sql = 'select name,username,password,accept,ps,addtime,type from databases'
        self.databases_name = ['数据库名','用户名','密码','访问权限','备注','添加时间','类型']
        self.databases_sql2 = 'select db_host,db_port,db_user,db_password,ps,datetime(addtime,"unixepoch"),type from database_servers'
        self.databases_name2 = ['数据库地址','端口','用户名','密码','备注','添加时间(UTC0)','类型']
        self.crontab_sql = 'select name,type,where1,where_hour,where_minute,echo,addtime,backupTo,sBody,sType,urladdress from crontab'
        self.crontab_name = ['任务名','周期','条件1','时','分','执行文件','添加时间','备份至','执行内容','任务类型','请求URL']
        self.config_sql = 'select webserver,backup_path,sites_path,mysql_root from config'
        self.config_name = ['WEB容器','备份路径','网站路径','MySQL管理员密码']
        self.backup_sql = 'select type,name,filename,size,addtime,ps,cron_id from backup'
        self.backup_name = ['类型','名称','文件路径','文件大小','备份时间','备注','定时任务ID']

    def set_path(self,path: dict) -> None:
        """
        @path:      下载下来待分析的文件路径字典
        """
        self.backup_db = path.get('backup.db')
        self.client_db = path.get('client_info.db')
        self.crontab_db = path.get('crontab.db')
        self.database_db = path.get('database.db')
        self.default_db = path.get('default.db')
        self.docker_db = path.get('docker.db')
        self.firewall_db = path.get('firewall.db')
        self.ftp_db = path.get('ftp.db')
        self.log_db = path.get('log.db')
        self.panel_db = path.get('panel.db')
        self.site_db = path.get('site.db')
        self.task_db = path.get('task.db')
        self.admin_path = path.get('admin_path.pl')
        self.default_path = path.get('default.pl')
        self.history_path = []
        for key in path:
            if key.endswith('_history.pl'):
                self.history_path.append(path.get(key))
        self.port_path = path.get('port.pl')
        self.user_path = path.get('userInfo.json')
        self.limitip_path = ''
        self.basic_auth_path = ''
        self.memo_path = ''
        self.title_path = path.get('title.pl')
        if 'memo.txt' in path.keys():
            self.memo_path = path.get('memo.txt')
        if 'limitip.conf' in path.keys():
            self.limitip_path = path.get('limitip.conf')
        if 'basic_auth.json' in path.keys():
            self.basic_auth_path = path.get('basic_auth.json')

    def connect(self,db: str) -> DBHelper:
        conn = DBHelper(db)
        return conn

    def decrypt(self,data: tuple) -> tuple:
        lst = data[1]
        print(lst)
        for i in range(len(lst)):
            for j in range(len(lst[i])):
                if str(lst[i][j]).startswith('BT-0x:'):
                    enc_data = lst[i][j].split('BT-0x:')[1]
                    dec_data = self.cipher.decrypt_bt(enc_data)
                    lst[i][j] = dec_data
        return (data[0],lst)

    def get_users(self) -> tuple:
        conn = DBHelper(self.panel_db)
        users = conn.select(self.users_sql)
        users = [list(t) for t in users]
        conn.close()
        conn = DBHelper(self.default_db)
        tmp = conn.select(self.users_sql2)
        # tmp = [list(t).append('') for t in tmp]
        tmp2 = []
        for t in tmp:
            _ = list(t)
            _.append("")
            tmp2.append(_)
        users.extend(tmp2)
        conn.close()
        return (self.users_name,users)

    def get_tasks(self) -> tuple:
        conn = DBHelper(self.task_db)
        tasks = conn.select(self.tasks_sql)
        tasks = [list(t) for t in tasks]
        conn.close()
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
        conn = DBHelper(self.site_db)
        sites = conn.select(self.sites_sql)
        sites = [list(t) for t in sites]
        conn.close()
        return (self.sites_name,sites)
    
    def get_logs(self) -> tuple:
        conn = DBHelper(self.log_db)
        logs = conn.select(self.logs_sql)
        logs = [list(t) for t in logs]
        conn.close()
        return (self.logs_name,logs)
    
    def get_ftps(self) -> tuple:
        conn = DBHelper(self.ftp_db)
        ftps = conn.select(self.ftps_sql)
        ftps = [list(t) for t in ftps]
        conn.close()
        return (self.ftps_name,ftps)
    
    def get_firewall(self) -> tuple:
        conn = DBHelper(self.firewall_db)
        firewall = conn.select(self.firewall_sql)
        firewall = [list(t) for t in firewall]
        conn.close()
        return (self.firewall_name,firewall)
    
    def get_firewall_trans(self) -> tuple:
        conn = DBHelper(self.firewall_db)
        firewall = conn.select(self.firewall_trans_sql)
        firewall = [list(t) for t in firewall]
        conn.close()
        return (self.firewall_trans_name,firewall)
    
    def get_firewall_ip(self) -> tuple:
        conn = DBHelper(self.firewall_db)
        firewall = conn.select(self.firewall_ip_sql)
        firewall = [list(t) for t in firewall]
        conn.close()
        return (self.firewall_ip_name,firewall)
    
    def get_databases(self) -> tuple:
        conn = DBHelper(self.database_db)
        databases = conn.select(self.databases_sql)
        databases = [list(t) for t in databases]
        conn.close()
        return (self.databases_name,databases)
    
    def get_databases_server(self) -> tuple:
        conn = DBHelper(self.database_db)
        databases = conn.select(self.databases_sql2)
        databases = [list(t) for t in databases]
        conn.close()
        return (self.databases_name2,databases)
    
    def get_crontab(self) -> tuple:
        conn = DBHelper(self.crontab_db)
        crontab = conn.select(self.crontab_sql)
        crontab = [list(t) for t in crontab]
        conn.close()
        return (self.crontab_name,crontab)
    
    def get_config(self) -> tuple:
        conn = DBHelper(self.panel_db)
        config = conn.select(self.config_sql)
        config = [list(t) for t in config]
        conn.close()
        return (self.config_name,config)
    
    def get_backup(self) -> tuple:
        conn = DBHelper(self.backup_db)
        backup = conn.select(self.backup_sql)
        backup = [list(t) for t in backup]
        conn.close()
        return (self.backup_name,backup)

    def get_div(self) -> str:
        conn = self.connect(self.default_db)
        sql = 'select div from div_list'
        div = conn.select(sql)[0][0]
        # 解密div
        self.cipher.decrypt_bt_div(div)
        conn.close()
        return div

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
        with open(self.title_path,'r',encoding='utf8') as fr:
            try:
                settings.append(fr.read().strip())
                name.append('网站标题')
            except:
                settings.append('title.pl提取异常')
                name.append('Warning')
        with open(self.memo_path,'r',encoding='utf8') as fr:
            try:
                settings.append(fr.read().strip())
                name.append('备忘录')
            except:
                settings.append('memo.txt提取异常')
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
                settings.append(str(datetime.datetime.fromtimestamp(data['addtime'])))
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
