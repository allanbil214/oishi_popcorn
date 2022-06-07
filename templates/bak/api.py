from flask import Flask, jsonify, request, session, render_template, flash, redirect, url_for
from model import Model as db
from app import app
from functools import wraps
import jwt
import datetime

## Fungsi Utama
def require_api_token(func):
    @wraps(func)
    def check_token(*args, **kwargs):
        if 'api_session_token' not in session:
            flash("Missing token")
            return redirect(url_for("index"))
        try:
            data = jwt.decode(session["api_session_token"], app.config["SECRET_KEY"])
        except:
            flash("Token Expired")
            return redirect(url_for("index"))
        return func(*args, **kwargs)

    return check_token

@app.route("/")
def index():
    return render_template("login.html")

@app.route("/auth")
@require_api_token
def authorised():
    return render_template("home.html")

@app.route("/login", methods=["POST"])
def login():
    sql = db()
    username = request.form["username"]
    password = request.form["password"]
    if(username and password):
        row = sql.login(username)
        if(row):
            if(row[2] == password):
                token = jwt.encode({
                    "user": username,
                    "exp": datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
                },
                app.config["SECRET_KEY"])
                session["api_session_token"] = token.decode("utf-8")
                return redirect(url_for("authorised"))
        else:
            flash("Incorrect Username or Password")
    return redirect(url_for("index"))


## Fungsi Employee
@app.route("/show_emp", methods=["GET"])
def show_emp():
    sql = db()
    if(request.method == "GET"):
        getall = sql.read_emp()
        res = jsonify(getall)
        res.status_code = 200
        print(res)
        return res
    
    else:
        res = jsonify("Something's wrong... i can feel it!")
        print(res)
        return res

@app.route("/addone_emp", methods=["POST"])
def addone_emp():
    sql = db()
    _json = request.json
    _id = _json["id"]
    _nama_lengkap = _json["nama_lengkap"]
    _tempat_lahir = _json["tempat_lahir"]
    _tanggal_lahir = _json["tanggal_lahir"]
    _gender = _json["gender"]
    _alamat = _json["alamat"]
    _username = _json["username"]
    _pwd = _json["pwd"]
    strip_id = _id.lstrip().rstrip()
    strip_nama_lengkap = _nama_lengkap.lstrip().rstrip()
    strip_tempat_lahir = _tempat_lahir.lstrip().rstrip()
    strip_tanggal_lahir = _tanggal_lahir.lstrip().rstrip()
    strip_gender = _gender.lstrip().rstrip()
    strip_alamat = _alamat.lstrip().rstrip()
    strip_username = _username.lstrip().rstrip()
    strip_pwd = _pwd.lstrip().rstrip()
    if(request.method == "POST"):
        if(sql.add_emp(strip_id, strip_nama_lengkap, strip_tempat_lahir, 
                strip_tanggal_lahir, strip_gender, strip_alamat, strip_username, strip_pwd)):
            flash("All data are transfered!")
            print("hello")
            return redirect(url_for("data"))
        else:
            flash("All data are not transfered!")
            return redirect(url_for("data"))
    
    else:
        flash("Method is not match!")
        return redirect(url_for("data"))

@app.route("/sayonara_emp/<int:id>", methods=["DELETE"])
def sayonara_emp(id):
    sql = db()
    sql.remove_emp(id)
    res = jsonify("Deleted!")
    res.status_code = 200
    return res

@app.route("/ganti_emp", methods=["PUT"])
def ganti_emp():
    sql = db()
    _json = request.json
    _id = _json["id"]
    _idnew = _json["id"]
    _nama_lengkapnew = _json["nama_lengkap"]
    _tempat_lahirnew = _json["tempat_lahir"]
    _tanggal_lahirnew = _json["tanggal_lahir"]
    _gendernew = _json["gender"]
    _alamatnew = _json["alamat"]
    _usernamenew = _json["username"]
    _pwdnew = _json["pwd"]
    strip_id = _id.lstrip().rstrip()
    strip_idnew = _idnew.lstrip().rstrip().rstrip()
    strip_nama_lengkap = _nama_lengkapnew.lstrip().rstrip()
    strip_tempat_lahir = _tempat_lahirnew.lstrip().rstrip()
    strip_tanggal_lahir = _tanggal_lahirnew.lstrip().rstrip()
    strip_gender = _gendernew.lstrip().rstrip()
    strip_alamat = _alamatnew.lstrip().rstrip()
    strip_username = _usernamenew.lstrip().rstrip()
    strip_pwd = _pwdnew.lstrip().rstrip()
    if(request.method == "PUT"):
        if(sql.edit_emp(strip_id, strip_idnew, strip_nama_lengkap, strip_tempat_lahir, 
                strip_tanggal_lahir, strip_gender, strip_alamat, strip_username, strip_pwd)):
            res = jsonify("All data are updated!")
            res.status_code = 200
            return res
        else:
            res = jsonify("All data are not updated!")
            res.status_code = 200
            return res
    
    else:
        res = jsonify("Method not PUT!")
        return res

