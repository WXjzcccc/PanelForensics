from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QPainter, QIcon
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget,
    QLabel, QLineEdit, QPushButton, QTabWidget, QTableWidget, QTableWidgetItem, QTextEdit, QMessageBox
)
from qt_material import apply_stylesheet

from BTPanel.BTPanel import BTPanel
from BTPanel.BTPanel2 import BTPanel2
from BTPanel.BTPanel3 import BTPanel3
from OnePanel.OnePanel import OnePanel
from XPanel.XpPanel import XpPanel
from helper.ServerHelper import ServerHelper


def show_message(title :str, text: str, icon = QMessageBox.Icon.Warning):
    message_box = QMessageBox()
    message_box.setWindowTitle(title)
    message_box.setText(text)
    message_box.setIcon(icon)
    message_box.exec()


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.path= {}
        self.flag = ''
        self.bt_flag = 0
        self.onePanelData = {}
        self.btPanelData = {}
        self.xpPanelData = {}
        self.setWindowTitle("PanelForensics")
        self.setWindowIcon(QIcon("icon.ico"))

        # 主窗口布局
        main_widget = QWidget()
        main_layout = QVBoxLayout(main_widget)

        # 上半部分布局
        upper_widget = QWidget()
        upper_layout = QHBoxLayout(upper_widget)

        # 左侧 SSH 输入区域
        ssh_widget = QWidget()
        ssh_layout = QVBoxLayout(ssh_widget)
        ssh_layout.setAlignment(Qt.AlignTop)

        ssh_layout.addWidget(QLabel("IP 地址:"))
        self.ip_input = QLineEdit()
        self.ip_input.setPlaceholderText("输入 IP 地址")
        self.ip_input.setText("192.168.71.1")
        ssh_layout.addWidget(self.ip_input)

        ssh_layout.addWidget(QLabel("端口:"))
        self.port_input = QLineEdit()
        self.port_input.setPlaceholderText("输入端口")
        self.port_input.setText("22")
        ssh_layout.addWidget(self.port_input)

        ssh_layout.addWidget(QLabel("用户名:"))
        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("输入用户名")
        self.user_input.setText("root")
        ssh_layout.addWidget(self.user_input)

        ssh_layout.addWidget(QLabel("密码:"))
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("输入密码")
        self.password_input.setText("123456")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        ssh_layout.addWidget(self.password_input)

        self.connect_button = QPushButton("梭哈！")
        self.connect_button.clicked.connect(self.handle_connect)
        ssh_layout.addWidget(self.connect_button)

        upper_layout.addWidget(ssh_widget, 1)  # 左侧占据 2 比例宽度

        # 右侧功能介绍区域
        description_widget = QTextEdit()
        description_widget.setReadOnly(True)
        description_widget.setFontFamily("Consolas")
        description_widget.setFontPointSize(14)
        description_widget.setText(
"""
   ___                     __   ____                              _           
  / _ \ ___ _  ___  ___   / /  / __/ ___   ____ ___   ___   ___  (_) ____  ___
 / ___// _ `/ / _ \/ -_) / /  / _/  / _ \ / __// -_) / _ \ (_-< / / / __/ (_-<
/_/    \_,_/ /_//_/\__/ /_/  /_/    \___//_/   \__/ /_//_//___//_/  \__/ /___/
Author: WXjzc

1.使用SSH连接到Linux服务器
2.软件会自动检测宝塔面板、小皮面板和1Panel，并从服务器下载文件进行分析
3.分析结果以表格形式呈现，分析的内容仅为面板基础内容，不包含数据库、网站的重建与还原
4.每次取证请重新打开软件
"""
        )
        upper_layout.addWidget(description_widget, 3)  # 右侧占据 3 比例宽度
        main_layout.addWidget(upper_widget, 1)  # 上半部分占据 1 比例高度

        # 下半部分 Tab 表格区域
        self.tab_widget = QTabWidget(self)
        main_layout.addWidget(self.tab_widget, 2)  # 下半部分占据 2 比例高度

        # 设置主窗口
        self.setCentralWidget(main_widget)

    def add_tab(self, name, data):
        # 创建新 Tab 页
        tab = QWidget()
        tab_layout = QVBoxLayout(tab)

        # 创建表格
        table = QTableWidget()
        table_head = data[0]
        table_data = data[1]
        x = len(table_head)
        y = len(table_data)
        table.setColumnCount(x)
        table.setRowCount(y)
        table.setHorizontalHeaderLabels(table_head)
        table.setVerticalHeaderLabels([f"{i}" for i in range(1, y+1)])
        # 填充表格内容
        for row in range(y):
            for col in range(x):
                table.setItem(row, col, QTableWidgetItem(table_data[row][col]))

        # 设置表格的宽度自适应和最小宽度
        table.horizontalHeader().setStretchLastSection(True)
        table.horizontalHeader().setDefaultSectionSize(120)
        table.setMinimumWidth(600)

        tab_layout.addWidget(table)
        self.tab_widget.addTab(tab, name)

    def show_table(self, panel_data: dict):
        for key, value in panel_data.items():
            self.add_tab(key,value)

    def handle_connect(self):
        self.tab_widget.clear()
        # 获取用户输入
        username = self.user_input.text()
        password = self.password_input.text()
        ip_address = self.ip_input.text()
        port = self.port_input.text()
        self.download(ip_address, port, username, password)
        panel_data = self.get_panel_data()
        if panel_data:
            self.show_table(panel_data)


    def get_panel_data(self):
        if self.flag == 'bt':
            if self.bt_flag == 1:
                self.get_btPanel_data2()
            elif self.bt_flag == 2:
                self.get_btPanel_data3()
            else:
                self.get_btPanel_data()
            return self.btPanelData
        elif self.flag == 'xp':
            self.get_xpPanel_data()
            return self.xpPanelData
        elif self.flag == 'one':
            self.get_onePanel_data()
            return self.onePanelData
        else:
            show_message("提示","未检测出支持的面板！",QMessageBox.Icon.Information)
        return {}

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
            if serverHelper.detect_bt_version() == 1:
                self.bt_flag = 1
                self.path = serverHelper.download_bt_new()
            elif serverHelper.detect_bt_version() == 2:
                self.bt_flag = 2
                self.path = serverHelper.download_bt()
            else:
                self.bt_flag = 0
                self.path = serverHelper.download_bt()
        elif panel == 'one':
            self.flag = 'one'
            self.path = serverHelper.download_one()
        elif panel == 'xp':
            self.flag = 'xp'
            self.path = serverHelper.download_xp()
        elif panel == '连接失败':
            show_message("错误","无法连接至目标服务器，请确认连接配置，或\n查看服务器SSH服务是否正常，防火墙是否放行或关闭！")
            return None
        serverHelper.close()

    def get_xpPanel_data(self):
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

    def get_onePanel_data(self):
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

    def get_btPanel_data(self):
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
        self.btPanelData.update({'历史命令':btPanel.get_history()})
        self.btPanelData.update({'任务':btPanel.get_tasks()})
        self.btPanelData.update({'面板用户':btPanel.get_users()})
        self.btPanelData.update({'面板配置':btPanel.get_settings()})
        btPanel.close()

    def get_btPanel_data2(self):
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
        self.btPanelData.update({'历史命令': btPanel.get_history()})
        self.btPanelData.update({'网站':btPanel.get_sites()})
        self.btPanelData.update({'任务':btPanel.get_tasks()})
        self.btPanelData.update({'面板用户':btPanel.decrypt(btPanel.get_users())})
        self.btPanelData.update({'面板配置':btPanel.get_settings()})


    def get_btPanel_data3(self):
        btPanel = BTPanel3()
        btPanel.set_path(self.path)
        btPanel.connect()
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
        self.btPanelData.update({'历史命令': btPanel.get_history()})
        self.btPanelData.update({'网站':btPanel.get_sites()})
        self.btPanelData.update({'任务':btPanel.get_tasks()})
        self.btPanelData.update({'面板用户':btPanel.decrypt(btPanel.get_users())})
        self.btPanelData.update({'面板配置':btPanel.get_settings()})
        btPanel.close()


class TextDrawingWidget(QWidget):
    def __init__(self, text):
        super().__init__()
        self.text = text

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.TextAntialiasing)
        font = QFont('Mono', 12)
        painter.setFont(font)
        painter.setPen(Qt.blue)
        painter.drawText(self.rect(), Qt.AlignCenter, self.text)
        painter.end()

if __name__ == "__main__":
    app = QApplication([])
    apply_stylesheet(app, theme='light_amber.xml')
    window = MainWindow()
    window.resize(1200, 800)
    window.show()
    app.exec()
