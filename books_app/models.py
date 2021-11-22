from werkzeug.security import generate_password_hash, check_password_hash
# from books_app.myconnutils import my_db_connection
from books_app import db


class user(db.Model):
    __tablename__ = 'users'
    User_Name = db.Column(db.String(55), primary_key=True, nullable=False)
    Password = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f'<{self.__class__.__name__}>: {self.User_Name}'


class inventory(db.Model):
    __tablename__ = 'books_inventory'
    title = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255))
    date_of_publication = db.Column(db.String(255))
    isbn = db.Column(db.String(255))
    nr_of_pages = db.Column(db.String(255))
    link_cover = db.Column(db.String(255))
    language = db.Column(db.String(255))
    product_id = db.Column(db.Integer, primary_key=True)

    def __repr__(self):
        return f'<{self.__class__.__name__}>: {self.title} {self.author}'


# class app_user:
#
#     def user_add(self, app_user_pass):
#         app_user_login = self
#         sql_formula = "INSERT INTO invent_system_users(User_Name, Pass) Values(%s,%s)"
#         if app_user_login == "":
#             return 'input user login'
#         else:
#             my_db = my_db_connection()
#             my_cursor = my_db.cursor()
#             my_cursor.execute("SELECT COUNT(1) FROM invent_system_users WHERE User_Name = %s;", [app_user_login])
#             if my_cursor.fetchone()[0]:
#                 return 'User ' + app_user_login + ' is already on the List'
#             else:
#                 app_user_pass_hash = generate_password_hash(app_user_pass, 'sha256')
#                 user_credentials = (app_user_login, app_user_pass_hash)
#                 app_user.query_execute(sql_formula, user_credentials)
#                 my_cursor.close()
#                 my_db.close()
#                 return 'Successfully Added!'
#
#     def user_pass_check(self, app_user_pass):
#         app_user_login = self
#         if app_user_pass == "" or app_user_login == "":
#             return 'input user password and login'
#         else:
#             app_user_pass_hash = app_user.user_pass_hash(app_user_login)
#             app_user_pass_hash_check = check_password_hash(app_user_pass_hash, app_user_pass)
#             if app_user_pass_hash_check is True:
#                 return True
#             else:
#                 return False
#
#     def user_pass_hash(self):
#         app_user_login = self
#         sql_formula = 'SELECT Pass FROM invent_system_users WHERE User_Name= %s;'
#         my_db = my_db_connection()
#         my_cursor = my_db.cursor()
#         my_cursor.execute(sql_formula, [app_user_login])
#         app_user_pass_hash = my_cursor.fetchone()[0]
#         my_cursor.close()
#         my_db.close()
#         return app_user_pass_hash
#
#     def user_delete(self):
#         del_user_login = self
#         sql_formula = "DELETE FROM invent_system_users WHERE User_Name = %s;"
#         if del_user_login == "":
#             return 'input user login to delete'
#         else:
#             my_db = my_db_connection()
#             my_cursor = my_db.cursor()
#             my_cursor.execute("SELECT COUNT(1) FROM invent_system_users WHERE User_Name = %s;", [del_user_login])
#             if my_cursor.fetchone()[0]:
#                 app_user.query_execute(sql_formula, del_user_login)
#                 my_cursor.close()
#                 my_db.close()
#                 return 'Successfully Deleted!'
#             else:
#                 return 'User ' + del_user_login + ' is not on the List'
#
#     def user_change_password(self, user_credentials):
#         pass
#
#     def query_execute(self, user_arg):
#         my_cursor.execute(self, user_arg)
#         my_db.commit()
#
#
# class books:
#
#     def books_insert(self):
#         pass
