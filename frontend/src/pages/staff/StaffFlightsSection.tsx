import { zodResolver } from "@hookform/resolvers/zod";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import {
  Alert,
  Button,
  Divider,
  Grid,
  MenuItem,
  Select,
  Stack,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  TextField,
  Typography,
} from "@mui/material";
import { useForm } from "react-hook-form";
import { z } from "zod";
import { createOrUpdateFlight, getUpcomingFlights, updateFlightStatus } from "../../api/staff";

const STATUS_OPTIONS = ["on-time", "delayed", "cancelled"];

const flightSchema = z.object({
  flight_no: z.string().min(1, "Required"),
  departure_date: z.string().min(1, "Required"),
  departure_time: z.string().min(1, "Required"),
  arrival_date: z.string().min(1, "Required"),
  arrival_time: z.string().min(1, "Required"),
  departure_airport_id: z.string().min(1, "Required"),
  arrival_airport_id: z.string().min(1, "Required"),
  base_price: z.number().positive("Must be positive"),
  airplane_id: z.string().min(1, "Required"),
  status: z.string().min(1, "Required"),
});
type FlightFormValues = z.infer<typeof flightSchema>;

export function StaffFlightsSection() {
  const queryClient = useQueryClient();
  const { data: flights } = useQuery({ queryKey: ["staff-upcoming-flights"], queryFn: getUpcomingFlights });

  const {
    register,
    handleSubmit,
    reset,
    formState: { errors },
  } = useForm<FlightFormValues>({
    resolver: zodResolver(flightSchema),
    defaultValues: { status: "on-time" },
  });

  const createMutation = useMutation({
    mutationFn: createOrUpdateFlight,
    onSuccess: () => {
      reset();
      queryClient.invalidateQueries({ queryKey: ["staff-upcoming-flights"] });
    },
  });

  const statusMutation = useMutation({
    mutationFn: ({ flightNo, departure, status }: { flightNo: string; departure: string; status: string }) =>
      updateFlightStatus(flightNo, departure, status),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["staff-upcoming-flights"] }),
  });

  const onSubmit = (values: FlightFormValues) => {
    createMutation.mutate({
      flight_no: values.flight_no,
      departure_date_and_time: `${values.departure_date}T${values.departure_time}:00`,
      arrival_date_and_time: `${values.arrival_date}T${values.arrival_time}:00`,
      departure_airport_id: values.departure_airport_id,
      arrival_airport_id: values.arrival_airport_id,
      base_price: values.base_price,
      airplane_id: values.airplane_id,
      status: values.status,
    });
  };

  return (
    <Stack spacing={3}>
      <div>
        <Typography variant="h6" gutterBottom>
          Create or update a flight
        </Typography>
        <Typography variant="body2" color="text.secondary" gutterBottom>
          Submitting with the same flight number and departure time as an existing flight updates it instead
          of creating a duplicate.
        </Typography>
        <form onSubmit={handleSubmit(onSubmit)} noValidate>
          <Grid container spacing={2} sx={{ mt: 1 }}>
            {createMutation.isError && (
              <Grid item xs={12}>
                <Alert severity="error">Could not save this flight. Check that the airports/airplane exist.</Alert>
              </Grid>
            )}
            <Grid item xs={6} sm={3}>
              <TextField
                label="Flight number"
                fullWidth
                {...register("flight_no")}
                error={!!errors.flight_no}
                helperText={errors.flight_no?.message}
              />
            </Grid>
            <Grid item xs={6} sm={3}>
              <TextField
                label="Airplane ID"
                fullWidth
                {...register("airplane_id")}
                error={!!errors.airplane_id}
                helperText={errors.airplane_id?.message}
              />
            </Grid>
            <Grid item xs={6} sm={3}>
              <TextField
                label="Departure airport ID"
                fullWidth
                {...register("departure_airport_id")}
                error={!!errors.departure_airport_id}
                helperText={errors.departure_airport_id?.message}
              />
            </Grid>
            <Grid item xs={6} sm={3}>
              <TextField
                label="Arrival airport ID"
                fullWidth
                {...register("arrival_airport_id")}
                error={!!errors.arrival_airport_id}
                helperText={errors.arrival_airport_id?.message}
              />
            </Grid>
            <Grid item xs={6} sm={3}>
              <TextField
                label="Departure date"
                type="date"
                fullWidth
                slotProps={{ inputLabel: { shrink: true } }}
                {...register("departure_date")}
                error={!!errors.departure_date}
                helperText={errors.departure_date?.message}
              />
            </Grid>
            <Grid item xs={6} sm={3}>
              <TextField
                label="Departure time"
                type="time"
                fullWidth
                slotProps={{ inputLabel: { shrink: true } }}
                {...register("departure_time")}
                error={!!errors.departure_time}
                helperText={errors.departure_time?.message}
              />
            </Grid>
            <Grid item xs={6} sm={3}>
              <TextField
                label="Arrival date"
                type="date"
                fullWidth
                slotProps={{ inputLabel: { shrink: true } }}
                {...register("arrival_date")}
                error={!!errors.arrival_date}
                helperText={errors.arrival_date?.message}
              />
            </Grid>
            <Grid item xs={6} sm={3}>
              <TextField
                label="Arrival time"
                type="time"
                fullWidth
                slotProps={{ inputLabel: { shrink: true } }}
                {...register("arrival_time")}
                error={!!errors.arrival_time}
                helperText={errors.arrival_time?.message}
              />
            </Grid>
            <Grid item xs={6} sm={3}>
              <TextField
                label="Base price"
                type="number"
                fullWidth
                {...register("base_price", { valueAsNumber: true })}
                error={!!errors.base_price}
                helperText={errors.base_price?.message}
              />
            </Grid>
            <Grid item xs={12}>
              <Button type="submit" variant="contained" disabled={createMutation.isPending}>
                Save flight
              </Button>
            </Grid>
          </Grid>
        </form>
      </div>

      <Divider />

      <div>
        <Typography variant="h6" gutterBottom>
          Update flight status
        </Typography>
        <TableContainer>
          <Table size="small">
            <TableHead>
              <TableRow>
                <TableCell>Flight</TableCell>
                <TableCell>Route</TableCell>
                <TableCell>Departs</TableCell>
                <TableCell>Status</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {(flights ?? []).map((flight) => (
                <TableRow key={`${flight.flight_no}-${flight.departure_date_and_time}`}>
                  <TableCell>{flight.flight_no}</TableCell>
                  <TableCell>
                    {flight.departure_airport_id} → {flight.arrival_airport_id}
                  </TableCell>
                  <TableCell>{new Date(flight.departure_date_and_time).toLocaleString()}</TableCell>
                  <TableCell>
                    <Select
                      size="small"
                      value={flight.status}
                      onChange={(e) =>
                        statusMutation.mutate({
                          flightNo: flight.flight_no,
                          departure: flight.departure_date_and_time,
                          status: e.target.value,
                        })
                      }
                    >
                      {STATUS_OPTIONS.map((s) => (
                        <MenuItem key={s} value={s}>
                          {s}
                        </MenuItem>
                      ))}
                    </Select>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      </div>
    </Stack>
  );
}
