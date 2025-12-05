import { Outlet } from "react-router-dom";
import ScrollToTop from "../../../common/components/ScrollToTop";
import { TeacherNavbar } from "../components/TeacherNavbar";
import { Footer } from "../../../common/components/Footer";

// Base component that maintains the navbar and footer throughout the page and the scroll to top functionality.
export const TeacherLayout = () => {
  return (
    <ScrollToTop>
      <TeacherNavbar />
      <Outlet />
      <Footer />
    </ScrollToTop>
  );
};
