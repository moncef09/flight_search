import { zodResolver } from "@hookform/resolvers/zod";
import { useMutation, useQuery } from "@tanstack/react-query";
import {
  Alert,
  Button,
  Card,
  CardContent,
  CircularProgress,
  Container,
  Divider,
  Grid,
  Stack,
  TextField,
  Typography,
} from "@mui/material";
import { useForm } from "react-hook-form";
import { useLocation, useNavigate } from "react-router-dom";
import { z } from "zod";
import { getQuote, payForBooking } from "../api/bookings";
import type { Flight } from "../api/types";

const paymentSchema = z.object({
  card_type: z.string().min(1, "Required"),
  card_num: z.string().regex(/^\d{12,19}$/, "Card number must be 12-19 digits"),
  name_on_card: z.string().min(1, "Required"),
  card_expiry_date: z.string().min(1, "Required"),
});
type PaymentValues = z.infer<typeof paymentSchema>;

export function BookingPage() {
  const location = useLocation();
  const navigate = useNavigate();
  const flight = (location.state as { flight?: Flight } | null)?.flight;

  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<PaymentValues>({ resolver: zodResolver(paymentSchema) });

  const quoteQuery = useQuery({
    queryKey: ["booking-quote", flight?.airline_name, flight?.flight_no, flight?.departure_date_and_time],
    queryFn: () =>
      getQuote({
        airline_name: flight!.airline_name,
        flight_no: flight!.flight_no,
        departure_date_and_time: flight!.departure_date_and_time,
      }),
    enabled: !!flight,
  });

  const payMutation = useMutation({
    mutationFn: payForBooking,
    onSuccess: (ticket) => {
      navigate(`/confirmation/${ticket.ticket_id}`, { state: { ticket } });
    },
  });

  if (!flight) {
    return (
      <Container maxWidth="sm" sx={{ mt: 6 }}>
        <Alert severity="warning">No flight selected. Go back and search again.</Alert>
      </Container>
    );
  }

  const onSubmit = (values: PaymentValues) => {
    if (!quoteQuery.data) return;
    payMutation.mutate({
      airline_name: flight.airline_name,
      flight_no: flight.flight_no,
      departure_date_and_time: flight.departure_date_and_time,
      sold_price: quoteQuery.data.sold_price,
      ...values,
    });
  };

  return (
    <Container maxWidth="sm" sx={{ mt: 4, mb: 6 }}>
      <Typography variant="h5" gutterBottom>
        Confirm and pay
      </Typography>

      {quoteQuery.isLoading && <CircularProgress />}
      {quoteQuery.isError && <Alert severity="error">This flight is no longer available for booking.</Alert>}

      {quoteQuery.data && (
        <Card variant="outlined" sx={{ mb: 3 }}>
          <CardContent>
            <Typography variant="h6">
              {quoteQuery.data.airline_name} · {quoteQuery.data.flight_no}
            </Typography>
            <Typography color="text.secondary">
              {quoteQuery.data.departure_airport} → {quoteQuery.data.arrival_airport}
            </Typography>
            <Divider sx={{ my: 1 }} />
            <Stack direction="row" justifyContent="space-between">
              <Typography>Base price</Typography>
              <Typography>${quoteQuery.data.base_price.toFixed(2)}</Typography>
            </Stack>
            {quoteQuery.data.sold_price > quoteQuery.data.base_price && (
              <Stack direction="row" justifyContent="space-between">
                <Typography color="warning.main">High-demand surcharge (≥60% booked)</Typography>
                <Typography color="warning.main">
                  +${(quoteQuery.data.sold_price - quoteQuery.data.base_price).toFixed(2)}
                </Typography>
              </Stack>
            )}
            <Divider sx={{ my: 1 }} />
            <Stack direction="row" justifyContent="space-between">
              <Typography variant="h6">Total</Typography>
              <Typography variant="h6">${quoteQuery.data.sold_price.toFixed(2)}</Typography>
            </Stack>
          </CardContent>
        </Card>
      )}

      {quoteQuery.data && (
        <form onSubmit={handleSubmit(onSubmit)} noValidate>
          <Stack spacing={2}>
            {payMutation.isError && <Alert severity="error">Payment failed. Check your card details.</Alert>}
            <Grid container spacing={2}>
              <Grid item xs={6}>
                <TextField
                  label="Card type"
                  fullWidth
                  placeholder="visa"
                  {...register("card_type")}
                  error={!!errors.card_type}
                  helperText={errors.card_type?.message}
                />
              </Grid>
              <Grid item xs={6}>
                <TextField
                  label="Card number"
                  fullWidth
                  {...register("card_num")}
                  error={!!errors.card_num}
                  helperText={errors.card_num?.message}
                />
              </Grid>
              <Grid item xs={12}>
                <TextField
                  label="Name on card"
                  fullWidth
                  {...register("name_on_card")}
                  error={!!errors.name_on_card}
                  helperText={errors.name_on_card?.message}
                />
              </Grid>
              <Grid item xs={12}>
                <TextField
                  label="Expiry date"
                  type="date"
                  fullWidth
                  slotProps={{ inputLabel: { shrink: true } }}
                  {...register("card_expiry_date")}
                  error={!!errors.card_expiry_date}
                  helperText={errors.card_expiry_date?.message}
                />
              </Grid>
            </Grid>
            <Button type="submit" variant="contained" size="large" disabled={payMutation.isPending}>
              Pay ${quoteQuery.data.sold_price.toFixed(2)}
            </Button>
          </Stack>
        </form>
      )}
    </Container>
  );
}
