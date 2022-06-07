from db_config import db

class Model:
    #fungsi employee
    def read_emp(self):
        con = db.connect()
        cur = con.cursor()
        cur.execute("select * from employee")
        return cur.fetchall()
    
    def add_emp(self, _id, _nama_lengkap, _tempat_lahir, 
        _tanggal_lahir, _gender, _alamat, _username, _pwd):
        query = """INSERT INTO employee (id, nama_lengkap, 
                tempat_lahir, tanggal_lahir, gender, 
                alamat, username, password) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"""
        data = [_id, _nama_lengkap, _tempat_lahir, 
                _tanggal_lahir, _gender, _alamat, _username, _pwd]

        conn = db.connect()
        cur = conn.cursor()
        cur.execute(query, data)
        conn.commit()
        return True
    
    def remove_emp(self, id):
        con = db.connect()
        cur = con.cursor()
        cur.execute("delete from employee where id=%s", (id,))
        con.commit()
        return True

    def edit_emp(self, _id, _idnew, _nama_lengkapnew, _tempat_lahirnew, 
        _tanggal_lahirnew, _gendernew, _alamatnew, _usernamenew, _pwdnew):
        query = """update employee set id=%s, nama_lengkap=%s, tempat_lahir=%s,
                   tanggal_lahir=%s, gender=%s, alamat=%s, username=%s, password=%s where id=%s"""
        data = [_id, _nama_lengkapnew, _tempat_lahirnew, _tanggal_lahirnew, _gendernew, _alamatnew, _usernamenew, _pwdnew, _idnew]
        conn = db.connect()
        cur = conn.cursor()
        cur.execute(query, data)
        conn.commit()
        return True
    
    #fungsi member
    def read_mem(self):
        con = db.connect()
        cur = con.cursor()
        cur.execute("select * from member")
        return cur.fetchall()
    
    def add_mem(self, _id, _nama_lengkap, _tempat_lahir, 
        _tanggal_lahir, _gender, _alamat, _username, _pwd):
        query = """INSERT INTO member (id, nama_lengkap, 
                tempat_lahir, tanggal_lahir, gender, 
                alamat, username, password) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"""
        data = [_id, _nama_lengkap, _tempat_lahir, 
                _tanggal_lahir, _gender, _alamat, _username, _pwd]

        conn = db.connect()
        cur = conn.cursor()
        cur.execute(query, data)
        conn.commit()
        return True
    
    def remove_mem(self, id):
        con = db.connect()
        cur = con.cursor()
        cur.execute("delete from member where id=%s", (id,))
        con.commit()
        return True

    def edit_mem(self, _id, _idnew, _nama_lengkapnew, _tempat_lahirnew, 
        _tanggal_lahirnew, _gendernew, _alamatnew, _usernamenew, _pwdnew):
        query = """update member set id=%s, nama_lengkap=%s, tempat_lahir=%s,
                   tanggal_lahir=%s, gender=%s, alamat=%s, username=%s, password=%s where id=%s"""
        data = [_id, _nama_lengkapnew, _tempat_lahirnew, _tanggal_lahirnew, _gendernew, _alamatnew, _usernamenew, _pwdnew, _idnew]
        conn = db.connect()
        cur = conn.cursor()
        cur.execute(query, data)
        conn.commit()
        return True

    #fungsi movie
    def read_mov(self):
        con = db.connect()
        cur = con.cursor()
        cur.execute("select * from movie")
        return cur.fetchall()
    
    def add_mov(self, _id, _name, _genre, _artist, _release_date, _plot, _poster):
        query = """INSERT INTO movie (id, name, genre, artist,
        release_date, plot, poster) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"""
        data = [_id, _name, _genre, _artist, _release_date, _plot, _poster]

        conn = db.connect()
        cur = conn.cursor()
        cur.execute(query, data)
        conn.commit()
        return True
    
    def remove_mov(self, id):
        con = db.connect()
        cur = con.cursor()
        cur.execute("delete from movie where id=%s", (id,))
        con.commit()
        return True

    def edit_mov(self, _id, _name, _genre, _artist, _release_date, _plot, _poster, _idnew):
        query = """update movie set id=%s, name=%s, genre=%s, artist=%s,
                   release_date=%s, plot=%s, poster=%s where id=%s"""
        data = [_id, _name, _genre, _artist, _release_date, _plot, _poster, _idnew]
        conn = db.connect()
        cur = conn.cursor()
        cur.execute(query, data)
        conn.commit()
        return True

    #other
    def login(self, username):
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute("""SELECT id, username, password 
        FROM employee WHERE username=%s""", username)
        return cursor.fetchone()
