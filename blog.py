from flask import Flask,render_template,flash,redirect,url_for,session,logging,request
from flask_mysqldb import MySQL 
from wtforms import Form,StringField,TextAreaField,PasswordField,validators
from passlib.hash import sha256_crypt
from functools import wraps

# kulanıcı giriş decoratır'ı
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "logged_in" in session:
            return f(*args, **kwargs)
        else:
            flash("Bu sayfayı görüntülemek için lütfen Giriş Yapın","danger")
            return redirect(url_for("login"))
    return decorated_function


# kullanıcı kayıt formu
class RegisterForm(Form):
    name = StringField("İsim  Soyisim",validators = [validators.Length(min = 4 ,max = 25)])
    username = StringField("Kulanıcı Adı",validators = [validators.Length(min = 4 ,max = 35),])
    email = StringField("Email Adresi",validators = [validators.Email(message="Lütfen geçerli bir email adresi giriniz...")])
    password = PasswordField("Password",validators = [
        validators.DataRequired(message="Lütfen bir parola belirleyin..."),
        validators.EqualTo(fieldname="confirm",message="Parolanız uyuşmuyor...")
    ])
    confirm = PasswordField("Parola Doğrula")

# login form 
class LoginForm(Form):
    username = StringField("Kulanıcı Adı")
    password = PasswordField("Parola")

class ContactForm(Form):
    name = StringField("Adınız")
    username = StringField("Kulanıcı Adınız")
    mesaj = StringField("Mesaj")



app = Flask(__name__)
app.secret_key = "serdarblog"
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = ""
app.config["MYSQL_DB"] = "serdarblog"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"
mysql = MySQL(app)

@app.route("/")
def index():
    cursor = mysql.connection.cursor()
    sorgu = "Select * from articles"
    result = cursor.execute(sorgu)
    if result > 0:
        articless = cursor.fetchall()
        return render_template("index.html",articless = articless)
    else:
        return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")


#kontrol paneli
@app.route("/dashboard")
@login_required
def dashboard():
    cursor = mysql.connection.cursor()
    sorgu = "Select * From articles where author = %s"
    result = cursor.execute(sorgu,(session["username"],))

    if result > 0:
        articles = cursor.fetchall()
        return render_template("dashboard.html",articles = articles)
    else:
        return render_template("dashboard.html")


#register olma
@app.route("/register",methods = ("GET","POST"))
def register():
    form = RegisterForm(request.form)

    if request.method == "POST" and form.validate():
        name = form.name.data
        email = form.email.data
        username = form.username.data
        password = sha256_crypt.encrypt(form.password.data)

        cursor = mysql.connection.cursor()
        sorgu = "Insert into users(name,email,username,password) VALUES(%s,%s,%s,%s)"

        cursor.execute(sorgu,(name,email,username,password))
        mysql.connection.commit()
        cursor.close()
        flash("başarıyla kayıt yaptınız...","success")
        return redirect(url_for("login"))
    
    else:
        return render_template("register.html",form = form  )



# login işlemi
@app.route("/login", methods=["GET","POST"])
def login():
    form = LoginForm(request.form)
    if request.method == "POST":
        username = form.username.data
        password_entered = form.password.data

        cursor = mysql.connection.cursor()

        sorgu = "Select * From users where username = %s"

        result = cursor.execute(sorgu,(username,))

        if result > 0:
            data = cursor.fetchone()
            real_password = data["password"]
            if sha256_crypt.verify(password_entered,real_password):
                flash("Başarıyla Giriş Yaptınız...","success")
                session["logged_in"] =  True
                session["username"] = username
                return redirect(url_for("index"))

            else:
                flash("Paralanızı yanlış girdiniz...","danger")
                return redirect(url_for("login"))

        else:
            flash("kullanıcı adınız yanlış...","danger")
            return redirect(url_for("login"))
        
    else:
        return render_template("login.html",form = form)
    


# detay sayfası
@app.route("/article/<string:id>")
def article(id):
    cursor = mysql.connection.cursor()
    sorgu = "Select * from articles where id = %s"
    result = cursor.execute(sorgu,(id,))
    if result > 0:
        article = cursor.fetchone()
        return render_template("article.html",article = article)
    else:
        return render_template("article.html")



# logout işlemi 
@app.route("/logout")
def logout():
    session.clear()
    flash("Çıkış Yapıldı" , "info")
    return redirect(url_for("index"))



