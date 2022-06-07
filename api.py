from flask import Flask, jsonify, request, session, render_template, flash, redirect, url_for
from model import Model as db
from app import app
from functools import wraps
from passlib.hash import sha256_crypt
from flask_uploads import UploadSet, configure_uploads, IMAGES
import jwt
import datetime

app.config['UPLOADED_PHOTOS_DEST'] = 'static/img'
photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)

## Fungsi Utama
def require_api_token(func):
    @wraps(func)
    def check_token(*args, **kwargs):
        if 'api_session_token' not in session:
            flash("Missing token")
            return redirect(url_for("dashboard"))
        try:
            data = jwt.decode(session["api_session_token"], app.config["SECRET_KEY"])
        except:
            flash("Token Expired")
            return redirect(url_for("dashboard"))
        return func(*args, **kwargs)

    return check_token

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard/login.html")

@app.route("/auth")
@require_api_token
def authorised():
    return render_template("dashboard/home.html", fname = session["fullname"])

@app.route("/login", methods=["POST"])
def login():
    sql = db()
    username = request.form["username"]
    password = request.form["password"]
    if(username and password):
        row = sql.login(username)
        if(row):
            if(sha256_crypt.verify(password, row[7])):
                token = jwt.encode({
                    "user": username,
                    "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
                },
                app.config["SECRET_KEY"])
                session["api_session_token"] = token.decode("utf-8")
                session["fullname"] = row[1]
                return redirect(url_for("authorised"))
        else:
            flash("Incorrect Username or Password")
    return redirect(url_for("dashboard"))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for("dashboard"))

# Kode Film 
@app.route("/add_video")
@require_api_token
def add_video():
    return render_template(
        "dashboard/video/add_video.html")

@app.route("/addsave_video", methods=["POST"])
def addsave_video():
    sql = db()
    _film_name = request.form["txtName"]
    _genre = ', '.join(request.form.getlist('genre'))
    _type_id = request.form["txtType"]
    _rdate = request.form["txtRDate"]
    _teps = request.form["txtEps"]
    _director = request.form["txtDirector"]
    _plot = request.form["txtPlot"]
    _poster = request.files["picture"]
    if(request.method == "POST"):
        pic = _poster.filename
        photo = pic.replace("'", "")
        picture = photo.replace(" ", "_")
        if picture.lower().endswith(('.png', '.jpg', '.jpeg')):
            save_photo = photos.save(_poster)
            if save_photo:
                if(sql.add_video(_film_name, _genre, _type_id,
                    _director, _teps, _rdate, _plot, picture)):
                    flash("All data are transfered!")
                    return redirect(url_for("show_video"))
                else:
                    flash("All data are not transfered!")
                    return redirect(url_for("show_video"))
    
    else:
        flash("Method is not match!")
        return redirect(url_for("show_video"))

@app.route("/detailF_video/<int:id>", methods=["GET", "POST"])
@require_api_token
def detail_video(id):
    sql = db()
    getted = sql.readone_video(id)
    return render_template(
        "dashboard/video/detail_video.html",
        pData = getted,
        oldID = id)

@app.route("/edit_video/<int:id>", methods=["GET", "POST"])
@require_api_token
def edit_video(id):
    sql = db()
    getted = sql.readone_video(id)
    return render_template(
        "dashboard/video/edit_video.html",
        pData = getted,
        oldID = id)

@app.route("/sayonara/<int:id>", methods=["DELETE"])
def sayonara_video(id):
    sql = db()
    sql.remove_video(id)
    res = jsonify("Deleted!")
    res.status_code = 200
    return res

@app.route("/ganti_video", methods=["POST"])
def ganti_video():
    sql = db()
    _id = request.form["hidid"]
    _film_name = request.form["txtName"]
    _genre = ', '.join(request.form.getlist('genre'))
    _type_id = request.form["txtType"]
    _rdate = request.form["txtRDate"]
    _teps = request.form["txtEps"]
    _director = request.form["txtDirector"]
    _plot = request.form["txtPlot"]
    _poster = request.files["picture"]
    if(request.method == "POST"):
        pic = _poster.filename
        photo = pic.replace("'", "")
        picture = photo.replace(" ", "_")
        if picture.lower().endswith(('.png', '.jpg', '.jpeg')):
            save_photo = photos.save(_poster)
            if save_photo:
                if(sql.edit_video(_id, _film_name, _genre, _type_id,
                _director, _teps, _rdate, _plot, picture)):
                    flash("All data are updated!")
                    return redirect(url_for("show_video"))
                else:
                    flash("All data are not updated!")
                    return redirect(url_for("show_video"))
    
    else:
        flash("Method not POST!")
        return redirect(url_for("show_video"))

@app.route("/show_video")
@require_api_token
def show_video():
    return render_template(
        "dashboard/video/data_video.html")

