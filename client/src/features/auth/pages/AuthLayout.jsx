import { Outlet } from "react-router-dom";
import ScrollToTop from "../../../common/components/ScrollToTop";
import { Footer } from "../../../common/components/Footer";
import { AuthNavbar } from "../components/AuthNavbar";

export const AuthLayout = () => {
  return (
    <ScrollToTop>
      <AuthNavbar />
      <Outlet />
      <Footer />
    </ScrollToTop>
  );
};