@app.route("/data_emp")
@require_api_token
def data_emp():
    return render_template("data_emp.html")

## Fungsi Member
@app.route("/show_mem", methods=["GET"])
def show_mem():
    sql = db()
    if(request.method == "GET"):
        getall = sql.read_mem()
        res = jsonify(getall)
        res.status_code = 200
        print(res)
        return res
    
    else:
        res = jsonify("Something's wrong... i can feel it!")
        print(res)
        return res

@app.route("/addone_mem", methods=["POST"])
def addone_mem():
    sql = db()
    _json = request.json
    _id = _json["id"]
    _nama_lengkap = _json["nama_lengkap"]
    _tempat_lahir = _json["tempat_lahir"]
    _tanggal_lahir = _json["tanggal_lahir"]
    _gender = _json["gender"]
    _alamat = _json["alamat"]
    _username = _json["username"]
    _pwd = _json["pwd"]
    strip_id = _id.lstrip().rstrip()
    strip_nama_lengkap = _nama_lengkap.lstrip().rstrip()
    strip_tempat_lahir = _tempat_lahir.lstrip().rstrip()
    strip_tanggal_lahir = _tanggal_lahir.lstrip().rstrip()
    strip_gender = _gender.lstrip().rstrip()
    strip_alamat = _alamat.lstrip().rstrip()
    strip_username = _username.lstrip().rstrip()
    strip_pwd = _pwd.lstrip().rstrip()
    if(request.method == "POST"):
        if(sql.add_mem(strip_id, strip_nama_lengkap, strip_tempat_lahir, 
                strip_tanggal_lahir, strip_gender, strip_alamat, strip_username, strip_pwd)):
            flash("All data are transfered!")
            print("hello")
            return redirect(url_for("data"))
        else:
            flash("All data are not transfered!")
            return redirect(url_for("data"))
    
    else:
        flash("Method is not match!")
        return redirect(url_for("data"))

@app.route("/sayonara_mem/<int:id>", methods=["DELETE"])
def sayonara_mem(id):
    sql = db()
    sql.remove_mem(id)
    res = jsonify("Deleted!")
    res.status_code = 200
    return res

@app.route("/ganti_mem", methods=["PUT"])
def ganti_mem():
    sql = db()
    _json = request.json
    _id = _json["id"]
    _idnew = _json["id"]
    _nama_lengkapnew = _json["nama_lengkap"]
    _tempat_lahirnew = _json["tempat_lahir"]
    _tanggal_lahirnew = _json["tanggal_lahir"]
    _gendernew = _json["gender"]
    _alamatnew = _json["alamat"]
    _usernamenew = _json["username"]
    _pwdnew = _json["pwd"]
    strip_id = _id.lstrip().rstrip()
    strip_idnew = _idnew.lstrip().rstrip().rstrip()
    strip_nama_lengkap = _nama_lengkapnew.lstrip().rstrip()
    strip_tempat_lahir = _tempat_lahirnew.lstrip().rstrip()
    strip_tanggal_lahir = _tanggal_lahirnew.lstrip().rstrip()
    strip_gender = _gendernew.lstrip().rstrip()
    strip_alamat = _alamatnew.lstrip().rstrip()
    strip_username = _usernamenew.lstrip().rstrip()
    strip_pwd = _pwdnew.lstrip().rstrip()
    if(request.method == "PUT"):
        if(sql.edit_mem(strip_id, strip_idnew, strip_nama_lengkap, strip_tempat_lahir, 
                strip_tanggal_lahir, strip_gender, strip_alamat, strip_username, strip_pwd)):
            res = jsonify("All data are updated!")
            res.status_code = 200
            return res
        else:
            res = jsonify("All data are not updated!")
            res.status_code = 200
            return res
    
    else:
        res = jsonify("Method not PUT!")
        return res

