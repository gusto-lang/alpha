from src.app.models import User, Enrollment, Grade, Attendance, Course, Schedule, GradeLevel
from src.app.extensions import db
from src.utils import APIException
import datetime

class TeacherService:
    @staticmethod
    def get_schedule_grid(teacher_id):
        user = User.query.get(teacher_id)
        if not user or user.role != "teacher" or user.status != "approved":
            raise APIException("Acceso no autorizado", 403)

        courses = Course.query.filter_by(teacher_id=teacher_id).all()
        course_ids = [c.id for c in courses]
        schedules = Schedule.query.filter(Schedule.course_id.in_(course_ids)).all()
        grade_map = {g.id: g.name for g in GradeLevel.query.all()}

        week_days = ["LUNES", "MARTES", "MIERCOLES", "JUEVES", "VIERNES"]
        grade_names = ["Primero", "Segundo", "Tercero", "Cuarto", "Quinto"]
        grid = {grade: {day: None for day in week_days} for grade in grade_names}

        for s in schedules:
            grade_name = grade_map.get(s.grade_level_id)
            if grade_name in grid:
                course_name = s.course.name
                time_range = f"{s.start_time.strftime('%H:%M')}-{s.end_time.strftime('%H:%M')}"
                grid[grade_name][s.day.upper()] = f"{course_name} ({time_range})"
        return grid

    @staticmethod
    def get_students_by_course_and_grade(teacher_id, grade_level_id, course_id):
        user = User.query.get(teacher_id)
        if not user or user.role != "teacher" or user.status != "approved":
            raise APIException("Acceso no autorizado", 403)

        enrollments = Enrollment.query.filter_by(course_id=course_id).all()
        filtered = [
            {"enrollment_id": e.id, "student": e.student.serialize()}
            for e in enrollments if e.student.grade_level_id == grade_level_id
        ]
        return filtered

    @staticmethod
    def get_students_attendance(teacher_id, grade_level_id, course_id, period):
        # Note: period is passed but not used in filtering attendance in original code, keeping as is or improving?
        # Original code didn't use period for filtering attendance records, just required it.
        enrollments = Enrollment.query.filter_by(course_id=course_id, grade_level_id=grade_level_id).all()
        result = []
        for enrollment in enrollments:
            student = enrollment.student.serialize()
            attendance_records = Attendance.query.filter_by(enrollment_id=enrollment.id).all()
            result.append({
                "enrollment_id": enrollment.id,
                "student": student,
                "attendance": [a.serialize() for a in attendance_records]
            })
        return result

    @staticmethod
    def register_attendance(data):
        try:
            attendance_date = datetime.datetime.strptime(data['date'], "%Y-%m-%d").date()
        except ValueError:
            raise APIException("Formato de fecha inválido. Use YYYY-MM-DD.", 400)

        valid_status = ["asistio", "falto", "tardanza", "no registrado"]
        if data['status'] not in valid_status:
            raise APIException("Estado de asistencia no válido.", 400)

        enrollment = Enrollment.query.get(data['enrollment_id'])
        if not enrollment:
            raise APIException("Matrícula no encontrada.", 404)

        existing = Attendance.query.filter_by(enrollment_id=data['enrollment_id'], date=attendance_date).first()
        if existing:
            existing.status = data['status']
            msg = "Asistencia actualizada exitosamente."
        else:
            attendance = Attendance(enrollment_id=data['enrollment_id'], date=attendance_date, status=data['status'])
            db.session.add(attendance)
            msg = "Asistencia registrada exitosamente."
        
        db.session.commit()
        return {"message": msg}

    @staticmethod
    def get_attendance_by_enrollment(enrollment_id):
        records = Attendance.query.filter_by(enrollment_id=enrollment_id).all()
        return [a.serialize() for a in records]

    @staticmethod
    def update_attendance(attendance_id, new_status):
        valid_status = ["asistio", "falto", "tardanza", "no registrado"]
        if new_status not in valid_status:
            raise APIException("Estado de asistencia no válido.", 400)

        attendance = Attendance.query.get(attendance_id)
        if not attendance:
            raise APIException("Asistencia no encontrada.", 404)

        attendance.status = new_status
        db.session.commit()
        return {"message": "Asistencia actualizada exitosamente."}

    @staticmethod
    def post_grade(teacher_id, data):
        enrollment = Enrollment.query.get(data['enrollment_id'])
        if not enrollment:
            raise APIException("Inscripción no encontrada.", 404)

        existing = Grade.query.filter_by(enrollment_id=data['enrollment_id'], period=data['period']).first()
        if existing:
            raise APIException("Ya existe una nota para este estudiante y periodo.", 409)

        average = round(
            data['participation'] * 0.15 +
            data['homework'] * 0.20 +
            data['midterm'] * 0.30 +
            data['final_exam'] * 0.35, 2
        )

        grade = Grade(
            enrollment_id=data['enrollment_id'],
            teacher_id=teacher_id,
            period=data['period'],
            participation=data['participation'],
            homework=data['homework'],
            midterm=data['midterm'],
            final_exam=data['final_exam'],
            average=average
        )
        db.session.add(grade)
        db.session.commit()
        return {"message": "Nota registrada exitosamente."}

    @staticmethod
    def update_grade(teacher_id, grade_id, data):
        grade = Grade.query.get(grade_id)
        if not grade:
            raise APIException("Nota no encontrada", 404)
        
        # Ensure teacher_id is int for comparison
        if grade.teacher_id != int(teacher_id):
            raise APIException("No autorizado para modificar esta calificación", 403)

        grade.participation = data.get('participation', grade.participation)
        grade.homework = data.get('homework', grade.homework)
        grade.midterm = data.get('midterm', grade.midterm)
        grade.final_exam = data.get('final_exam', grade.final_exam)

        grade.average = round(
            grade.participation * 0.15 +
            grade.homework * 0.20 +
            grade.midterm * 0.30 +
            grade.final_exam * 0.35, 2
        )
        db.session.commit()
        return {"message": "Nota actualizada exitosamente"}

    @staticmethod
    def get_students_with_grades(teacher_id, grade_level_id, course_id, period):
        user = User.query.get(teacher_id)
        if not user or user.role != "teacher" or user.status != "approved":
            raise APIException("Acceso no autorizado", 403)

        course = Course.query.get(course_id)
        if not course:
            raise APIException(f"Curso con id {course_id} no encontrado", 404)
        if course.teacher_id != int(teacher_id):
            raise APIException(f"Acceso denegado. Curso pertenece al profesor {course.teacher_id}", 403)

        enrollments = Enrollment.query.filter_by(course_id=course_id).all()
        filtered_enrollments = [e for e in enrollments if e.student and e.student.grade_level_id == grade_level_id]

        result = []
        for enrollment in filtered_enrollments:
            student = enrollment.student.serialize() if enrollment.student else None
            grade = Grade.query.filter_by(enrollment_id=enrollment.id, period=period).first()
            result.append({
                "enrollment_id": enrollment.id,
                "student": student,
                "grade": grade.serialize() if grade else None
            })
        return result