@app.route("/data_video", methods=["GET"])
def data_video():
    sql = db()
    if(request.method == "GET"):
        getall = sql.read_video()
        res = jsonify(getall)
        res.status_code = 200
        print(res)
        return res
    
    else:
        res = jsonify("Something's wrong... i can feel it!")
        print(res)
        return res

## Fungsi Employee
@app.route("/addsave_emp", methods=["POST"])
def addsave_emp():
    sql = db()
    _nama_lengkap = request.form["txtName"]
    _tempat_lahir = request.form["txtBPlace"]
    _tanggal_lahir = request.form["txtBDate"]
    _gender = request.form["gender"]
    _alamat = request.form["txtAddress"]
    _username = request.form["txtUname"]
    _pwd = sha256_crypt.encrypt(str(request.form["txtPwd"]))
    if(request.method == "POST"):
        if(sql.add_emp(_nama_lengkap, _tempat_lahir, 
                _tanggal_lahir, _gender, _alamat, _username, _pwd)):
            flash("All data are transfered!")
            return redirect(url_for("dashboard"))
        else:
            flash("All data are not transfered!")
            return redirect(url_for("dashboard"))
    
    else:
        flash("Method is not match!")
        return redirect(url_for("data_emp"))

@app.route("/sayonara_emp", methods=["POST"])
def sayonara_emp():
    sql = db()
    id = request.form["del_this"]
    sql.remove_emp(id)
    flash("The data are deleted!")
    return redirect(url_for("data_emp"))

@app.route("/add_emp")
@require_api_token
def add_emp():
    return render_template(
        "dashboard/employee/add_emp.html")

@app.route("/edit_emp", methods=["GET", "POST"])
@require_api_token
def edit_emp():
    id = request.form["edit_this"]
    sql = db()
    getted = sql.readone_emp(id)
    return render_template(
        "dashboard/employee/edit_emp.html",
        pData = getted,
        oldID = id)

@app.route("/ganti_emp", methods=["POST"])
def ganti_emp():
    sql = db()
    _id = request.form["hidid"]
    _nama_lengkap = request.form["txtName"]
    _tempat_lahir = request.form["txtBPlace"]
    _tanggal_lahir = request.form["txtBDate"]
    _gender = request.form["gender"]
    _alamat = request.form["txtAddress"]
    _username = request.form["txtUname"]
    _pwd = sha256_crypt.encrypt(str(request.form["txtPwd"]))
    if(request.method == "POST"):
        if(sql.edit_emp(_id, _nama_lengkap, _tempat_lahir, 
                _tanggal_lahir, _gender, _alamat, _username, _pwd)):
            flash("All data are updated!")
            return redirect(url_for("data_emp"))
        else:
            flash("All data are not updated!")
            return redirect(url_for("data_emp"))
    
    else:
        flash("Method not POST!")
        return redirect(url_for("data_emp"))

@app.route("/data_emp")
@require_api_token
def data_emp():
    sql = db()
    getall = sql.read_emp()
    return render_template("dashboard/employee/data_emp.html", dEmp = getall)

#fungsi user page
@app.route("/")
def frontpage():
    sql = db()
    getmov = sql.read_newmov()
    gettv = sql.read_newtv()
    return render_template("user/index.html", movdata = getmov, tvdata = gettv)
    
@app.route("/search", methods=["POST"])
def search():
    sql = db()
    name = request.form["search"]
    getmov = sql.getmov_specific(name)
    gettv = sql.gettv_specific(name)
    return render_template("user/search.html", movdata = getmov, tvdata = gettv)

@app.route("/viewmovie/<int:id>", methods=["GET"])
def viewmovie(id):
    sql = db()
    getone = sql.readone_mov(id)
    return render_template("user/view_mov.html", data = getone)

@app.route("/viewtv/<int:id>", methods=["GET"])
def viewtv(id):
    sql = db()
    getone = sql.readone_tv(id)
    return render_template("user/view_tv.html", data = getone)


### LEGACY CODE DIBAWAH ###


## Fungsi Movie
@app.route("/add_mov")
@require_api_token
def add_mov():
    return render_template(
        "dashboard/movie/add_mov.html")

@app.route("/addsave_mov", methods=["POST"])
def addsave_mov():
    sql = db()
    _movie_name = request.form["txtName"]
    _genre = ', '.join(request.form.getlist('genre'))
    _rdate = request.form["txtRDate"]
    _director = request.form["txtDirector"]
    _plot = request.form["txtPlot"]
    _poster = request.files["picture"]
    if(request.method == "POST"):
        pic = _poster.filename
        photo = pic.replace("'", "")
        picture = photo.replace(" ", "_")
        if picture.lower().endswith(('.png', '.jpg', '.jpeg')):
            save_photo = photos.save(_poster)
            if save_photo:
                if(sql.add_mov(_movie_name, _genre, 
                    _director, _rdate, _plot, picture)):
                    flash("All data are transfered!")
                    return redirect(url_for("data_mov"))
                else:
                    flash("All data are not transfered!")
                    return redirect(url_for("data_mov"))
    
    else:
        flash("Method is not match!")
        return redirect(url_for("data_mov"))

