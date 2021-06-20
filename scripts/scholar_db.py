import sqlite3

class ScholarDB(object):
    """
    sqlite3 backed scholar storage
    """
    def __init__(self,db_path="./processed/scholars.db"):
        super().__init__()
        self.path = db_path
        self.conn = sqlite3.connect(self.path)

    def __exit__(self,*args):
        self.close()

    def close(self):
        '''close the connection to the database
        '''
        self.conn.close()

    def get_scholar_ids(self):
        '''
        fetch all ids from scholars
        ''''
        cursor = self.conn.cursor()
        cursor.execute(
            "select id from scholars"
        )
        results = [r[0] for r in cursor.fetchall()]
        cursor.close()
        return results

    def get_linkednodes(self,id):
        '''
        get the linked nodes for id 
        '''
        cursor = self.conn.cursor()
        cursor.execute(
            "select linkednodes from scholars where id = ?",(str(id),)
        )
        res = cursor.fetchone()[0]
        return res.split(",")

    def get_attributes(self,id,original=False):
        '''
        get the attributes/original_attributes for id
        '''
        cursor = self.conn.cursor()
        attribute = "attributes" if not original else "original_attributes"
        cursor.execute(
           "select {} from scholar where id = ?".format(attribute) ,(str(id),)
        )
        res = cursor.fetchone()[0]
        return res.split("\n")
