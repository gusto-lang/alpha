from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.app.services.auth_service import AuthService
from src.app.services.academic_service import AcademicService
from src.app.services.teacher_service import TeacherService
from src.app.services.student_service import StudentService
from src.app.services.admin_service import AdminService
from src.utils import APIException

api = Blueprint('api', __name__)

# --- AUTH ROUTES ---

@api.route('/register/admin', methods=['POST'])
def register_admin():
    data = request.json
    required = ['first_name', 'last_name', 'email', 'password']
    if not all(k in data for k in required):
        return jsonify({"error": "Faltan campos requeridos"}), 400
    return jsonify(AuthService.register_admin(data)), 201

@api.route('/register/student', methods=['POST'])
def register_student():
    data = request.json
    required = ['first_name', 'last_name', 'email', 'password', 'phone', 'grade_level_id', 'period', 'location']
    if not all(k in data for k in required):
        return jsonify({"error": "Faltan campos requeridos"}), 400
    return jsonify(AuthService.register_student(data)), 201

@api.route('/register/teacher', methods=['POST'])
def register_teacher():
    data = request.json
    required = ['first_name', 'last_name', 'email', 'password', 'phone', 'course_id', 'location']
    if not all(k in data for k in required):
        return jsonify({"error": "Faltan campos requeridos"}), 400
    return jsonify(AuthService.register_teacher(data)), 201

@api.route('/login/student', methods=['POST'])
def login_student():
    data = request.get_json()
    if not data.get("email") or not data.get("password"):
        return jsonify({"msg": "Email y contraseña requeridos"}), 400
    return jsonify(AuthService.login(data["email"], data["password"], role="student")), 200

@api.route('/login/teacher', methods=['POST'])
def login_teacher():
    data = request.get_json()
    if not data.get("email") or not data.get("password"):
        return jsonify({"msg": "Email y contraseña requeridos"}), 400
    return jsonify(AuthService.login(data["email"], data["password"], role="teacher")), 200

@api.route('/login/admin', methods=['POST'])
def login_admin():
    data = request.get_json()
    if not data.get("email") or not data.get("password"):
        return jsonify({"msg": "Email y contraseña requeridos"}), 400
    return jsonify(AuthService.login(data["email"], data["password"], role="admin")), 200

@api.route('/forgot-password', methods=['POST'])
def forgot_password():
    data = request.get_json()
    if not data.get("email"):
        return jsonify({"error": "Se requiere un correo electrónico"}), 400
    return jsonify(AuthService.forgot_password(data["email"])), 200

@api.route('/reset-password/<token>', methods=['POST'])
def reset_password(token):
    data = request.get_json()
    if not data.get('password'):
        return jsonify({"error": "Contraseña requerida"}), 400
    return jsonify(AuthService.reset_password(token, data['password'])), 200

# --- ACADEMIC ROUTES ---

@api.route('/setup/grade_levels', methods=['POST'])
def setup_grade_levels():
    return jsonify(AcademicService.setup_grade_levels()), 201

@api.route('/setup/courses', methods=['POST'])
def setup_courses():
    return jsonify(AcademicService.setup_courses()), 201

@api.route('/setup/schedules', methods=['POST'])
def setup_schedules():
    return jsonify(AcademicService.setup_schedules()), 201

@api.route('/setup/associate_courses_to_grades', methods=['POST'])
def associate_courses_to_grades():
    return jsonify(AcademicService.associate_courses_to_grades()), 201

@api.route('/setup/grade_levels', methods=['GET'])
def get_grade_levels():
    return jsonify(AcademicService.get_grade_levels()), 200

@api.route('/courses', methods=['GET'])
def get_courses():
    return jsonify(AcademicService.get_courses()), 200

@api.route('/periods', methods=['GET'])
def get_periods():
    return jsonify(AcademicService.get_periods()), 200

# --- TEACHER ROUTES ---

@api.route('/teacher/schedule-grid', methods=['GET'])
@jwt_required()
def get_teacher_schedule_grid():
    return jsonify(TeacherService.get_schedule_grid(get_jwt_identity())), 200

@api.route('/teacher/students', methods=['GET'])
@jwt_required()
def get_students_by_course_and_grade():
    grade_level_id = request.args.get("grade_level_id", type=int)
    course_id = request.args.get("course_id", type=int)
    if not grade_level_id or not course_id:
        return jsonify({"msg": "Faltan parámetros"}), 400
    return jsonify(TeacherService.get_students_by_course_and_grade(get_jwt_identity(), grade_level_id, course_id)), 200

@api.route('/teacher/students/attendance', methods=['GET'])
@jwt_required()
def get_students_attendance():
    grade_level_id = request.args.get("grade_level_id", type=int)
    course_id = request.args.get("course_id", type=int)
    period = request.args.get("period", type=int)
    if not grade_level_id or not course_id or not period:
        return jsonify({"error": "Faltan parámetros requeridos"}), 400
    return jsonify(TeacherService.get_students_attendance(get_jwt_identity(), grade_level_id, course_id, period)), 200