@app.route("/edit_mov", methods=["GET", "POST"])
@require_api_token
def edit_mov():
    id = request.form["edit_this"]
    sql = db()
    getted = sql.readone_mov(id)
    return render_template(
        "dashboard/movie/edit_mov.html",
        pData = getted,
        oldID = id)

@app.route("/sayonara_mov", methods=["POST"])
def sayonara_mov():
    sql = db()
    id = request.form["del_this"]
    sql.remove_mov(id)
    flash("The data are deleted!")
    return redirect(url_for("data_mov"))

@app.route("/ganti_mov", methods=["POST"])
def ganti_mov():
    sql = db()
    _id = request.form["hidid"]
    _movie_name = request.form["txtName"]
    _genre = ', '.join(request.form.getlist('genre'))
    _rdate = request.form["txtRDate"]
    _director = request.form["txtDirector"]
    _plot = request.form["txtPlot"]
    _poster = request.files["picture"]
    if(request.method == "POST"):
        pic = _poster.filename
        photo = pic.replace("'", "")
        picture = photo.replace(" ", "_")
        if picture.lower().endswith(('.png', '.jpg', '.jpeg')):
            save_photo = photos.save(_poster)
            if save_photo:
                if(sql.edit_mov(_id, _movie_name, _genre, 
                            _director, _rdate, _plot, picture)):
                    flash("All data are updated!")
                    return redirect(url_for("data_mov"))
                else:
                    flash("All data are not updated!")
                    return redirect(url_for("data_mov"))
    
    else:
        flash("Method not POST!")
        return redirect(url_for("data_mov"))

@app.route("/data_mov")
@require_api_token
def data_mov():
    sql = db()
    getall = sql.read_mov()
    return render_template("dashboard/movie/data_mov.html", dMov = getall)

## Fungsi TV Series
@app.route("/add_tv")
@require_api_token
def add_tv():
    return render_template(
        "dashboard/tv/add_tv.html")

@app.route("/addsave_tv", methods=["POST"])
def addsave_tv():
    sql = db()
    _tvs_name = request.form["txtName"]
    _genre = ', '.join(request.form.getlist('genre'))
    _rdate = request.form["txtRDate"]
    _teps = request.form["txtEps"]
    _director = request.form["txtDirector"]
    _plot = request.form["txtPlot"]
    _poster = request.files["picture"]
    if(request.method == "POST"):
        pic = _poster.filename
        photo = pic.replace("'", "")
        picture = photo.replace(" ", "_")
        if picture.lower().endswith(('.png', '.jpg', '.jpeg')):
            save_photo = photos.save(_poster)
            if save_photo:
                if(sql.add_tv(_tvs_name, _genre, 
                    _director, _teps, _rdate, _plot, picture)):
                    flash("All data are transfered!")
                    return redirect(url_for("data_tv"))
                else:
                    flash("All data are not transfered!")
                    return redirect(url_for("data_tv"))
    
    else:
        flash("Method is not match!")
        return redirect(url_for("data_tv"))

@app.route("/edit_tv", methods=["GET", "POST"])
@require_api_token
def edit_tv():
    id = request.form["edit_this"]
    sql = db()
    getted = sql.readone_tv(id)
    return render_template(
        "dashboard/tv/edit_tv.html",
        pData = getted,
        oldID = id)

@app.route("/sayonara_tv", methods=["POST"])
def sayonara_tv():
    sql = db()
    id = request.form["del_this"]
    sql.remove_tv(id)
    flash("The data are deleted!")
    return redirect(url_for("data_tv"))

@app.route("/ganti_tv", methods=["POST"])
def ganti_tv():
    sql = db()
    _id = request.form["hidid"]
    _tvs_name = request.form["txtName"]
    _genre = ', '.join(request.form.getlist('genre'))
    _rdate = request.form["txtRDate"]
    _teps = request.form["txtEps"]
    _director = request.form["txtDirector"]
    _plot = request.form["txtPlot"]
    _poster = request.files["picture"]
    if(request.method == "POST"):
        pic = _poster.filename
        photo = pic.replace("'", "")
        picture = photo.replace(" ", "_")
        if picture.lower().endswith(('.png', '.jpg', '.jpeg')):
            save_photo = photos.save(_poster)
            if save_photo:
                if(sql.edit_tv(_id, _tvs_name, _genre, 
                _director, _teps, _rdate, _plot, picture)):
                    flash("All data are updated!")
                    return redirect(url_for("data_tv"))
                else:
                    flash("All data are not updated!")
                    return redirect(url_for("data_tv"))
    
    else:
        flash("Method not POST!")
        return redirect(url_for("data_tv"))

@app.route("/data_tv")
@require_api_token
def data_tv():
    sql = db()
    getall = sql.read_tv()
    print(getall)
    return render_template("dashboard/tv/data_tv.html", dTv = getall)



if __name__ == "__main__":
    app.run(debug=True)