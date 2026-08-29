import { Container, Paper, Typography } from "@mui/material";
import { useNavigate } from "react-router-dom";
import { SearchForm, type SearchFormValues } from "../components/SearchForm";

export function HomePage() {
  const navigate = useNavigate();

  const handleSearch = (values: SearchFormValues) => {
    const params = new URLSearchParams({
      source: values.source,
      destination: values.destination,
      departure_date: values.departure_date,
      ...(values.return_date ? { return_date: values.return_date } : {}),
    });
    navigate(`/results?${params.toString()}`);
  };

  return (
    <Container maxWidth="sm" sx={{ mt: 6 }}>
      <Typography variant="h4" gutterBottom textAlign="center">
        Find your next flight
      </Typography>
      <Paper sx={{ p: 3, mt: 3 }}>
        <SearchForm onSearch={handleSearch} />
      </Paper>
    </Container>
  );
}
