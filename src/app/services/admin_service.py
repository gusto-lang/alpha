from src.app.models import User, Student, Teacher, Course
from src.app.extensions import db
from src.utils import APIException

class AdminService:
    @staticmethod
    def get_pending_users(admin_id):
        admin = User.query.get(admin_id)
        if not admin or admin.role != "admin":
            raise APIException("Acceso no autorizado", 403)
        
        pending_users = User.query.filter(User.status == "pending", User.role.in_(["student", "teacher"])).all()
        return [user.serialize() for user in pending_users]

    @staticmethod
    def approve_user(user_id, role, status):
        user = User.query.filter_by(id=user_id, role=role).first()
        if not user:
            raise APIException(f"{role.capitalize()} no encontrado", 404)
        
        if status not in ["approved", "rejected"]:
            raise APIException("Estado inválido. Usa 'approved' o 'rejected'.", 400)
        
        user.status = status
        db.session.commit()
        return {"msg": f"Estado del {role} actualizado a '{status}'"}

    @staticmethod
    def delete_user(admin_id, user_id):
        admin = User.query.get(admin_id)
        if not admin or admin.role != "admin":
            raise APIException("Acceso no autorizado", 403)

        user = User.query.get(user_id)
        if not user:
            raise APIException("Usuario no encontrado", 404)

        if user.role == "student":
            student = Student.query.filter_by(user_id=user.id).first()
            if student: db.session.delete(student)
        
        if user.role == "teacher":
            teacher = Teacher.query.filter_by(user_id=user.id).first()
            if teacher:
                course = Course.query.filter_by(teacher_id=teacher.user_id).first()
                if course: course.teacher_id = None
                db.session.delete(teacher)
        
        db.session.delete(user)
        db.session.commit()
        return {"msg": "Usuario eliminado correctamente"}

    @staticmethod
    def get_users_by_role(admin_id, role):
        admin = User.query.get(admin_id)
        if not admin or admin.role != "admin":
            raise APIException("Acceso no autorizado", 403)
        
        users = User.query.filter_by(role=role, status="approved").all()
        return [u.serialize() for u in users]
