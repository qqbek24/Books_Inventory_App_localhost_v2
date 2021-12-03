from flask import render_template, request, redirect, url_for, flash, session, escape
# from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user

from config import Config
from books_app.models import Users, Inventory, app_user
from books_app import app, db
import json
from urllib.request import urlopen
import string

# TODO: HTML Error handling improve
#       unit tests with pytest
#       switch to SQLAlchemy

# app.permanent_session_lifetime = True


@app.route('/')
def login():
    if 'username' in session:
        username_session = escape(session['username']).capitalize()
        return render_template('index.html', session_user_name=username_session)
    return render_template('login.html')


@app.route('/home')
def home():
    return render_template('index.html')


@app.route('/register', methods=['POST'])
def register():
    try:
        username_form = request.form['username']
        password_form1 = request.form['password']
        password_form2 = request.form['rep_password']
        if password_form1 != password_form2:
            flash('Incorrect passwords. Password 1 must be equal to Password 2')
        else:
            if username_form == "" and password_form1 == "" or password_form2 == "":
                flash('Please fill out the fields')
            else:
                if request.method == 'POST':
                    db_res_information = app_user.user_add(username_form, password_form1)
                    if db_res_information != 'Successfully Added!':
                        flash(db_res_information)
                        return redirect(url_for('registered'))
                    else:
                        flash(db_res_information)
                        return redirect(url_for('logout'))

    except Exception as exc:
        flash('Unexpected error: {}'.format(exc))
        return render_template('register.html')


@app.route('/registered', methods=['GET'])
def registered():
    if request.method == 'GET':
        session.clear()
        return render_template('register.html')


@app.route('/log', methods=['POST'])
def log():
    try:
        username_form = request.form['username']
        password_form = request.form['password']
        if username_form == "" and password_form == "":
            flash('Please fill out the fields')
        else:
            if request.method == 'POST':
                if 'username' in session:
                    return redirect(url_for('index'))
                if request.method == 'POST':
                    user = db.session.query(Users).filter_by(User_Name=username_form).first()
                    if user:
                        password_form_hash_checked = app_user.user_pass_check(username_form, password_form)
                        if password_form_hash_checked is True:
                            session['username'] = request.form['username']
                            flash('Login Successfully')
                            return render_template('index.html')
                        else:
                            flash('Either Username or Password_2 is Incorrect')
                            return redirect(url_for('login'))
                    else:
                        flash('Either Username or Password_1 is Incorrect')
                        return redirect(url_for('login'))

    except Exception as exc:
        # flash('Unexpected error: {}'.format(400))
        flash('Unexpected error: {}'.format(exc))
        return render_template('login.html')


@app.route('/logout', methods=['GET'])
def logout():
    if request.method == 'GET':
        session.clear()
        return render_template('login.html')


@app.route('/insert', methods=['POST'])
def insert():
    try:
        p_title = request.form['addtitle']
        p_author = request.form['addauthor']
        p_date_pub = request.form['adddatepub']
        p_isbn = request.form['addisbn']
        p_pages = request.form['addpages']
        p_cover = request.form['addcover']
        p_lang = request.form['addlang']

        if p_title == "":
            return render_template('index.html')
        elif p_author == "":
            return render_template('index.html')
        elif p_date_pub == "":
            return render_template('index.html')
        elif p_isbn == "":
            return render_template('index.html')
        elif p_pages == "":
            return render_template('index.html')
        elif p_cover == "":
            return render_template('index.html')
        elif p_lang == "":
            return render_template('index.html')
        else:
            if request.method == 'POST':
                item = db.session.query(Inventory).filter_by(title=p_title).first()
                if item:
                    flash(p_title + ' is already on the list')
                    return render_template('index.html')
                else:
                    new_title = Inventory(
                        title=p_title, author=p_author,
                        date_of_publication=p_date_pub, isbn=p_isbn,
                        pages=p_pages, cover=p_cover, language=p_lang
                    )
                    db.session.add(new_title)
                    db.session.commit()
                    flash(p_title + ', ' + p_author + ', ' + p_date_pub + ', Successfully saved!')
                    return render_template('index.html')
            else:
                return render_template('index.html')

    except Exception as exc:
        flash('Unexpected error: {}'.format(exc))
        return render_template('index.html')


