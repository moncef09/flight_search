import { zodResolver } from "@hookform/resolvers/zod";
import { Alert, Button, Container, Grid, Paper, Stack, TextField, Typography } from "@mui/material";
import { useState } from "react";
import { useForm } from "react-hook-form";
import { useNavigate } from "react-router-dom";
import { z } from "zod";
import { registerCustomer } from "../api/auth";

const registerSchema = z.object({
  email: z.email("Enter a valid email"),
  password: z.string().min(6, "At least 6 characters"),
  name: z.string().min(1, "Required"),
  building_num: z.string().min(1, "Required"),
  street: z.string().min(1, "Required"),
  city: z.string().min(1, "Required"),
  state: z.string().min(1, "Required"),
  phone_num: z.string().min(10, "10 digit phone number").max(10),
  passport_number: z.string().min(1, "Required"),
  passport_expiration: z.string().min(1, "Required"),
  passport_country: z.string().min(1, "Required"),
  date_of_birth: z.string().min(1, "Required"),
});
type RegisterValues = z.infer<typeof registerSchema>;

export function RegisterPage() {
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();

  const {
    register,
    handleSubmit,
    formState: { errors, isSubmitting },
  } = useForm<RegisterValues>({ resolver: zodResolver(registerSchema) });

  const onSubmit = async (values: RegisterValues) => {
    setError(null);
    try {
      await registerCustomer(values);
      navigate("/login");
    } catch (err: unknown) {
      const message =
        (err as { response?: { data?: { detail?: string } } })?.response?.data?.detail ??
        "Registration failed";
      setError(message);
    }
  };

  const field = (name: keyof RegisterValues, label: string, extra: Record<string, unknown> = {}) => (
    <TextField
      label={label}
      fullWidth
      {...register(name)}
      error={!!errors[name]}
      helperText={errors[name]?.message}
      {...extra}
    />
  );

  return (
    <Container maxWidth="sm" sx={{ mt: 4, mb: 6 }}>
      <Paper sx={{ p: 3 }}>
        <Typography variant="h5" gutterBottom textAlign="center">
          Create your account
        </Typography>
        <form onSubmit={handleSubmit(onSubmit)} noValidate>
          <Stack spacing={2}>
            {error && <Alert severity="error">{error}</Alert>}
            <Grid container spacing={2}>
              <Grid item xs={12}>{field("email", "Email")}</Grid>
              <Grid item xs={12}>{field("password", "Password", { type: "password" })}</Grid>
              <Grid item xs={12}>{field("name", "Full name")}</Grid>
              <Grid item xs={6}>{field("building_num", "Building #")}</Grid>
              <Grid item xs={6}>{field("street", "Street")}</Grid>
              <Grid item xs={6}>{field("city", "City")}</Grid>
              <Grid item xs={6}>{field("state", "State")}</Grid>
              <Grid item xs={12}>{field("phone_num", "Phone number")}</Grid>
              <Grid item xs={6}>{field("passport_number", "Passport number")}</Grid>
              <Grid item xs={6}>
                {field("passport_expiration", "Passport expiration", {
                  type: "date",
                  InputLabelProps: { shrink: true },
                })}
              </Grid>
              <Grid item xs={6}>{field("passport_country", "Passport country")}</Grid>
              <Grid item xs={6}>
                {field("date_of_birth", "Date of birth", { type: "date", InputLabelProps: { shrink: true } })}
              </Grid>
            </Grid>
            <Button type="submit" variant="contained" size="large" disabled={isSubmitting}>
              Register
            </Button>
          </Stack>
        </form>
      </Paper>
    </Container>
  );
}
