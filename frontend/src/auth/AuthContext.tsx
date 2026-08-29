import { createContext, useContext, useMemo, useState, type ReactNode } from "react";
import type { TokenResponse } from "../api/types";

interface AuthState {
  username: string | null;
  userType: "customer" | "staff" | null;
  isAuthenticated: boolean;
  login: (token: TokenResponse) => void;
  logout: () => void;
}

const AuthContext = createContext<AuthState | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [username, setUsername] = useState<string | null>(() =>
    localStorage.getItem("username"),
  );
  const [userType, setUserType] = useState<"customer" | "staff" | null>(
    () => localStorage.getItem("user_type") as "customer" | "staff" | null,
  );

  const login = (token: TokenResponse) => {
    localStorage.setItem("access_token", token.access_token);
    localStorage.setItem("user_type", token.user_type);
    localStorage.setItem("username", token.username);
    setUsername(token.username);
    setUserType(token.user_type);
  };

  const logout = () => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("user_type");
    localStorage.removeItem("username");
    setUsername(null);
    setUserType(null);
  };

  const value = useMemo<AuthState>(
    () => ({ username, userType, isAuthenticated: !!username, login, logout }),
    [username, userType],
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}

export function useAuth(): AuthState {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within an AuthProvider");
  return ctx;
}
