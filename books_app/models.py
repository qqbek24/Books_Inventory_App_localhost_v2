from werkzeug.security import generate_password_hash, check_password_hash
from books_app import db


class Users(db.Model):
    __tablename__ = 'users'
    User_Name = db.Column(db.String(55), primary_key=True, nullable=False, unique=True)
    Password = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f'<{self.__class__.__name__}>: {self.User_Name}'


class Inventory(db.Model):
    __tablename__ = 'books_inventory'
    title = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255))
    date_of_publication = db.Column(db.String(255))
    isbn = db.Column(db.String(255))
    pages = db.Column(db.String(255))
    cover = db.Column(db.String(255))
    language = db.Column(db.String(255))
    product_id = db.Column(db.Integer, primary_key=True)

    def __repr__(self):
        return f'<{self.__class__.__name__}>: {self.title} {self.author}'


class app_user:

    def user_add(self, app_user_pass):
        try:
            app_user_login = self
            if app_user_login == "":
                return 'input user login'
            else:
                user = db.session.query(Users).filter_by(User_Name=app_user_login).first()
                if user:
                    return 'User ' + app_user_login + ' is already on the List'
                else:
                    app_user_pass_hash = generate_password_hash(app_user_pass, 'sha256')
                    new_user = Users(User_Name=app_user_login, Password=app_user_pass_hash)
                    db.session.add(new_user)
                    db.session.commit()
                    return 'Successfully Added!'
        except Exception as exc:
            return 'Unexpected error: {}'.format(exc)

    def user_pass_check(self, app_user_pass):
        try:
            app_user_login = self
            if app_user_pass == "" or app_user_login == "":
                return 'input user password and login'
            else:
                user = db.session.query(Users).filter_by(User_Name=app_user_login).first()
                app_user_pass_hash = user.Password
                app_user_pass_hash_check = check_password_hash(app_user_pass_hash, app_user_pass)
                return app_user_pass_hash_check
        except Exception as exc:
            return 'Unexpected error: {}'.format(exc)

    def user_delete(self):
        try:
            del_user_login = self
            if del_user_login == "":
                return 'input user login to delete'
            else:
                user = db.session.query(Users).filter_by(User_Name=del_user_login).first()
                if user:
                    db.session.delete(user)
                    db.session.commit()
                    return 'Successfully Deleted!'
                else:
                    return 'User ' + del_user_login + ' is not on the List'
        except Exception as exc:
            return 'Unexpected error: {}'.format(exc)

    def user_change_password(self, user_credentials):
        pass


class books:

    def books_insert(self):
        pass
