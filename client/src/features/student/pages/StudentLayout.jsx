import { Outlet } from "react-router-dom";
import ScrollToTop from "../../../common/components/ScrollToTop";
import { StudentNavbar } from "../components/StudentNavbar";
import { Footer } from "../../../common/components/Footer";

// Base component that maintains the navbar and footer throughout the page and the scroll to top functionality.
export const StudentLayout = () => {
  return (
    <ScrollToTop>
      <StudentNavbar />
      <Outlet />
      <Footer />
    </ScrollToTop>
  );
};
