import { zodResolver } from "@hookform/resolvers/zod";
import { Button, Grid, Stack, TextField } from "@mui/material";
import { useForm } from "react-hook-form";
import { z } from "zod";

const searchSchema = z
  .object({
    source: z.string().min(1, "Departure city/airport is required"),
    destination: z.string().min(1, "Arrival city/airport is required"),
    departure_date: z.string().min(1, "Departure date is required"),
    return_date: z.string().optional(),
  })
  .refine((data) => data.source.trim().toLowerCase() !== data.destination.trim().toLowerCase(), {
    message: "Departure and arrival can't be the same",
    path: ["destination"],
  })
  .refine((data) => !data.return_date || data.return_date >= data.departure_date, {
    message: "Return date must be on or after the departure date",
    path: ["return_date"],
  });

export type SearchFormValues = z.infer<typeof searchSchema>;

interface SearchFormProps {
  onSearch: (values: SearchFormValues) => void;
  defaultValues?: Partial<SearchFormValues>;
}

export function SearchForm({ onSearch, defaultValues }: SearchFormProps) {
  const {
    register,
    handleSubmit,
    formState: { errors },
  } = useForm<SearchFormValues>({
    resolver: zodResolver(searchSchema),
    defaultValues: { source: "", destination: "", departure_date: "", return_date: "", ...defaultValues },
  });

  return (
    <form onSubmit={handleSubmit(onSearch)} noValidate>
      <Stack spacing={2}>
        <Grid container spacing={2}>
          <Grid item xs={12} sm={6}>
            <TextField
              label="From (city, airport name, or code)"
              fullWidth
              {...register("source")}
              error={!!errors.source}
              helperText={errors.source?.message}
            />
          </Grid>
          <Grid item xs={12} sm={6}>
            <TextField
              label="To (city, airport name, or code)"
              fullWidth
              {...register("destination")}
              error={!!errors.destination}
              helperText={errors.destination?.message}
            />
          </Grid>
          <Grid item xs={12} sm={6}>
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
          <Grid item xs={12} sm={6}>
            <TextField
              label="Return date (optional)"
              type="date"
              fullWidth
              slotProps={{ inputLabel: { shrink: true } }}
              {...register("return_date")}
              error={!!errors.return_date}
              helperText={errors.return_date?.message}
            />
          </Grid>
        </Grid>
        <Button type="submit" variant="contained" size="large">
          Search Flights
        </Button>
      </Stack>
    </form>
  );
}
