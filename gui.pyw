import PySimpleGUI as psg
from BTPanel.BTPanel2 import BTPanel2
from OnePanel.OnePanel import OnePanel
from helper.ServerHelper import ServerHelper
from BTPanel.BTPanel import BTPanel
from XPanel.XpPanel import XpPanel

class GUI:
    def __init__(self) -> None:
        self.onePanelData = {}
        self.btPanelData = {}
        self.xpPanelData = {}
        self.flag = ''
        self.bt_flag = ''
        self.path = {}

    def show_details(self,event,data) -> None:
        """
        @event:     触发的事件
        @data:      取证结果
        """
        try:
            row = values.get(event)[0]
            tmp = ''
            for i in range(len(data.get(event)[1][row])):
                tmp += data.get(event)[0][i]+':'+str(data.get(event)[1][row][i])+'\n'
            psg.popup_scrolled(tmp,title=event,background_color='lightblue')
        except:
            pass

    def download(self,host: str,port: int,username: str,password: str) -> None:
        """
        @host:        需要连接的主机地址
        @port:        主机端口
        @username:    用户名
        @password:    密码
        """
        serverHelper = ServerHelper(host,port,username,password)
        serverHelper.connect()
        panel = serverHelper.detect_panel()
        self.path = {}
        if panel == 'bt':
            self.flag = 'bt'
            if serverHelper.detect_bt_version:
                self.bt_flag = True
                self.path = serverHelper.download_bt_new()
            else:
                self.bt_flag = False
                self.path = serverHelper.download_bt()
        elif panel == 'one':
            self.flag = 'one'
            self.path = serverHelper.download_one()
        elif panel == 'xp':
            self.flag = 'xp'
            self.path = serverHelper.download_xp()
        elif panel == '连接失败':
            psg.popup_no_buttons('无法连接至目标服务器，请确认连接配置，或\n查看服务器SSH服务是否正常，防火墙是否放行或关闭！',title='错误')
            return None
        serverHelper.close()

    def get_onePanel_layout(self) -> list:
        onePanel = OnePanel()
        onePanel.set_path(self.path)
        onePanel.connect()
        self.onePanelData.update({'登录日志':onePanel.get_login_logs()})
        self.onePanelData.update({'操作日志':onePanel.get_operation_logs()})
        self.onePanelData.update({'备份记录':onePanel.get_backup_records()})
        self.onePanelData.update({'命令':onePanel.get_commands()})
        self.onePanelData.update({'计划任务':onePanel.get_cronjobs()})
        self.onePanelData.update({'数据库':onePanel.get_database()})
        self.onePanelData.update({'安装应用':onePanel.get_installed_app()})
        self.onePanelData.update({'计划任务执行记录':onePanel.get_job_records()})
        self.onePanelData.update({'Mysql配置':onePanel.get_mysql()})
        self.onePanelData.update({'面板配置':onePanel.get_settings()})
        self.onePanelData.update({'网站':onePanel.get_websites()})
        onePanel.close()
        onePanel_tab_layout = []
        for key in self.onePanelData.keys():
            onePanel_tab_layout.append([psg.Tab(key,[[psg.Table(values=self.onePanelData.get(key)[1],headings=self.onePanelData.get(key)[0],num_rows=20,def_col_width=20,auto_size_columns=False,display_row_numbers=True,justification='center',alternating_row_color='lightblue',text_color='black',vertical_scroll_only=False,bind_return_key=True,key=key)]])])
        return onePanel_tab_layout

    def get_btPanel_layout(self) -> list:
        btPanel = BTPanel()
        btPanel.set_path(self.path)
        btPanel.connect()
        self.btPanelData.update({'备份记录':btPanel.get_backup()})
        self.btPanelData.update({'配置':btPanel.get_config()})
        self.btPanelData.update({'计划任务':btPanel.get_crontab()})
        self.btPanelData.update({'数据库':btPanel.get_databases()})
        self.btPanelData.update({'防火墙':btPanel.get_firewall()})
        self.btPanelData.update({'FTP服务':btPanel.get_ftps()})
        self.btPanelData.update({'操作日志':btPanel.get_logs()})
        self.btPanelData.update({'网站':btPanel.get_sites()})
        self.btPanelData.update({'任务':btPanel.get_tasks()})
        self.btPanelData.update({'面板用户':btPanel.get_users()})
        self.btPanelData.update({'面板配置':btPanel.get_settings()})
        btPanel.close()
        btPanel_tab_layout = []
        for key in self.btPanelData.keys():
            btPanel_tab_layout.append([psg.Tab(key,[[psg.Table(values=self.btPanelData.get(key)[1],headings=self.btPanelData.get(key)[0],num_rows=20,def_col_width=20,auto_size_columns=False,display_row_numbers=True,justification='center',alternating_row_color='lightblue',text_color='black',vertical_scroll_only=False,bind_return_key=True,key=key)]])])
        return btPanel_tab_layout
    
    def get_btPanel_layout2(self) -> list:
        btPanel = BTPanel2()
        btPanel.set_path(self.path)
        btPanel.get_div()
        self.btPanelData.update({'备份记录':btPanel.get_backup()})
        self.btPanelData.update({'配置':btPanel.decrypt(btPanel.get_config())})
        self.btPanelData.update({'计划任务':btPanel.get_crontab()})
        self.btPanelData.update({'数据库':btPanel.decrypt(btPanel.get_databases())})
        self.btPanelData.update({'远程数据库':btPanel.decrypt(btPanel.get_databases_server())})
        self.btPanelData.update({'防火墙':btPanel.get_firewall()})
        self.btPanelData.update({'防火墙-ip':btPanel.get_firewall_ip()})
        self.btPanelData.update({'防火墙-端口转发':btPanel.get_firewall_trans()})
        self.btPanelData.update({'FTP服务':btPanel.decrypt(btPanel.get_ftps())})
        self.btPanelData.update({'操作日志':btPanel.get_logs()})
        self.btPanelData.update({'网站':btPanel.get_sites()})
        self.btPanelData.update({'任务':btPanel.get_tasks()})
        self.btPanelData.update({'面板用户':btPanel.decrypt(btPanel.get_users())})
        self.btPanelData.update({'面板配置':btPanel.get_settings()})
        btPanel_tab_layout = []
        for key in self.btPanelData.keys():
            btPanel_tab_layout.append([psg.Tab(key,[[psg.Table(values=self.btPanelData.get(key)[1],headings=self.btPanelData.get(key)[0],num_rows=20,def_col_width=20,auto_size_columns=False,display_row_numbers=True,justification='center',alternating_row_color='lightblue',text_color='black',vertical_scroll_only=False,bind_return_key=True,key=key)]])])
        return btPanel_tab_layout

    def get_xpPanel_layout(self) -> list:
        xpPanel = XpPanel()
        xpPanel.set_path(self.path)
        xpPanel.connect()
        self.xpPanelData.update({'防火墙':xpPanel.get_accept_port()})
        self.xpPanelData.update({'用户':xpPanel.get_admins()})
        self.xpPanelData.update({'黑名单':xpPanel.get_deny_ip()})
        self.xpPanelData.update({'FTP用户':xpPanel.get_ftp_account()})
        self.xpPanelData.update({'安装信息':xpPanel.get_install_info()})
        self.xpPanelData.update({'MySQL用户':xpPanel.get_mysql_account()})
        self.xpPanelData.update({'MySQL备份':xpPanel.get_mysql_backup_info()})
        self.xpPanelData.update({'MySQL':xpPanel.get_mysql_db_info()})
        self.xpPanelData.update({'MySQL文件上传':xpPanel.get_mysql_upload_file()})
        self.xpPanelData.update({'操作日志':xpPanel.get_operlog()})
        self.xpPanelData.update({'回收站':xpPanel.get_recycle()})
        self.xpPanelData.update({'Server':xpPanel.get_server_info()})
        self.xpPanelData.update({'系统配置':xpPanel.get_syscfg()})
        self.xpPanelData.update({'计划任务记录':xpPanel.get_task_runlog()})
        self.xpPanelData.update({'计划任务':xpPanel.get_taskmng()})
        self.xpPanelData.update({'URL':xpPanel.get_urlmng()})
        self.xpPanelData.update({'网站':xpPanel.get_website()})
        xpPanel.close()
        xpPanel_tab_layout = []
        for key in self.xpPanelData.keys():
            xpPanel_tab_layout.append([psg.Tab(key,[[psg.Table(values=self.xpPanelData.get(key)[1],headings=self.xpPanelData.get(key)[0],num_rows=20,def_col_width=20,auto_size_columns=False,display_row_numbers=True,justification='center',alternating_row_color='lightblue',text_color='black',vertical_scroll_only=False,bind_return_key=True,key=key)]])])
        return xpPanel_tab_layout

    def get_table_layout(self) -> list:
        if self.flag == 'bt':
            print('done')
            if self.bt_flag:
                return self.get_btPanel_layout2()
            else:
                return self.get_btPanel_layout()
        elif self.flag == 'one':
            print('done')
            return self.get_onePanel_layout()
        elif self.flag == 'xp':
            print('done')
            return self.get_xpPanel_layout()
        return []

