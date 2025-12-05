import os
from flask_admin import Admin
from src.app.models import User, Student, Teacher, GradeLevel, Course, Schedule, Enrollment, Attendance, Grade, Payment
from src.app.extensions import db
from flask_admin.contrib.sqla import ModelView


def setup_admin(app):
    app.secret_key = os.environ.get('FLASK_APP_KEY', 'sample key')
    app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
    admin = Admin(app, name='Alpha Admin')

    admin.add_view(ModelView(User, db.session))
    admin.add_view(ModelView(Student, db.session))
    admin.add_view(ModelView(GradeLevel, db.session))
    admin.add_view(ModelView(Teacher, db.session))
    admin.add_view(ModelView(Enrollment, db.session))
    admin.add_view(ModelView(Payment, db.session))
    admin.add_view(ModelView(Schedule, db.session))
    admin.add_view(ModelView(Attendance, db.session))
    admin.add_view(ModelView(Grade, db.session))
    admin.add_view(ModelView(Course, db.session))
