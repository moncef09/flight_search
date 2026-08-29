import { zodResolver } from "@hookform/resolvers/zod";
import { Alert, Button, Container, Paper, Stack, Tab, Tabs, TextField, Typography } from "@mui/material";
import { useState } from "react";
import { useForm } from "react-hook-form";
import { useLocation, useNavigate } from "react-router-dom";
import { z } from "zod";
import { loginCustomer, loginStaff } from "../api/auth";
import { useAuth } from "../auth/AuthContext";

const loginSchema = z.object({
  username: z.string().min(1, "Required"),
  password: z.string().min(1, "Required"),
});
type LoginValues = z.infer<typeof loginSchema>;

export function LoginPage() {
  const [tab, setTab] = useState<"customer" | "staff">("customer");
  const [error, setError] = useState<string | null>(null);
  const { login } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<LoginValues>({ resolver: zodResolver(loginSchema) });

  const onSubmit = async (values: LoginValues) => {
    setError(null);
    try {
      const token = tab === "customer"
        ? await loginCustomer(values.username, values.password)
        : await loginStaff(values.username, values.password);
      login(token);

      const state = location.state as { from?: string; pendingFlight?: unknown } | null;
      if (state?.from === "/results" && state.pendingFlight) {
        navigate("/booking", { state: { flight: state.pendingFlight } });
      } else {
        navigate(tab === "staff" ? "/staff/dashboard" : "/");
      }
    } catch {
      setError("Invalid username or password");
    }
  };

  return (
    <Container maxWidth="xs" sx={{ mt: 6 }}>
      <Paper sx={{ p: 3 }}>
        <Typography variant="h5" gutterBottom textAlign="center">
          Log in
        </Typography>
        <Tabs value={tab} onChange={(_, v) => setTab(v)} centered sx={{ mb: 2 }}>
          <Tab label="Customer" value="customer" />
          <Tab label="Staff" value="staff" />
        </Tabs>
        <form onSubmit={handleSubmit(onSubmit)} noValidate>
          <Stack spacing={2}>
            {error && <Alert severity="error">{error}</Alert>}
            <TextField
              label={tab === "customer" ? "Email" : "Username"}
              fullWidth
              {...register("username")}
              error={!!errors.username}
              helperText={errors.username?.message}
            />
            <TextField
              label="Password"
              type="password"
              fullWidth
              {...register("password")}
              error={!!errors.password}
              helperText={errors.password?.message}
            />
            <Button type="submit" variant="contained" disabled={isSubmitting}>
              Log in
            </Button>
          </Stack>
        </form>
      </Paper>
    </Container>
  );
}
