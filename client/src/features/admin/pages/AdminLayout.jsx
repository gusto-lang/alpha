import { Outlet } from "react-router-dom";
import ScrollToTop from "../../../common/components/ScrollToTop";
import { AdminNavbar } from "../components/AdminNavbar";
import { Footer } from "../../../common/components/Footer";

// Base component that maintains the navbar and footer throughout the page and the scroll to top functionality.
export const AdminLayout = () => {
  return (
    <ScrollToTop>
      <AdminNavbar />
      <Outlet />
      <Footer />
    </ScrollToTop>
  );
};