if __name__ == '__main__':
    gui = GUI()
    slogan = """
 _______                        __   ________                                        _                 
|_   __ \                      [  | |_   __  |                                      (_)                
  | |__) |,--.   _ .--.  .---.  | |   | |_ \_|.--.   _ .--.  .---.  _ .--.   .--.   __   .---.  .--.   
  |  ___/`'_\ : [ `.-. |/ /__\\ | |   |  _| / .'`\ \[ `/'`\]/ /__\\[ `.-. | ( (`\] [  | / /'`\]( (`\]  
 _| |_   // | |, | | | || \__., | |  _| |_  | \__. | | |    | \__., | | | |  `'.'.  | | | \__.  `'.'.  
|_____|  \'-;__/[___||__]'.__.'[___]|_____|  '.__.' [___]    '.__.'[___||__][\__) )[___]'.___.'[\__) )                                                                                                     
1.使用SSH连接到Linux服务器
2.软件会自动检测宝塔面板、小皮面板和1Panel，并从服务器下载文件进行分析
3.分析结果以表格形式呈现，分析的内容仅为面板基础内容，不包含数据库、网站的重建与还原
4.每次取证请重新打开软件
"""
    layout = [
    [psg.Column([
        [psg.Text('Host:\t'),psg.InputText('192.168.8.129',size=(15),key='host')],
        [psg.Text('Port:\t'),psg.InputText(22,size=(15),key='port')],
        [psg.Text('用户名:\t'),psg.InputText('root',size=(15),key='username')],
        [psg.Text('密码:\t'),psg.InputText('666666',size=(15),password_char='*',key='password')],
        [psg.Button('梭哈!')],
        ]),psg.Column([
            [psg.Stretch(),psg.Text(slogan,font=('Courier New',9),text_color='lightgreen'),psg.Stretch()],
    ])],
    [psg.Stretch(),psg.Text(f'{"="*40}👇结果会出现在下面👇{"="*40}',text_color='lightyellow',key='description'),psg.Stretch()]
    ]
    window = psg.Window('PanelForensics', layout, size=(800,600))
    while True:
        # 事件监听循环
        event, values = window.read()
        print(event, values)
        if event in (None, 'Exit'):
            break
        elif event in gui.onePanelData.keys():
            gui.show_details(event,gui.onePanelData)
        elif event in gui.btPanelData.keys():
            gui.show_details(event,gui.btPanelData)
        elif event in gui.xpPanelData.keys():
            gui.show_details(event,gui.xpPanelData)
        elif event == '梭哈!':
            if gui.flag == '':
                host = values.get('host')
                port = int(values.get('port'))
                username = values.get('username')
                password = values.get('password')
                gui.download(host,port,username,password)
                window.extend_layout(window,[[psg.TabGroup(gui.get_table_layout(),key='tabGroup')]])
                window.finalize()
                if gui.flag == 'bt':
                    window['description'].update(f'{"="*40}👇检测到宝塔面板👇{"="*40}')
                elif gui.flag == 'one':
                    window['description'].update(f'{"="*40}👇检测到1Panel👇{"="*40}')
                elif gui.flag == 'xp':
                    window['description'].update(f'{"="*40}👇检测到小皮面板👇{"="*40}')
            else:
                psg.popup_no_buttons('此版本无法多次取证，请重启应用！',title='Warning')
    window.close()
