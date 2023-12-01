from helper.DBHelper import DBHelper
from helper.DecHelper import DecHelper

class XpPanel:
    def __init__(self) -> None:
        self.db_path = ''
        self.conn = None

        self.accept_port_sql = 'select PORT,TIME,REMARK from ACCEPTPORT'
        self.accept_port_name = ['端口','添加时间','备注']
        self.admins_sql = 'select USERNAME,ALIAS,PASSWORD,REALNAME,ADD_TIME,AGREEMENT from ADMINS'
        self.admins_name = ['用户名','别名','密码','昵称','添加事件','允许登录']
        self.deny_ip_sql = 'select IP,TIME,REMARK from DENYIP'
        self.deny_ip_name = ['IP','添加时间','备注']
        self.ftp_account_sql = 'select FTPUSER,FTPPWD,FTPROOT,FTPSTATUS,REMARK from FTPACCOUNT'
        self.ftp_account_name = ['用户名','密码','目录','状态','备注']
        self.mysql_account_sql = 'select DBVER,USER,PASS,PRIVILEGE from MYSQLACCOUNT'
        self.mysql_account_name = ['版本','用户名','密码','权限']
        self.mysql_backup_info_sql = 'select DBID,BACKUPFILE,BACKUPTIME,BACKUPSIZE from MYSQLBACKUPINFO'
        self.mysql_backup_info_name = ['数据库ID','备份文件','备份时间','备份大小']
        self.mysql_db_info_sql = 'select DBNAME,DBVER,DBUSER,DBCHARACTER from MYSQLDBINFO'
        self.mysql_db_info_name = ['数据库','版本','用户名','角色']
        self.mysql_upload_file_sql = 'select DBID,FILENAME,FILEPATH,UPLOADTIME,FILESIZE from MYSQLUPLOADFILE'
        self.mysql_upload_file_name = ['数据库ID','文件名','文件路径','上传时间','文件大小']
        self.operlog_sql = 'select TYPE,DETAIL,TIME from OPERLOG'
        self.operlog_name = ['类型','操作详情','操作时间']
        self.recycle_sql = 'select SRC,DEST,TIME from RECYCLE'
        self.recycle_name = ['原路径','目标路径','删除时间']
        self.server_info_sql = 'select ADDRESS,USER,PWD,ADDTIME,REMARK from SERVERINFO'
        self.server_info_name = ['地址','用户名','密码','添加时间','备注']
        self.syscfg_sql = 'select PARANAME,PARAVALUE,REMARK from SYSCFG'
        self.syscfg_name = ['参数','值','备注']
        self.taskmng_sql = 'select TITLE,TYPE,CYCLE,TIME,ADDTIME,SHELL,SITES,TASK_TYPE,DBS from TASKMNG'
        self.taskmng_name = ['任务名','类型','周期','时间','添加时间','SHELL指令','网站','任务类型','DBS']
        self.task_runlog_sql = 'select m.TITLE,RESULT,r.TIME,AUTO from TASKRUNLOG r left join TASKMNG m on r.TASKID = m.ID'
        self.task_runlog_name = ['任务名','执行结果','执行时间','自动执行']
        self.urlmng_sql = 'select URL,PORT from URLMNG'
        self.urlmng_name = ['URL','端口']
        self.website_sql = 'select PORT,DOCUMENTROOT,EXECROOT,SERVERNAME,PHPVER,REMARK,RULE_PATH,WAF_LOG_DIR,LOG_PATH from WEBSITE'
        self.website_name = ['端口','根目录','运行目录','网站名','PHP版本','备注','规则文件','WAF日志','访问日志']

    def set_path(self,path: dict) -> None:
        self.db_path = path.get('encdb')
        dec = DecHelper()
        if dec.decrypt_xp_db(self.db_path) == 1:
            self.db_path = path.get('decdb')
        self.install_path = path.get('install.result')

    def connect(self) -> None:
        self.conn = DBHelper(self.db_path)

    def close(self) -> None:
        self.conn.close()

    def get_website(self) -> tuple:
        website = self.conn.select(self.website_sql)
        website = [list(t) for t in website]
        return (self.website_name,website)

    def get_urlmng(self) -> tuple:
        urlmng = self.conn.select(self.urlmng_sql)
        urlmng = [list(t) for t in urlmng]
        return (self.urlmng_name,urlmng)

    def get_task_runlog(self) -> tuple:
        task_runlog = self.conn.select(self.task_runlog_sql)
        task_runlog = [list(t) for t in task_runlog]
        return (self.task_runlog_name,task_runlog)

    def get_taskmng(self) -> tuple:
        taskmng = self.conn.select(self.taskmng_sql)
        taskmng = [list(t) for t in taskmng]
        return (self.taskmng_name,taskmng)

    def get_syscfg(self) -> tuple:
        syscfg = self.conn.select(self.syscfg_sql)
        syscfg = [list(t) for t in syscfg]
        return (self.syscfg_name,syscfg)

    def get_server_info(self) -> tuple:
        server_info = self.conn.select(self.server_info_sql)
        server_info = [list(t) for t in server_info]
        return (self.server_info_name,server_info)

    def get_recycle(self) -> tuple:
        recycle = self.conn.select(self.recycle_sql)
        recycle = [list(t) for t in recycle]
        return (self.recycle_name,recycle)

    def get_operlog(self) -> tuple:
        operlog = self.conn.select(self.operlog_sql)
        operlog = [list(t) for t in operlog]
        return (self.operlog_name,operlog)

    def get_accept_port(self) -> tuple:
        accept_port = self.conn.select(self.accept_port_sql)
        accept_port = [list(t) for t in accept_port]
        return (self.accept_port_name,accept_port)
    
    def get_admins(self) -> tuple:
        admins = self.conn.select(self.admins_sql)
        admins = [list(t) for t in admins]
        return (self.admins_name,admins)
    
    def get_deny_ip(self) -> tuple:
        deny_ip = self.conn.select(self.deny_ip_sql)
        deny_ip = [list(t) for t in deny_ip]
        return (self.deny_ip_name,deny_ip)
    
    def get_ftp_account(self) -> tuple:
        ftp_account = self.conn.select(self.ftp_account_sql)
        ftp_account = [list(t) for t in ftp_account]
        return (self.ftp_account_name,ftp_account)
    
    def get_mysql_account(self) -> tuple:
        mysql_account = self.conn.select(self.mysql_account_sql)
        mysql_account = [list(t) for t in mysql_account]
        return (self.mysql_account_name,mysql_account)
    
    def get_mysql_backup_info(self) -> tuple:
        mysql_backup_info = self.conn.select(self.mysql_backup_info_sql)
        mysql_backup_info = [list(t) for t in mysql_backup_info]
        return (self.mysql_backup_info_name,mysql_backup_info)
    
    def get_mysql_db_info(self) -> tuple:
        mysql_db_info = self.conn.select(self.mysql_db_info_sql)
        mysql_db_info = [list(t) for t in mysql_db_info]
        return (self.mysql_db_info_name,mysql_db_info)
    
    def get_mysql_upload_file(self) -> tuple:
        mysql_upload_file = self.conn.select(self.mysql_upload_file_sql)
        mysql_upload_file = [list(t) for t in mysql_upload_file]
        return (self.mysql_upload_file_name,mysql_upload_file)
    
    def get_install_info(self) -> tuple:
        info = []
        name = []
        with open(self.install_path,'r',encoding='utf-8') as fr:
            data = fr.readlines()
            info.append(data[2].split(':')[1])
            name.append(data[2].split(':')[0])
            info.append(data[3].split(':')[1])
            name.append(data[3].split(':')[0])
            info.append(data[4].split(':')[1])
            name.append(data[4].split(':')[0])
            info.append(data[5].split(':')[1])
            name.append(data[5].split(':')[0])
        return (name,[info])