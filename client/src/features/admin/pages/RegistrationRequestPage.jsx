import { useEffect, useState } from "react";
// Ya no necesitamos useAuth para el token, el apiClient lo maneja solo
import { apiClient } from "../../../common/api/apiClient";

export const RegistrationRequestPage = () => {
  const [register, setRegister] = useState("");
  const [teachers, setTeachers] = useState([]);
  const [students, setStudents] = useState([]);

  useEffect(() => {
    const fetchPending = async () => {
      try {
        // REFACTOR: Uso de apiClient.get
        const dataResponse = await apiClient.get("/api/pending/registrations");

        const onlyTeachers = dataResponse.filter(
          (user) => user.role === "teacher"
        );
        setTeachers(onlyTeachers);
        const onlyStudents = dataResponse.filter(
          (user) => user.role === "student"
        );
        setStudents(onlyStudents);
      } catch (error) {
        console.error("Error cargando solicitudes:", error);
      }
    };
    fetchPending();
  }, []);

  const approve = async (role, id) => {
    try {
      // REFACTOR: Uso de apiClient.put
      const result = await apiClient.put(`/api/approve/${role}/${id}`, {
        status: "approved",
      });

      console.log(result.msg);
      if (role === "teacher") {
        setTeachers((prev) => prev.filter((user) => user.id !== id));
      } else if (role === "student") {
        setStudents((prev) => prev.filter((user) => user.id !== id));
      }
    } catch (error) {
      console.error("Error aprobando usuario:", error);
    }
  };

  const reject = async (role, id) => {
    try {
      // REFACTOR: Uso de apiClient.delete
      await apiClient.delete(`/api/delete/user/${id}`);

      // Asumimos éxito si no lanza error
      if (role === "teacher") {
        setTeachers((prev) => prev.filter((user) => user.id !== id));
      } else if (role === "student") {
        setStudents((prev) => prev.filter((user) => user.id !== id));
      }
    } catch (error) {
      console.error("Error rechazando usuario:", error);
    }
  };

  return (
    <div className="container table-responsive my-5">
      <div className="row">
        <div className="col-2">
          <select
            className="form-select"
            aria-label="Selecciona una opción"
            onChange={(e) => setRegister(e.target.value)}
          >
            <option value="">Selecciona:</option>
            <option value="students">Alumnos</option>
            <option value="teachers">Profesores</option>
          </select>
        </div>
        {register === "teachers" ? (
          <table className="col-12 table table-striped table-bordered text-center mt-5">
            <thead className="table-light">
              <tr>
                <th scope="col">ID</th>
                <th scope="col">Apellidos</th>
                <th scope="col">Nombres</th>
                <th scope="col">Correo</th>
                <th scope="col">Celular</th>
                <th scope="col">Dirección</th>
                <th scope="col">Materia</th>
                <th scope="col">Acción</th>
              </tr>
            </thead>
            <tbody>
              {teachers.map((teachers) => (
                <tr key={teachers.id}>
                  <td>{teachers.id}</td>
                  <td>{teachers.last_name}</td>
                  <td>{teachers.first_name}</td>
                  <td>{teachers.email}</td>
                  <td>{teachers.teacher.phone}</td>
                  <td>{teachers.location}</td>
                  <td>{teachers.teacher.courses[0].name}</td>
                  <td>
                    <div className="d-flex justify-content-center align-items-center gap-2">
                      <button
                        type="button"
                        className="btn btn-success btn-sm"
                        onClick={() => approve(teachers.role, teachers.id)}
                      >
                        <i class="ri-check-double-line"></i>
                      </button>
                      <button
                        type="button"
                        className="btn btn-danger btn-sm"
                        onClick={() => reject(teachers.role, teachers.id)}
                      >
                        <i class="ri-prohibited-line"></i>
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        ) : (
          ""
        )}

        {register === "students" ? (
          <table className="col-12 table table-striped table-bordered text-center mt-5">
            <thead className="table-light">
              <tr>
                <th scope="col">ID</th>
                <th scope="col">Apellidos</th>
                <th scope="col">Nombres</th>
                <th scope="col">Correo</th>
                <th scope="col">Celular</th>
                <th scope="col">Dirección</th>
                <th scope="col">Grado</th>
                <th scope="col">Acción</th>
              </tr>
            </thead>
            <tbody>
              {students.map((students) => (
                <tr key={students.id}>
                  <td>{students.id}</td>
                  <td>{students.last_name}</td>
                  <td>{students.first_name}</td>
                  <td>{students.email}</td>
                  <td>{students.student.phone}</td>
                  <td>{students.location}</td>
                  <td>{students.student.grade_level}</td>
                  <td>
                    <div className="d-flex justify-content-center align-items-center gap-2">
                      <button
                        type="button"
                        className="btn btn-success btn-sm"
                        onClick={() => approve(students.role, students.id)}
                      >
                        <i class="ri-check-double-line"></i>
                      </button>
                      <button
                        type="button"
                        className="btn btn-danger btn-sm"
                        onClick={() => reject(students.role, students.id)}
                      >
                        <i class="ri-prohibited-line"></i>
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        ) : (
          ""
        )}
      </div>
    </div>
  );
};