@app.route('/searchall', methods=['POST'])
def searchall():
    try:
        if request.method == 'POST':
            data = db.session.query(Inventory.title, Inventory.author,
                                    Inventory.date_of_publication, Inventory.isbn,
                                    Inventory.pages, Inventory.cover,
                                    Inventory.language, Inventory.product_id).all()
            return render_template('index.html', products=data)

    except Exception as exc:
        flash('Unexpected error: {}'.format(exc))
        return render_template('index.html')


@app.route('/search_title', methods=['POST'])
def search_title():
    try:
        prod_search = request.form['searchprod']
        if prod_search == "":
            flash('Please fill out the search field ')
            return render_template('index.html')
        else:
            if request.method == 'POST':
                items = db.session.query(Inventory).filter(Inventory.title.contains(prod_search))
                if items:
                    flash(prod_search + ' Found!')
                    items = db.session.query(
                        Inventory.title, Inventory.author,
                        Inventory.date_of_publication, Inventory.isbn,
                        Inventory.pages, Inventory.cover,
                        Inventory.language, Inventory.product_id
                    ).filter(Inventory.title.contains(prod_search))
                    return render_template('index.html', prodnames=items)
                else:
                    flash('There no such product as ' + prod_search)
                    return render_template('index.html')

    except Exception as exc:
        flash('Unexpected error: {}'.format(exc))
        return render_template('index.html')


@app.route('/search_author', methods=['POST'])
def search_author():
    try:
        prod_search = request.form['searchprod']
        if prod_search == "":
            flash('Please fill out the search field ')
            return render_template('index.html')
        else:
            if request.method == 'POST':
                items = db.session.query(Inventory).filter(Inventory.author.contains(prod_search))
                if items:
                    flash(prod_search + ' Found!')
                    items = db.session.query(
                        Inventory.title, Inventory.author,
                        Inventory.date_of_publication, Inventory.isbn,
                        Inventory.pages, Inventory.cover,
                        Inventory.language, Inventory.product_id
                    ).filter(Inventory.author.contains(prod_search))
                    return render_template('index.html', prodnames=items)
                else:
                    flash('There no such product as ' + prod_search)
                    return render_template('index.html')

    except Exception as exc:
        flash('Unexpected error: {}'.format(exc))
        return render_template('index.html')


@app.route('/search_language', methods=['POST'])
def search_language():
    try:
        prod_search = request.form['searchprod']
        if prod_search == "":
            flash('Please fill out the search field ')
            return render_template('index.html')
        else:
            if request.method == 'POST':
                items = db.session.query(Inventory).filter(Inventory.language.contains(prod_search))
                if items:
                    flash(prod_search + ' Found!')
                    items = db.session.query(
                        Inventory.title, Inventory.author,
                        Inventory.date_of_publication, Inventory.isbn,
                        Inventory.pages, Inventory.cover,
                        Inventory.language, Inventory.product_id
                    ).filter(Inventory.language.contains(prod_search))
                    return render_template('index.html', prodnames=items)
                else:
                    flash('There no such product as ' + prod_search)
                    return render_template('index.html')

    except Exception as exc:
        flash('Unexpected error: {}'.format(exc))
        return render_template('index.html')


@app.route('/delete', methods=['POST'])
def delete():
    try:
        del_title = request.form['titlename']
        if del_title == "":
            return render_template('index.html')
        else:
            if request.method == 'POST':
                item = db.session.query(Inventory).filter_by(title=del_title).first()
                if item:
                    db.session.delete(item)
                    db.session.commit()
                    flash('Successfully Deleted!')
                    return render_template('index.html')
                else:
                    flash('Record ' + request.form['titlename'] + ' is not on the List')
        return render_template('index.html')

    except Exception as exc:
        flash('Unexpected error: {}'.format(exc))
        return render_template('index.html')


