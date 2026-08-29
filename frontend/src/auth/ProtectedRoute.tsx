import type { ReactNode } from "react";
import { Navigate } from "react-router-dom";
import { useAuth } from "./AuthContext";

interface ProtectedRouteProps {
  children: ReactNode;
  requireUserType?: "customer" | "staff";
}

// Client-side route guard - mirrors @protected_cust / @protected_staff in the
// old Flask app. This is a UX convenience only: the real enforcement is on
// the backend (CurrentCustomer / CurrentStaff in deps.py), which rejects
// requests regardless of what the frontend does.
export function ProtectedRoute({ children, requireUserType }: ProtectedRouteProps) {
  const { isAuthenticated, userType } = useAuth();

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  if (requireUserType && userType !== requireUserType) {
    return <Navigate to="/" replace />;
  }

  return <>{children}</>;
}
