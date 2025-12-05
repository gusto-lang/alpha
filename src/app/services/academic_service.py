from src.app.models import GradeLevel, Course, Schedule
from src.app.extensions import db
from datetime import datetime

class AcademicService:
    @staticmethod
    def setup_grade_levels():
        niveles = [
            'Primero de secundaria', 'Segundo de secundaria', 
            'Tercero de secundaria', 'Cuarto de secundaria', 'Quinto de secundaria'
        ]
        created = False
        for i, name in enumerate(niveles, start=1):
            if not GradeLevel.query.get(i):
                db.session.add(GradeLevel(id=i, name=name))
                created = True
        
        if created:
            db.session.commit()
        return {"message": "Niveles académicos verificados/creados"}

    @staticmethod
    def setup_courses():
        course_names = [
            "Matemáticas", "Física", "Biología", "Historia", "Computación",
            "Química", "Educación Física", "Educación Cívica", "Arte",
            "Religión", "Inglés", "Filosofía", "Tutoría"
        ]
        created = []
        for name in course_names:
            if not Course.query.filter_by(name=name).first():
                course = Course(name=name)
                db.session.add(course)
                created.append(name)
        db.session.commit()
        return {"message": f"Cursos creados: {created}"}

    @staticmethod
    def setup_schedules():
        horas = [("07:00", "09:00"), ("09:00", "11:00"), ("11:00", "13:00")]
        dias = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes"]
        horario = [
            [["Matemáticas", "Educación Física", "Inglés"], ["Historia", "Química", "Filosofía"], ["Biología", "Matemáticas", "Tutoría"], ["Educación Cívica", "Arte", "Física"], ["Computación", "Arte", "Física"]],
            [["Historia", "Física", "Filosofía"], ["Matemáticas", "Química", "Inglés"], ["Religión", "Educación Física", "Tutoría"], ["Educación Cívica", "Religión", "Matemáticas"], ["Inglés", "Filosofía", "Arte"]],
            [["Biología", "Historia", "Educación Cívica"], ["Computación", "Tutoría", "Arte"], ["Matemáticas", "Filosofía", "Educación Física"], ["Religión", "Inglés", "Arte"], ["Educación Física", "Matemáticas", "Física"]],
            [["Física", "Tutoría", "Computación"], ["Educación Cívica", "Filosofía", "Religión"], ["Química", "Matemáticas", "Historia"], ["Inglés", "Filosofía", "Arte"], ["Religión", "Computación", "Biología"]],
            [["Educación Cívica", "Computación", "Religión"], ["Matemáticas", "Tutoría", "Educación Física"], ["Arte", "Química", "Física"], ["Filosofía", "Religión", "Matemáticas"], ["Inglés", "Educación Física", "Física"]]
        ]
        created = []
        for year_index, semana in enumerate(horario, start=1):
            for dia_index, dia in enumerate(dias):
                for bloque_index, materia in enumerate(semana[dia_index]):
                    course = Course.query.filter_by(name=materia).first()
                    if not course: continue
                    inicio = datetime.strptime(horas[bloque_index][0], "%H:%M").time()
                    fin = datetime.strptime(horas[bloque_index][1], "%H:%M").time()
                    db.session.add(Schedule(course_id=course.id, grade_level_id=year_index, day=dia, start_time=inicio, end_time=fin, classroom=f"Aula {year_index}"))
                    created.append(f"{materia} - {dia} - Año {year_index}")
        db.session.commit()
        return {"message": f"Se crearon {len(created)} horarios", "cursos": created}

    @staticmethod
    def associate_courses_to_grades():
        courses = Course.query.all()
        grade_levels = GradeLevel.query.all()
        for grade_level in grade_levels:
            for course in courses:
                if not Schedule.query.filter_by(grade_level_id=grade_level.id, course_id=course.id).first():
                    schedule = Schedule(grade_level_id=grade_level.id, course_id=course.id, day="Lunes", start_time=datetime.strptime("08:00", "%H:%M").time(), end_time=datetime.strptime("09:00", "%H:%M").time(), classroom="Aula general")
                    db.session.add(schedule)
        db.session.commit()
        return {"message": "Cursos asociados a todos los niveles exitosamente"}

    @staticmethod
    def get_grade_levels():
        return [gl.serialize() for gl in GradeLevel.query.all()]

    @staticmethod
    def get_courses():
        return [{"id": c.id, "name": c.name} for c in Course.query.all()]

    @staticmethod
    def get_periods():
        return ['Primer', 'Segundo', 'Tercer', 'Cuarto']