@app.route('/update', methods=['POST'])
def update():
    try:
        title_p = request.form['updtitle']
        author_p = request.form['updauthor']
        date_pub_p = request.form['upddatepub']
        isbn_p = request.form['updisbn']
        pages_p = request.form['updpages']
        cover_p = request.form['updcover']
        lang_p = request.form['updlang']
        if title_p == "":
            return render_template('index.html')
        elif author_p == "":
            return render_template('index.html')
        elif date_pub_p == "":
            return render_template('index.html')
        elif isbn_p == "":
            return render_template('index.html')
        elif pages_p == "":
            return render_template('index.html')
        elif cover_p == "":
            return render_template('index.html')
        elif lang_p == "":
            return render_template('index.html')
        else:
            if request.method == 'POST':
                item = db.session.query(Inventory).filter(Inventory.title == title_p).first()
                if item:
                    flash(title_p + ' Found!')
                    item.title = title_p
                    item.author = author_p
                    item.date_of_publication = date_pub_p
                    item.isbn = isbn_p
                    item.pages = pages_p
                    item.cover = cover_p
                    item.language = lang_p
                    db.session.commit()
                    flash('Successfully Updated')
                    return render_template('index.html')
                else:
                    flash('There no such product as ' + title_p)
                return render_template('index.html')

    except Exception as exc:
        flash('Unexpected error: {}'.format(exc))
        return render_template('index.html')


@app.route('/searchapi', methods=['POST'])
def searchapi():
    try:
        q_value = request.form['value_str']
        req_api = request_ggl_bks_api(q_value)
        req_jsn = json.load(req_api)
        data = ret_from_ggl_bks_jsn(req_jsn)
        return render_template('index.html', apiproducts=data)

    except Exception as exc:
        flash('Unexpected error: {}'.format(exc))
        return render_template('index.html')


def request_ggl_bks_api(form_value):
    # try:
    q_value = form_value.translate({ord(c): None for c in string.whitespace})
    google_api_key = Config.GOOGLE_BOOKS_API_KEY
    req_params = ('?q=' + q_value + '&maxResults=40' + '&key=' + google_api_key)
    req_api = urlopen("https://www.googleapis.com/books/v1/volumes" + req_params)
    return req_api

    # except Exception as exc:
    #     flash('Unexpected error: {}'.format(exc))
    #     return req_api


def ret_from_ggl_bks_jsn(req_jsn):
    items_req_jsn = req_jsn["items"]
    x = len(items_req_jsn)
    for i in range(0, x):
        volume_info = items_req_jsn[i]["volumeInfo"]
        volume_info_cover = "" if "imageLinks" not in volume_info else volume_info["imageLinks"]

        p_title = "" if "title" not in volume_info else volume_info["title"]
        p_subtitle = "" if "subtitle" not in volume_info else " - " + volume_info["subtitle"]
        title_subtitle = p_title + p_subtitle
        p_pub_date = "none date" if "publishedDate" not in volume_info else volume_info["publishedDate"]
        p_page_count = 0 if "pageCount" not in volume_info else volume_info["pageCount"]
        p_thumbnail = "none link" if "thumbnail" not in volume_info_cover else volume_info_cover["thumbnail"]
        p_language = "none lang" if "language" not in volume_info else volume_info["language"]

        if "authors" not in volume_info:
            prettify_author = ""
        else:
            p_author = volume_info["authors"]
            prettify_author = p_author if len(p_author) > 1 else p_author[0]

        if "industryIdentifiers" not in volume_info:
            volume_info_id = "0"
        else:
            volume_info_id = volume_info["industryIdentifiers"]

        if len(volume_info_id) > 1:
            for x_id in range(0, len(volume_info_id)):
                id_cds = volume_info_id[x_id]
                id_cdt = 0 if "identifier" not in id_cds else id_cds["identifier"]
                if len(id_cdt) == 13:
                    p_identifier = id_cdt
        else:
            volume_info_isbn = volume_info_id[0]
            req_identifier = "none isbn" if "identifier" not in volume_info_isbn else volume_info_isbn["identifier"]
            p_identifier = req_identifier if len(req_identifier) > 1 else req_identifier[1]

        title_str = title_subtitle
        author_str = prettify_author
        pubdate_str = p_pub_date
        id_str = p_identifier
        page_str = p_page_count
        thumb_str = p_thumbnail
        lang_str = p_language

        t1 = title_str, author_str, pubdate_str, id_str, page_str, thumb_str, lang_str
        if i == 0:
            data = [t1]
        else:
            data += [t1]
    data_bks = data
    return data_bks
