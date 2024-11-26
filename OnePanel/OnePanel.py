from helper.DBHelper import DBHelper
from helper.JsonHelper import JsonHelper
from helper.DecHelper import DecHelper

class OnePanel:
    def __init__(self) -> None:
        self.db_path = ''
        self.conn = None
        self.aes_key = ''

        self.installed_app_sql = 'select created_at,updated_at,name,version,param,env,docker_compose,status,description,message,container_name,service_name,http_port,https_port from app_installs;'
        self.installed_app_name = ['创建时间','修改时间','应用名','版本','参数','环境配置','Compose配置','运行状态','描述','消息','容器名称','服务名称','HTTP端口号','HTTPS端口号']

        self.backup_records_sql = 'select created_at,updated_at,name,source,backup_type,file_dir,file_name from backup_records;'
        self.backup_records_name = ['创建时间','修改时间','备份应用','备份源','备份类型','备份目录','备份文件名']

        self.commands_sql = 'select created_at,updated_at,name,command from commands;'
        self.commands_name = ['创建时间','修改时间','名称','命令']

        self.cronjobs_sql = 'select created_at,updated_at,name,type,spec,script,website,db_name,url,source_dir,exclusion_rules,keep_local,status,container_name from cronjobs;'
        self.cronjobs_name = ['创建时间','修改时间','任务名','类型','执行周期','脚本','网站名','数据库','URL','源目录','执行规则','是否保存本地','任务状态','容器名称']

        self.mysql_sql = 'select created_at,updated_at,name,mysql_name,format,username,password,permission from database_mysqls;'
        self.mysql_name = ['创建时间','修改时间','数据库名','类型','字符集','用户名','密码','访问权限']

        self.database_sql = 'select created_at,updated_at,name,type,version,address,port,username,password from databases;'
        self.database_name = ['创建时间','修改时间','数据库名','类型','版本','地址','端口','用户名','密码']

        self.job_records_sql = 'select j.created_at,j.updated_at,cj.name,start_time,file,j.status,message from job_records j left join cronjobs cj on cj.id = j.cronjob_id'
        self.job_records_name = ['创建时间','修改时间','任务名','开始时间','文件','状态','消息']

        self.login_logs_sql = 'select created_at,ip,address,agent,status,message from login_logs'
        self.login_logs_name = ['登录时间','登录IP','登录地址','登录所用UA','状态','消息']

        self.operation_logs_sql = 'select created_at,source,ip,path,user_agent,status,message,detail_zh from operation_logs'
        self.operation_logs_name = ['操作时间','操作内容','IP','请求接口','操作所用UA','状态','消息','操作描述']

        self.websites_sql = 'select created_at,updated_at,protocol,primary_domain,type,alias,remark,status,expire_date,site_dir from websites'
        self.websites_name = ['创建时间','修改时间','协议','主域名','类型','代号','备注','状态','过期时间','网站根目录']

        self.hosts_sql = 'select created_at,updated_at,name,addr,port,user,password from hosts'
        self.hosts_name = ['创建时间','修改时间','连接名','地址','端口','用户名','密码']

        self.settings_sql = 'select key,value from settings'

    def set_path(self,path: dict) -> None:
        self.db_path = path.get('1Panel.db')

    def connect(self) -> None:
        self.conn = DBHelper(self.db_path)
        self.get_settings()

    def close(self) -> None:
        self.conn.close()

    def get_installed_app(self) -> tuple:
        installed_app = self.conn.select(self.installed_app_sql)
        installed_app = [list(t) for t in installed_app]
        return (self.installed_app_name,installed_app)
    
    def get_backup_records(self) -> tuple:
        backup_records = self.conn.select(self.backup_records_sql)
        backup_records = [list(t) for t in backup_records]
        return (self.backup_records_name,backup_records)
    
    def get_commands(self) -> tuple:
        commands = self.conn.select(self.commands_sql)
        commands = [list(t) for t in commands]
        return (self.commands_name,commands)
    
    def get_cronjobs(self) -> tuple:
        cronjobs = self.conn.select(self.cronjobs_sql)
        cronjobs = [list(t) for t in cronjobs]
        return (self.cronjobs_name,cronjobs)
    
    def get_mysql(self) -> tuple:
        mysql = self.conn.select(self.mysql_sql)
        mysql = [list(t) for t in mysql]
        for i in range(len(mysql)):
            mysql[i][6] = self.decrypt(mysql[i][6])
        return (self.mysql_name,mysql)
    
    def get_database(self) -> tuple:
        database = self.conn.select(self.database_sql)
        database = [list(t) for t in database]
        for i in range(len(database)):
            database[i][8] = self.decrypt(database[i][8])
        return (self.database_name,database)
    
    def get_job_records(self) -> tuple:
        job_records = self.conn.select(self.job_records_sql)
        job_records = [list(t) for t in job_records]
        return (self.job_records_name,job_records)
    
    def get_login_logs(self) -> tuple:
        login_logs = self.conn.select(self.login_logs_sql)
        login_logs = [list(t) for t in login_logs]
        return (self.login_logs_name,login_logs)
    
    def get_operation_logs(self) -> tuple:
        operation_logs = self.conn.select(self.operation_logs_sql)
        operation_logs = [list(t) for t in operation_logs]
        return (self.operation_logs_name,operation_logs)
    
    def get_websites(self) -> tuple:
        websites = self.conn.select(self.websites_sql)
        websites = [list(t) for t in websites]
        return (self.websites_name,websites)

    def get_hosts(self) -> tuple:
        hosts = self.conn.select(self.hosts_sql)
        hosts = [list(t) for t in hosts]
        for i in range(len(hosts)):
            hosts[i][6] = self.decrypt(hosts[i][6])
        return (self.hosts_name,hosts)

    
    def decrypt(self,text: str) -> str:
        """
        @text:      待解密的密文
        """
        if text == '':
            return ''
        cipher = DecHelper()
        return cipher.onepanel_password_decrypt(self.aes_key,text)
    
    def get_settings(self) -> tuple:
        settings = self.conn.select(self.settings_sql)
        dic = {}
        dic.update({'用户名':settings[0][1]})
        dic.update({'密码':settings[1][1]})
        dic.update({'邮箱':settings[2][1]})
        dic.update({'面板名称':settings[3][1]})
        dic.update({'超时时间':settings[6][1]})
        dic.update({'端口':settings[8][1]})
        dic.update({'安全入口':settings[9][1]})
        dic.update({'JWT签名密钥':settings[10][1]})
        dic.update({'密码解密密钥':settings[11][1]})
        setting = []
        name = []
        
        self.aes_key = settings[11][1]
        for key in dic.keys():
            name.append(key)
            if key == '密码':
                setting.append(self.decrypt(dic.get(key)))
            else:
                setting.append(dic.get(key))
        # todo其他设置待加入
        return (name,[setting])