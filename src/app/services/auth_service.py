import os
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from flask_mail import Message
from itsdangerous import SignatureExpired, BadSignature
from src.app.models import User, Student, Teacher, Enrollment, Schedule, Course
from src.app.extensions import db, mail, serializer
from src.utils import APIException

class AuthService:
    @staticmethod
    def register_admin(data):
        if User.query.filter_by(email=data['email']).first():
            raise APIException("El correo ya está registrado", 400)

        admin = User(
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email'],
            password=generate_password_hash(data['password']),
            role='admin',
            status='approved'
        )
        db.session.add(admin)
        db.session.commit()
        return {"message": "Administrador registrado exitosamente"}

    @staticmethod
    def register_student(data):
        if User.query.filter_by(email=data['email']).first():
            raise APIException("El correo ya está registrado", 400)

        valid_periods = ['Primer', 'Segundo', 'Tercer', 'Cuarto']
        if data.get('period') not in valid_periods:
            raise APIException("Periodo inválido", 400)

        user = User(
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email'],
            password=generate_password_hash(data['password']),
            role='student',
            status='pending',
            location=data.get('location')
        )
        db.session.add(user)
        db.session.flush()

        student = Student(
            user_id=user.id,
            phone=data['phone'],
            grade_level_id=data['grade_level_id'],
            period=data['period']
        )
        db.session.add(student)

        # Auto-enrollment logic
        schedules = Schedule.query.filter_by(grade_level_id=student.grade_level_id).all()
        for schedule in schedules:
            enrollment_exists = Enrollment.query.filter_by(
                student_id=student.user_id,
                course_id=schedule.course_id
            ).first()
            if not enrollment_exists:
                enrollment = Enrollment(
                    student_id=student.user_id,
                    course_id=schedule.course_id,
                    created_by=user.id
                )
                db.session.add(enrollment)

        db.session.commit()
        return {"message": "Solicitud de registro como estudiante enviada"}

    @staticmethod
    def register_teacher(data):
        if User.query.filter_by(email=data['email']).first():
            raise APIException("El correo ya está registrado", 400)

        course_id = int(data['course_id'])
        course = Course.query.get(course_id)
        if not course:
            raise APIException("Curso no encontrado", 404)

        user = User(
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email'],
            password=generate_password_hash(data['password']),
            role='teacher',
            status='pending',
            location=data['location']
        )
        db.session.add(user)
        db.session.flush()

        teacher = Teacher(
            user_id=user.id,
            phone=data['phone']
        )
        db.session.add(teacher)
        db.session.flush()

        course.teacher_id = teacher.user_id
        db.session.commit()
        return {"message": "Solicitud de registro como profesor enviada"}

    @staticmethod
    def login(email, password, role):
        user = User.query.filter_by(email=email, role=role).first()
        
        if not user:
            raise APIException(f"{role.capitalize()} no encontrado", 404)
        
        if not check_password_hash(user.password, password):
            raise APIException("Contraseña incorrecta", 401)
        
        if role != 'admin' and user.status != "approved":
            raise APIException("Cuenta no aprobada", 403)

        access_token = create_access_token(identity=str(user.id))
        
        return {
            "access_token": access_token,
            "user": user.serialize()
        }

    @staticmethod
    def forgot_password(email):
        user = User.query.filter_by(email=email).first()
        if not user:
            raise APIException("Usuario no encontrado", 404)

        token = serializer.dumps(user.id, salt="recuperar-clave")
        frontend_url = os.getenv("FRONTEND_URL", "http://localhost:3000")
        reset_url = f"{frontend_url}/reset-password/{token}"

        msg = Message(
            subject="Recuperación de contraseña - Alpha School",
            sender=os.getenv("MAIL_DEFAULT_SENDER"),
            recipients=[email],
            body=f"Hola {user.first_name},\n\nPara restablecer tu contraseña haz clic en el siguiente enlace:\n{reset_url}\n\nEste enlace expirará en 10 minutos."
        )
        try:
            mail.send(msg)
        except Exception as e:
            raise APIException(f"Error al enviar correo: {str(e)}", 500)
            
        return {"msg": "Correo de recuperación enviado con éxito"}

    @staticmethod
    def reset_password(token, new_password):
        try:
            user_id = serializer.loads(token, salt="recuperar-clave", max_age=600)
        except (SignatureExpired, BadSignature):
            raise APIException("Token inválido o expirado", 400)

        user = User.query.get(user_id)
        if not user:
            raise APIException("Usuario no encontrado", 404)

        user.password = generate_password_hash(new_password)
        db.session.commit()
        return {"message": "Contraseña actualizada exitosamente"}
