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

        self.cronjobs_sql = 'select created_at,updated_at,name,type,spec_type,spec,script,website,db_name,url,source_dir,exclusion_rules,keep_local,status,container_name from cronjobs;'
        self.cronjobs_name = ['创建时间','修改时间','任务名','类型','计划类型','执行周期','脚本','网站名','数据库','URL','源目录','执行规则','是否保存本地','任务状态','容器名称']

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

        self.settings_sql = 'select key,value from settings'

    def set_db_path(self,path: str) -> None:
        self.db_path = path

    def connect(self) -> None:
        self.conn = DBHelper(self.db_path)

    def get_installed_app(self) -> dict:
        installed_app = self.conn.select(self.installed_app_sql)
        jh = JsonHelper()
        return jh.list2json(self.installed_app_name,installed_app)
    
    def get_backup_records(self) -> dict:
        backup_records = self.conn.select(self.backup_records_sql)
        print(backup_records)
        jh = JsonHelper()
        return jh.list2json(self.backup_records_name,backup_records)
    
    def get_commands(self) -> dict:
        commands = self.conn.select(self.commands_sql)
        jh = JsonHelper()
        return jh.list2json(self.commands_name,commands)
    
    def get_cronjobs(self) -> dict:
        cronjobs = self.conn.select(self.cronjobs_sql)
        jh = JsonHelper()
        return jh.list2json(self.cronjobs_name,cronjobs)
    
    def get_mysql(self) -> dict:
        mysql = self.conn.select(self.mysql_sql)
        jh = JsonHelper()
        return jh.list2json(self.mysql_name,mysql)
    
    def get_database(self) -> dict:
        database = self.conn.select(self.database_sql)
        jh = JsonHelper()
        return jh.list2json(self.database_name,database)
    
    def get_job_records(self) -> dict:
        job_records = self.conn.select(self.job_records_sql)
        jh = JsonHelper()
        return jh.list2json(self.job_records_name,job_records)
    
    def get_login_logs(self) -> dict:
        login_logs = self.conn.select(self.login_logs_sql)
        jh = JsonHelper()
        return jh.list2json(self.login_logs_name,login_logs)
    
    def get_operation_logs(self) -> dict:
        operation_logs = self.conn.select(self.operation_logs_sql)
        jh = JsonHelper()
        return jh.list2json(self.operation_logs_name,operation_logs)
    
    def get_websites(self) -> dict:
        websites = self.conn.select(self.websites_sql)
        jh = JsonHelper()
        return jh.list2json(self.websites_name,websites)
    
    def get_settings(self) -> dict:
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
        self.aes_key = settings[11][1]
        # dec = DecHelper()
        # print(dec.onepanel_password_decrypt(self.aes_key,settings[1][1]))
        # 其他设置待加入
        # dic.update({'':settings[10][1]})
        # dic.update({'':settings[11][1]})
        return dic