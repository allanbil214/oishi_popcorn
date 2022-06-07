from db_config import db

class Model:
    #fungsi employee
    def read_emp(self):
        con = db.connect()
        cur = con.cursor()
        cur.execute("select * from employee")
        return cur.fetchall()   

    def add_emp(self, _nama_lengkap, _tempat_lahir, 
        _tanggal_lahir, _gender, _alamat, _username, _pwd):
        query = """INSERT INTO employee (nama_lengkap, 
                tempat_lahir, tanggal_lahir, gender, 
                alamat, username, password) VALUES (%s, %s, %s, %s, %s, %s, %s);"""
        data = [_nama_lengkap, _tempat_lahir, 
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

    def edit_emp(self, _id, _nama_lengkapnew, _tempat_lahirnew, 
        _tanggal_lahirnew, _gendernew, _alamatnew, _usernamenew, _pwdnew):
        query = """update employee set nama_lengkap=%s, tempat_lahir=%s,
                   tanggal_lahir=%s, gender=%s, alamat=%s, username=%s, password=%s where id=%s"""
        data = [_nama_lengkapnew, _tempat_lahirnew, _tanggal_lahirnew, _gendernew, _alamatnew, _usernamenew, _pwdnew, _id]
        conn = db.connect()
        cur = conn.cursor()
        cur.execute(query, data)
        conn.commit()
        return True
    
    def readone_emp(self, id):
        con = db.connect()
        cur = con.cursor()
        cur.execute("select * from employee where id=%s", id)
        return cur.fetchall()


    #fungsi movie
    def read_mov(self):
        con = db.connect()
        cur = con.cursor()
        cur.execute("select * from movie")
        return cur.fetchall()
    
    def readone_mov(self, id):
        con = db.connect()
        cur = con.cursor()
        cur.execute("select * from video where id=%s AND type_id='1'", id)
        return cur.fetchall()

    def add_mov(self, _name, _genre, _director, _release_date, _plot, _poster):
        query = """INSERT INTO movie (name, genre, director,
        release_date, plot, poster) VALUES (%s, %s, %s, %s, %s, %s);"""
        data = [_name, _genre, _director, _release_date, _plot, _poster]

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

    def edit_mov(self, _id, _name, _genre, _director, _release_date, _plot, _poster):
        query = """update movie set name=%s, genre=%s, director=%s,
                   release_date=%s, plot=%s, poster=%s where id=%s"""
        data = [ _name, _genre, _director, _release_date, _plot, _poster, _id]
        conn = db.connect()
        cur = conn.cursor()
        cur.execute(query, data)
        conn.commit()
        return True

    #fungsi tvseries
    def read_tv(self):
        con = db.connect()
        cur = con.cursor()
        cur.execute("select * from tvseries")
        return cur.fetchall()
    
    def readone_tv(self, id):
        con = db.connect()
        cur = con.cursor()
        cur.execute("select * from video where id=%s AND type_id='2'", id)
        return cur.fetchall()

    def add_tv(self, _name, _genre, _director, _episodes, _release_date, _plot, _poster):
        query = """INSERT INTO tvseries (name, genre, director, episodes,
        release_date, plot, poster) VALUES (%s, %s, %s, %s, %s, %s, %s);"""
        data = [_name, _genre, _director, _episodes, _release_date, _plot, _poster]

        conn = db.connect()
        cur = conn.cursor()
        cur.execute(query, data)
        conn.commit()
        return True
    
    def remove_tv(self, id):
        con = db.connect()
        cur = con.cursor()
        cur.execute("delete from tvseries where id=%s", (id,))
        con.commit()
        return True

    def edit_tv(self, _id, _name, _genre, _director, _episodes, _release_date, _plot, _poster):
        query = """update tvseries set name=%s, genre=%s, director=%s, episodes=%s,
                   release_date=%s, plot=%s, poster=%s where id=%s"""
        data = [_name, _genre, _director, _episodes, _release_date, _plot, _poster, _id]
        conn = db.connect()
        cur = conn.cursor()
        cur.execute(query, data)
        conn.commit()
        return True

    #fungsi frontpage
    def read_newmov(self): 
        con = db.connect()
        cur = con.cursor()
        cur.execute("select * from video where type_id='1' ORDER BY release_date desc limit 4")
        return cur.fetchall()

    def read_newtv(self):
        con = db.connect()
        cur = con.cursor()
        cur.execute("select * from video where type_id='2' ORDER BY release_date DESC")
        return cur.fetchall()

    def getmov_specific(self, name): 
        con = db.connect()
        cur = con.cursor()
        cur.execute("select * from video where name like %s AND type_id='1'", ('%' + name + '%'),)
        return cur.fetchall()

    def gettv_specific(self, name):
        con = db.connect()
        cur = con.cursor()
        cur.execute("select * from video where name like %s AND type_id='2'", ('%' + name + '%'),)
        return cur.fetchall()

    #fungsi aio
    def read_video(self):
        con = db.connect()
        cur = con.cursor()
        cur.execute("""SELECT video.*, video_type.name FROM video
                   LEFT JOIN video_type ON video_type.id = video.type_id""")
        return cur.fetchall()

    def readone_video(self, id):
        con = db.connect()
        cur = con.cursor()
        cur.execute("""SELECT video.*, video_type.name FROM video
                    LEFT JOIN video_type ON video_type.id = video.type_id
                    where video.id=%s""", id)
        return cur.fetchall()

    def add_video(self, _name, _genre, _type_id, _director, _episodes, _release_date, _plot, _poster):
        query = """INSERT INTO video (name, genre, type_id, director, episode,
        release_date, plot, poster) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);"""
        data = [_name, _genre, _type_id, _director, _episodes, _release_date, _plot, _poster]

        conn = db.connect()
        cur = conn.cursor()
        cur.execute(query, data)
        conn.commit()
        return True

    def remove_video(self, id):
        con = db.connect()
        cur = con.cursor()
        cur.execute("delete from video where id=%s", (id,))
        con.commit()
        return True

    def edit_video(self, _id, _name, _genre, _type_id, _director, _episodes, _release_date, _plot, _poster):
        query = """update video set name=%s, genre=%s, type_id=%s, director=%s, episode=%s,
                   release_date=%s, plot=%s, poster=%s where id=%s"""
        data = [_name, _genre, _type_id, _director, _episodes, _release_date, _plot, _poster, _id]

        conn = db.connect()
        cur = conn.cursor()
        cur.execute(query, data)
        conn.commit()
        return True

    #other
    def login(self, username):
        conn = db.connect()
        cursor = conn.cursor()
        cursor.execute("""SELECT * 
        FROM employee WHERE username=%s""", username)
        return cursor.fetchone()
