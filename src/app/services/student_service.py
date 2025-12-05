from src.app.models import User, Student, Schedule, Grade
from src.utils import APIException

class StudentService:
    @staticmethod
    def get_schedule(student_id):
        user = User.query.get(student_id)
        if not user or user.role != "student" or user.status != "approved":
            raise APIException("Acceso no autorizado", 403)

        student = Student.query.get(student_id)
        if not student:
            raise APIException("Estudiante no encontrado", 404)

        schedules = Schedule.query.filter_by(grade_level_id=student.grade_level_id).all()
        bloques = ["07:00 - 09:00", "09:00 - 11:00", "11:00 - 13:00"]
        dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]

        horario = []
        for bloque in bloques:
            fila = {"bloque": bloque}
            for dia in dias:
                fila[dia] = ""
            horario.append(fila)

        for sched in schedules:
            bloque_str = f"{sched.start_time.strftime('%H:%M')} - {sched.end_time.strftime('%H:%M')}"
            for fila in horario:
                if fila["bloque"] == bloque_str:
                    fila[sched.day] = sched.course.name
                    break
        return horario

    @staticmethod
    def get_attendance(student_id):
        student = Student.query.filter_by(user_id=student_id).first()
        if not student:
            raise APIException("Estudiante no encontrado", 404)

        all_records = []
        for enrollment in student.enrollments:
            course_name = enrollment.course.name if enrollment.course else "Curso no asignado"
            teacher_name = f"{enrollment.teacher.user.first_name} {enrollment.teacher.user.last_name}" if enrollment.teacher else "Profesor no asignado"
            for att in enrollment.attendance:
                all_records.append({
                    "date": att.date.strftime('%Y-%m-%d'),
                    "status": att.status,
                    "course": course_name,
                    "teacher": teacher_name
                })
        return all_records

    @staticmethod
    def get_grades(student_id, course_id=None, period=None):
        user = User.query.get(student_id)
        if not user or user.role != "student" or user.status != "approved":
            raise APIException("Acceso no autorizado", 403)

        student = Student.query.filter_by(user_id=student_id).first()
        if not student:
            raise APIException("Estudiante no encontrado", 404)

        results = []
        for enrollment in student.enrollments:
            if course_id and enrollment.course_id != course_id:
                continue
            
            query = Grade.query.filter_by(enrollment_id=enrollment.id)
            if period:
                query = query.filter_by(period=period)
            
            grades = query.all()
            for grade in grades:
                results.append(grade.serialize())
        return results