@api.route('/attendance', methods=['POST'])
@jwt_required()
def register_attendance():
    data = request.get_json()
    required = ['enrollment_id', 'date', 'status']
    if not all(k in data for k in required):
        return jsonify({"error": "Faltan campos"}), 400
    return jsonify(TeacherService.register_attendance(data)), 201

@api.route('/attendance', methods=['GET'])
@jwt_required()
def get_attendance_by_enrollment():
    enrollment_id = request.args.get('enrollment_id', type=int)
    if not enrollment_id:
        return jsonify({"error": "Falta enrollment_id"}), 400
    return jsonify(TeacherService.get_attendance_by_enrollment(enrollment_id)), 200

@api.route('/attendance/<int:attendance_id>', methods=['PUT'])
@jwt_required()
def update_attendance(attendance_id):
    data = request.get_json()
    if not data.get("status"):
        return jsonify({"error": "Falta status"}), 400
    return jsonify(TeacherService.update_attendance(attendance_id, data.get("status"))), 200

@api.route('/grade', methods=['POST'])
@jwt_required()
def post_grade():
    data = request.get_json()
    required = ['enrollment_id', 'period', 'participation', 'homework', 'midterm', 'final_exam']
    if not all(k in data for k in required):
        return jsonify({"error": "Faltan campos requeridos"}), 400
    return jsonify(TeacherService.post_grade(get_jwt_identity(), data)), 201

@api.route('/grade/<int:grade_id>', methods=['PUT'])
@jwt_required()
def update_grade(grade_id):
    data = request.get_json()
    return jsonify(TeacherService.update_grade(get_jwt_identity(), grade_id, data)), 200

@api.route('/teacher/grades', methods=['GET'])
@jwt_required()
def get_students_with_grades():
    grade_level_id = request.args.get("grade_level_id", type=int)
    course_id = request.args.get("course_id", type=int)
    period = request.args.get("period", type=int)
    if grade_level_id is None or course_id is None or period is None:
        return jsonify({"msg": "Faltan parámetros"}), 400
    return jsonify(TeacherService.get_students_with_grades(get_jwt_identity(), grade_level_id, course_id, period)), 200

# --- STUDENT ROUTES ---

@api.route('/student/schedule', methods=['GET'])
@jwt_required()
def get_student_schedule():
    return jsonify(StudentService.get_schedule(get_jwt_identity())), 200

@api.route('/student/attendance', methods=['GET'])
@jwt_required()
def get_student_attendance():
    return jsonify(StudentService.get_attendance(get_jwt_identity())), 200

@api.route('/student/grades', methods=['GET'])
@jwt_required()
def get_student_grades():
    course_id = request.args.get('course_id', type=int)
    period = request.args.get('period', type=int)
    return jsonify(StudentService.get_grades(get_jwt_identity(), course_id, period)), 200

# --- ADMIN ROUTES ---

@api.route('/pending/registrations', methods=['GET'])
@jwt_required()
def get_pending_users():
    return jsonify(AdminService.get_pending_users(get_jwt_identity())), 200

@api.route('/approve/student/<int:user_id>', methods=['PUT'])
@jwt_required()
def approve_student(user_id):
    data = request.get_json()
    if not data.get("status"):
        return jsonify({"msg": "Falta status"}), 400
    
    from src.app.models import User
    admin_id = get_jwt_identity()
    admin = User.query.get(admin_id)
    if not admin or admin.role != "admin":
        return jsonify({"msg": "Acceso no autorizado"}), 403
        
    return jsonify(AdminService.approve_user(user_id, "student", data.get("status"))), 200

@api.route('/approve/teacher/<int:user_id>', methods=['PUT'])
@jwt_required()
def approve_teacher(user_id):
    data = request.get_json()
    if not data.get("status"):
        return jsonify({"msg": "Falta status"}), 400
    
    from src.app.models import User
    admin_id = get_jwt_identity()
    admin = User.query.get(admin_id)
    if not admin or admin.role != "admin":
        return jsonify({"msg": "Acceso no autorizado"}), 403

    return jsonify(AdminService.approve_user(user_id, "teacher", data.get("status"))), 200

@api.route('/delete/user/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    return jsonify(AdminService.delete_user(get_jwt_identity(), user_id)), 200

@api.route('/admin/profile', methods=['GET'])
@jwt_required()
def get_admin_profile():
    from src.app.models import User
    user = User.query.get(get_jwt_identity())
    if not user or user.role != "admin":
        return jsonify({"msg": "Acceso no autorizado"}), 403
    return jsonify(user.serialize()), 200

@api.route('/students', methods=['GET'])
@jwt_required()
def get_approved_students():
    return jsonify(AdminService.get_users_by_role(get_jwt_identity(), "student")), 200

@api.route('/teachers', methods=['GET'])
@jwt_required()
def get_approved_teachers():
    return jsonify(AdminService.get_users_by_role(get_jwt_identity(), "teacher")), 200

@api.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    from src.app.models import User
    user = User.query.get(get_jwt_identity())
    if not user:
        return jsonify({"msg": "Usuario no encontrado"}), 404
    return jsonify(user.serialize()), 200