# makale ekleme 
@app.route("/addarticle",methods=["GET","POST"])
def addarticle():
    form = ArticleForm(request.form)
    if request.method == "POST" and form.validate():
        title = form.title.data
        content = form.content.data
        cursor = mysql.connection.cursor()

        sorgu = "Insert into articles(title,author,content) VALUES(%s,%s,%s)"

        cursor.execute(sorgu,(title,session["username"],content))

        mysql.connection.commit()

        cursor.close()
        flash("makale başarıyla eklendi","success")
        return redirect(url_for("dashboard"))

    return render_template("addarticle.html",form = form)



#makkale sil
@app.route("/delete/<string:id>")
@login_required
def delete(id):
    cursor = mysql.connection.cursor()
    sorgu = "Select * from articles where author = %s and id = %s"
    result = cursor.execute(sorgu,(session["username"],id))
    if result > 0:
        sorgu2 = "Delete from articles where id = %s"
        cursor.execute(sorgu2,(id,))
        mysql.connection.commit()
        return redirect(url_for("dashboard"))
    else:
        flash("böyle bir makale yok veya bu işlemi yapmak için yetkiniz yok.","danger")
        return redirect(url_for("index"))
    

    
# update işlemi
@app.route("/edit/<string:id>",methods = ["GET","POST"])
@login_required
def edit(id):
    if request.method == "GET":
        cursor = mysql.connection.cursor()

        sorgu = "Select * From articles where id = %s and author = %s"

        result = cursor.execute(sorgu,(id,session["username"]))

        if result == 0:
            flash("Böyle bir makale yok veya bu işlemi yapmaya yetkiniz yok","danger")
            return redirect(url_for("index"))
        else:
            article = cursor.fetchone()
            form = ArticleForm()

            form .title.data = article["title"]
            form.content.data = article["content"]
            return render_template("update.html",form = form)
    else:
        # POST REQUEST
        form = ArticleForm(request.form)
        newtitle = form.title.data
        newcontent = form.content.data
        sorgu2 = "Update articles Set title = %s , content = %s where id = %s"
        cursor = mysql.connection.cursor()
        cursor.execute(sorgu2,(newtitle,newcontent,id))
        cursor.connection.commit()
        flash("Makale Barıyla Güncellendi...","success")
        return redirect(url_for("dashboard"))





#makale form
class ArticleForm(Form):
    title = StringField("Makale Başlığı",validators=[validators.length(min= 5 ,max =100)])
    content = TextAreaField("Makale İçreği", validators=[validators.length(min=10)])

    

#makkale sayfası
@app.route("/articles")
def articles():
    cursor = mysql.connection.cursor()
    sorgu = "Select * from articles"
    result = cursor.execute(sorgu)
    if result > 0:
        articles = cursor.fetchall()
        return render_template("articles.html",articles = articles)
    else:
        return render_template("articles.html")
    

# makale arama
@app.route("/search", methods = ["GET","POST"])
def search():
    if request.method == "GET":
        flash("Bu sayfaya bu şekilde ulaşılamaz.")
        return redirect(url_for("index"))
    else:
        keyword = request.form.get("keyword")
        cursor = mysql.connection.cursor()
        sorgu = "Select * From articles where title like '%" + keyword + "%'"

        result = cursor.execute(sorgu)  
        if result == 0:
            flash("Aranan kelimeye uygun makale bulunamadı...","warning")
            return redirect(url_for("articles"))
        else:
            articles = cursor.fetchall()
            return render_template("articles.html",articles = articles)
        
# contact
@app.route("/contact",methods = ["GET","POST"])
def contact():
    contact = ContactForm(request.form)
    if request.method == "POST":
        name = contact.name.data
        username = contact.username.data
        mesaj = contact.mesaj.data

        cursor = mysql.connection.cursor()

        sorgu = "Insert into contact(name,username,mesaj) VALUES(%s,%s,%s)"

        cursor.execute(sorgu,(name,username,mesaj))

        mysql.connection.commit()

        cursor.close()
        flash("başarıyla yorum yapıldı","success")
        return redirect(url_for("index")) 

    else:
        return render_template("contact.html", contact = contact )


# dashboard arama
@app.route("/dbsearch",methods = ["GET","POST"])
def dbsearch():
    if request.method == "GET":
        flash("Bu sayfaya bu şekilde ulaşılamaz.")
        return redirect(url_for("index"))
    else:
        keyword = request.form.get("keyword")
        cursor = mysql.connection.cursor()
        sorgu = "Select * From articles where title like '%" + keyword + "%'"

        result = cursor.execute(sorgu)  
        if result == 0:
            flash("Aranan kelimeye uygun makale bulunamadı...","warning")
            return redirect(url_for("dashboard"))
        else:
            articles = cursor.fetchall()
            return render_template("dashboard.html",articles = articles)

if(__name__ == "__main__"):
    app.run(debug=True)