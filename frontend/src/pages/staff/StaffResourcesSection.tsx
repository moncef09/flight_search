import { zodResolver } from "@hookform/resolvers/zod";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import {
  Alert,
  Button,
  Divider,
  Grid,
  Stack,
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableRow,
  TextField,
  Typography,
} from "@mui/material";
import { useForm } from "react-hook-form";
import { z } from "zod";
import { addAirplane, addAirport, listAirplanes } from "../../api/staff";

const airportSchema = z.object({
  airport_id: z.string().min(1, "Required"),
  name: z.string().min(1, "Required"),
  city: z.string().min(1, "Required"),
  country: z.string().min(1, "Required"),
});
type AirportFormValues = z.infer<typeof airportSchema>;

const airplaneSchema = z.object({
  id: z.string().min(1, "Required"),
  num_seats: z.number().int().positive("Must be positive"),
  manufacturing_co: z.string().min(1, "Required"),
});
type AirplaneFormValues = z.infer<typeof airplaneSchema>;

export function StaffResourcesSection() {
  const queryClient = useQueryClient();
  const { data: airplanes } = useQuery({ queryKey: ["staff-airplanes"], queryFn: listAirplanes });

  const airportForm = useForm<AirportFormValues>({ resolver: zodResolver(airportSchema) });
  const airportMutation = useMutation({
    mutationFn: addAirport,
    onSuccess: () => airportForm.reset(),
  });

  const airplaneForm = useForm<AirplaneFormValues>({ resolver: zodResolver(airplaneSchema) });
  const airplaneMutation = useMutation({
    mutationFn: addAirplane,
    onSuccess: () => {
      airplaneForm.reset();
      queryClient.invalidateQueries({ queryKey: ["staff-airplanes"] });
    },
  });

  return (
    <Stack spacing={4}>
      <div>
        <Typography variant="h6" gutterBottom>
          Add an airport
        </Typography>
        <form onSubmit={airportForm.handleSubmit((v) => airportMutation.mutate(v))} noValidate>
          <Grid container spacing={2}>
            {airportMutation.isError && (
              <Grid item xs={12}>
                <Alert severity="error">Could not add this airport (ID may already exist).</Alert>
              </Grid>
            )}
            {airportMutation.isSuccess && (
              <Grid item xs={12}>
                <Alert severity="success">Airport added.</Alert>
              </Grid>
            )}
            <Grid item xs={6} sm={3}>
              <TextField
                label="Airport ID"
                fullWidth
                {...airportForm.register("airport_id")}
                error={!!airportForm.formState.errors.airport_id}
                helperText={airportForm.formState.errors.airport_id?.message}
              />
            </Grid>
            <Grid item xs={6} sm={3}>
              <TextField
                label="Name"
                fullWidth
                {...airportForm.register("name")}
                error={!!airportForm.formState.errors.name}
                helperText={airportForm.formState.errors.name?.message}
              />
            </Grid>
            <Grid item xs={6} sm={3}>
              <TextField
                label="City"
                fullWidth
                {...airportForm.register("city")}
                error={!!airportForm.formState.errors.city}
                helperText={airportForm.formState.errors.city?.message}
              />
            </Grid>
            <Grid item xs={6} sm={3}>
              <TextField
                label="Country"
                fullWidth
                {...airportForm.register("country")}
                error={!!airportForm.formState.errors.country}
                helperText={airportForm.formState.errors.country?.message}
              />
            </Grid>
            <Grid item xs={12}>
              <Button type="submit" variant="contained" disabled={airportMutation.isPending}>
                Add airport
              </Button>
            </Grid>
          </Grid>
        </form>
      </div>

      <Divider />

      <div>
        <Typography variant="h6" gutterBottom>
          Add an airplane
        </Typography>
        <form onSubmit={airplaneForm.handleSubmit((v) => airplaneMutation.mutate(v))} noValidate>
          <Grid container spacing={2}>
            {airplaneMutation.isError && (
              <Grid item xs={12}>
                <Alert severity="error">Could not add this airplane (ID may already exist).</Alert>
              </Grid>
            )}
            <Grid item xs={4}>
              <TextField
                label="Airplane ID"
                fullWidth
                {...airplaneForm.register("id")}
                error={!!airplaneForm.formState.errors.id}
                helperText={airplaneForm.formState.errors.id?.message}
              />
            </Grid>
            <Grid item xs={4}>
              <TextField
                label="Seats"
                type="number"
                fullWidth
                {...airplaneForm.register("num_seats", { valueAsNumber: true })}
                error={!!airplaneForm.formState.errors.num_seats}
                helperText={airplaneForm.formState.errors.num_seats?.message}
              />
            </Grid>
            <Grid item xs={4}>
              <TextField
                label="Manufacturer"
                fullWidth
                {...airplaneForm.register("manufacturing_co")}
                error={!!airplaneForm.formState.errors.manufacturing_co}
                helperText={airplaneForm.formState.errors.manufacturing_co?.message}
              />
            </Grid>
            <Grid item xs={12}>
              <Button type="submit" variant="contained" disabled={airplaneMutation.isPending}>
                Add airplane
              </Button>
            </Grid>
          </Grid>
        </form>

        {airplanes && airplanes.length > 0 && (
          <Table size="small" sx={{ mt: 2 }}>
            <TableHead>
              <TableRow>
                <TableCell>ID</TableCell>
                <TableCell>Seats</TableCell>
                <TableCell>Manufacturer</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {airplanes.map((plane) => (
                <TableRow key={plane.id}>
                  <TableCell>{plane.id}</TableCell>
                  <TableCell>{plane.num_seats}</TableCell>
                  <TableCell>{plane.manufacturing_co}</TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        )}
      </div>
    </Stack>
  );
}