@app.route("/data_mem")
@require_api_token
def data_mem():
    return render_template("data_mem.html")

## Fungsi Member
@app.route("/show_mov", methods=["GET"])
def show_mov():
    sql = db()
    if(request.method == "GET"):
        getall = sql.read_mov()
        res = jsonify(getall)
        res.status_code = 200
        print(res)
        return res
    
    else:
        res = jsonify("Something's wrong... i can feel it!")
        print(res)
        return res

@app.route("/addone_mov", methods=["POST"])
def addone_mov():
    sql = db()
    _json = request.json
    _id = _json["id"]
    _nama_lengkap = _json["nama_lengkap"]
    _tempat_lahir = _json["tempat_lahir"]
    _tanggal_lahir = _json["tanggal_lahir"]
    _gender = _json["gender"]
    _alamat = _json["alamat"]
    _username = _json["username"]
    _pwd = _json["pwd"]
    strip_id = _id.lstrip().rstrip()
    strip_nama_lengkap = _nama_lengkap.lstrip().rstrip()
    strip_tempat_lahir = _tempat_lahir.lstrip().rstrip()
    strip_tanggal_lahir = _tanggal_lahir.lstrip().rstrip()
    strip_gender = _gender.lstrip().rstrip()
    strip_alamat = _alamat.lstrip().rstrip()
    strip_username = _username.lstrip().rstrip()
    strip_pwd = _pwd.lstrip().rstrip()
    if(request.method == "POST"):
        if(sql.add_mov(strip_id, strip_nama_lengkap, strip_tempat_lahir, 
                strip_tanggal_lahir, strip_gender, strip_alamat, strip_username, strip_pwd)):
            flash("All data are transfered!")
            print("hello")
            return redirect(url_for("data"))
        else:
            flash("All data are not transfered!")
            return redirect(url_for("data"))
    
    else:
        flash("Method is not match!")
        return redirect(url_for("data"))

@app.route("/sayonara_mov/<int:id>", methods=["DELETE"])
def sayonara_mov(id):
    sql = db()
    sql.remove_mov(id)
    res = jsonify("Deleted!")
    res.status_code = 200
    return res

@app.route("/ganti_mov", methods=["PUT"])
def ganti_mov():
    sql = db()
    _json = request.json
    _id = _json["id"]
    _idnew = _json["id"]
    _nama_lengkapnew = _json["nama_lengkap"]
    _tempat_lahirnew = _json["tempat_lahir"]
    _tanggal_lahirnew = _json["tanggal_lahir"]
    _gendernew = _json["gender"]
    _alamatnew = _json["alamat"]
    _usernamenew = _json["username"]
    _pwdnew = _json["pwd"]
    strip_id = _id.lstrip().rstrip()
    strip_idnew = _idnew.lstrip().rstrip().rstrip()
    strip_nama_lengkap = _nama_lengkapnew.lstrip().rstrip()
    strip_tempat_lahir = _tempat_lahirnew.lstrip().rstrip()
    strip_tanggal_lahir = _tanggal_lahirnew.lstrip().rstrip()
    strip_gender = _gendernew.lstrip().rstrip()
    strip_alamat = _alamatnew.lstrip().rstrip()
    strip_username = _usernamenew.lstrip().rstrip()
    strip_pwd = _pwdnew.lstrip().rstrip()
    if(request.method == "PUT"):
        if(sql.edit_mov(strip_id, strip_idnew, strip_nama_lengkap, strip_tempat_lahir, 
                strip_tanggal_lahir, strip_gender, strip_alamat, strip_username, strip_pwd)):
            res = jsonify("All data are updated!")
            res.status_code = 200
            return res
        else:
            res = jsonify("All data are not updated!")
            res.status_code = 200
            return res
    
    else:
        res = jsonify("Method not PUT!")
        return res

@app.route("/data_mov")
@require_api_token
def data_mov():
    return render_template("data_mov.html")

if __name__ == "__main__":
    app.run(debug=True)