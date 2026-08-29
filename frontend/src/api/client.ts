import axios from "axios";

export const API_BASE_URL = import.meta.env.VITE_API_URL ?? "http://127.0.0.1:8000";

export const apiClient = axios.create({ baseURL: API_BASE_URL });

// Attach the JWT (if we have one) to every outgoing request.
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem("access_token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// If the token has expired/is invalid, the backend returns 401 - clear the
// stale token and send the user back to login instead of showing a confusing error.
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem("access_token");
      localStorage.removeItem("user_type");
      localStorage.removeItem("username");
      if (window.location.pathname !== "/login") {
        window.location.href = "/login";
      }
    }
    return Promise.reject(error);
  },
);
