import { Route, Routes } from "react-router-dom";
import { NavBar } from "./components/NavBar";
import { ProtectedRoute } from "./auth/ProtectedRoute";
import { HomePage } from "./pages/HomePage";
import { ResultsPage } from "./pages/ResultsPage";
import { LoginPage } from "./pages/LoginPage";
import { RegisterPage } from "./pages/RegisterPage";
import { BookingPage } from "./pages/BookingPage";
import { ConfirmationPage } from "./pages/ConfirmationPage";
import { MyBookingsPage } from "./pages/MyBookingsPage";
import { StaffDashboardPage } from "./pages/StaffDashboardPage";

export function App() {
  return (
    <>
      <NavBar />
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/results" element={<ResultsPage />} />
        <Route path="/login" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
        <Route
          path="/booking"
          element={
            <ProtectedRoute requireUserType="customer">
              <BookingPage />
            </ProtectedRoute>
          }
        />
        <Route
          path="/confirmation/:ticketId"
          element={
            <ProtectedRoute requireUserType="customer">
              <ConfirmationPage />
            </ProtectedRoute>
          }
        />
        <Route
          path="/my-bookings"
          element={
            <ProtectedRoute requireUserType="customer">
              <MyBookingsPage />
            </ProtectedRoute>
          }
        />
        <Route
          path="/staff/dashboard"
          element={
            <ProtectedRoute requireUserType="staff">
              <StaffDashboardPage />
            </ProtectedRoute>
          }
        />
      </Routes>
    </>
  );
}
