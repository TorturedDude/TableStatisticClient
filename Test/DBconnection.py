import psycopg2

class DBconn:

    _dbname = 'TestApp'
    _user = 'postgres'
    _password = '354610213'
    _host = 'localhost'

    def AddClients(self,inicials,status,service,adress):

        conn = psycopg2.connect(dbname=self._dbname, user=self._user, password=self._password, host=self._host)
        conn.autocommit = True

        try:
            with conn.cursor() as cursor:
                cursor.execute(f"INSERT INTO clients (inicials,status,service,adress) VALUES ('{inicials}','{status}','{service}','{adress}');")
                conn.commit()

        except Exception as _ex:
            print('[INFO] Error while inputing data in database...', _ex)
        finally:
            if conn:
                conn.close()

    def SelectFromUsers(self):

        conn = psycopg2.connect(dbname=self._dbname, user=self._user, password=self._password, host=self._host)

        try:
            cursor = conn.cursor()

            cursor.execute('SELECT * FROM "Users";')
            firstdata = cursor.fetchall()
            lastdata = [i for i in firstdata[0]]
            return lastdata
        except Exception as _ex:
            print('[INFO] Error while selecting data in database...', _ex)
        finally:
            if conn:
                conn.close()

    def SelectFromServices(self):

        conn = psycopg2.connect(dbname=self._dbname, user=self._user, password=self._password, host=self._host)

        try:
            cursor = conn.cursor()

            cursor.execute('SELECT "Title" FROM "Services";')
            firstdata = cursor.fetchall()
            lastdata = []

            for i in firstdata:
                lastdata.append(i[0])

            return lastdata
        except Exception as _ex:
            print('[INFO] Error while selecting data in database...', _ex)
        finally:
            if conn:
                conn.close()

    def SelectFromClients(self):

        conn = psycopg2.connect(dbname=self._dbname, user=self._user, password=self._password, host=self._host)

        try:
            cursor = conn.cursor()

            cursor.execute('SELECT * FROM "clients";')
            firstdata = cursor.fetchall()
            lastdata = []

            for i in firstdata:
                lastdata.append(i)

            return lastdata
        except Exception as _ex:
            print('[INFO] Error while selecting data in database...', _ex)
        finally:
            if conn:
                conn.close()

    def SelectFromStatus(self):

        conn = psycopg2.connect(dbname=self._dbname, user=self._user, password=self._password, host=self._host)

        try:
            cursor = conn.cursor()

            cursor.execute('SELECT * FROM status;')
            firstdata = cursor.fetchall()
            lastdata = []

            for i in firstdata:
                lastdata.append(i)


            return lastdata
        except Exception as _ex:
            print('[INFO] Error while selecting data in database...', _ex)
        finally:
            if conn:
                conn.close()
