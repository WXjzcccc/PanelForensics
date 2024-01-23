import sqlite3

class DBHelper:
    def __init__(self,db_path: str) -> None:
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()

    def select(self,sql: str) -> list:
        """
        @sql:       要执行的SQL语句
        """
        try:
            self.cursor.execute(sql)
            rows = self.cursor.fetchall()
        except:
            print(f'数据库中存在不支持的字段，请比对查询语句{sql}')
            return [()]
        return rows
    
    def close(self) -> None:
        self.cursor.close()
        self.conn.close()