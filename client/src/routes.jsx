import {
  createBrowserRouter,
  createRoutesFromElements,
  Route,
} from "react-router-dom";

// Auth Features
import { LoginPage } from "./features/auth/pages/LoginPage";
import { AdminLoginPage } from "./features/admin/pages/AdminLoginPage";
import { RoleSelectionPage } from "./features/auth/pages/RoleSectionPage";
import { StudentRegisterPage } from "./features/auth/pages/StudentRegisterPage";
import { TeacherRegisterPage } from "./features/auth/pages/TeacherRegisterPage";
import { ForgotPasswordPage } from "./features/auth/pages/ForgotPasswordPage";
import { ResetPasswordPage } from "./features/auth/pages/ResetPasswordPage";
import { AuthLayout } from "./features/auth/pages/AuthLayout";

// Admin Features
import { AdminLayout } from "./features/admin/pages/AdminLayout";
import { AdminProfilePage } from "./features/admin/pages/AdminProfilePage";
import { AllGradesPage } from "./features/admin/pages/AllGradesPage";
import { AllAsistancePage } from "./features/admin/pages/AllAsistancePage";
import { TeacherManagementPage } from "./features/admin/pages/TeacherManagementPage";
import { RegistrationRequestPage } from "./features/admin/pages/RegistrationRequestPage";

// Student Features
import { StudentLayout } from "./features/student/pages/StudentLayout";
import { StudentProfilePage } from "./features/student/pages/StudentProfilePage";
import { StudentSchedulePage } from "./features/student/pages/StudentSchedulePage";
import { StudentGradePage } from "./features/student/pages/StudentGradePage";

// Teacher Features
import { TeacherLayout } from "./features/teacher/pages/TeacherLayout";
import { TeacherProfilePage } from "./features/teacher/pages/TeacherProfilePage";
import { GradeEntryPage } from "./features/teacher/pages/GradeEntryPage";
import { AssistanceEntryPage } from "./features/teacher/pages/AssistanceEntryPage";
import { TeacherSchedulePage } from "./features/teacher/pages/TeacherSchedulePage";

// Common
import PrivateRoute from "./common/components/PrivateRoute";

export const router = createBrowserRouter(
  createRoutesFromElements(
    <Route path="/" errorElement={<h1>Not found!</h1>}>
      <Route path="/login/admin" element={<AdminLoginPage />} />

      <Route
        path="/"
        element={<AuthLayout />}
        errorElement={<h1>Not found!</h1>}
      >
        <Route path="/" element={<LoginPage />} />
        <Route path="/forgot-password" element={<ForgotPasswordPage />} />
        <Route path="/reset-password/:token" element={<ResetPasswordPage />} />
        <Route path="/signup" element={<RoleSelectionPage />} />
        <Route path="/signup/alumno" element={<StudentRegisterPage />} />
        <Route path="/signup/profesor" element={<TeacherRegisterPage />} />
      </Route>

      <Route
        path="/admin/dashboard"
        element={
          <PrivateRoute>
            <AdminLayout />
          </PrivateRoute>
        }
      >
        <Route path="/admin/dashboard/profile" element={<AdminProfilePage />} />
        <Route
          path="/admin/dashboard/alumnos/notas"
          element={<AllGradesPage />}
        />
        <Route
          path="/admin/dashboard/alumnos/asistencia"
          element={<AllAsistancePage />}
        />
        <Route
          path="/admin/dashboard/profesores"
          element={<TeacherManagementPage />}
        />
        <Route
          path="/admin/dashboard/solicitudes"
          element={<RegistrationRequestPage />}
        />
      </Route>

      <Route
        path="/teacher/dashboard"
        element={
          <PrivateRoute>
            <TeacherLayout />
          </PrivateRoute>
        }
      >
        <Route
          path="/teacher/dashboard/profile"
          element={<TeacherProfilePage />}
        />
        <Route
          path="/teacher/dashboard/alumnos/notas"
          element={<GradeEntryPage />}
        />
        <Route
          path="/teacher/dashboard/alumnos/asistencia"
          element={<AssistanceEntryPage />}
        />
        <Route
          path="/teacher/dashboard/horario"
          element={<TeacherSchedulePage />}
        />
      </Route>

      <Route
        path="/student/dashboard"
        element={
          <PrivateRoute>
            <StudentLayout />
          </PrivateRoute>
        }
      >
        <Route
          path="/student/dashboard/profile"
          element={<StudentProfilePage />}
        />
        <Route path="/student/dashboard/notas" element={<StudentGradePage />} />
        <Route
          path="/student/dashboard/horario"
          element={<StudentSchedulePage />}
        />
      </Route>
    </Route>
  )
);
