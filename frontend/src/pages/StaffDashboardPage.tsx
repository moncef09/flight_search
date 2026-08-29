import { Container, Tab, Tabs, Typography } from "@mui/material";
import { useState } from "react";
import { useAuth } from "../auth/AuthContext";
import { StaffFlightsSection } from "./staff/StaffFlightsSection";
import { StaffOverviewSection } from "./staff/StaffOverviewSection";
import { StaffRatingsSection } from "./staff/StaffRatingsSection";
import { StaffReportsSection } from "./staff/StaffReportsSection";
import { StaffResourcesSection } from "./staff/StaffResourcesSection";

type StaffTab = "overview" | "flights" | "resources" | "ratings" | "reports";

export function StaffDashboardPage() {
  const { username } = useAuth();
  const [tab, setTab] = useState<StaffTab>("overview");

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 6 }}>
      <Typography variant="h5" gutterBottom>
        Staff Dashboard — {username}
      </Typography>
      <Tabs value={tab} onChange={(_, v) => setTab(v)} sx={{ mb: 3 }}>
        <Tab label="Overview" value="overview" />
        <Tab label="Manage Flights" value="flights" />
        <Tab label="Airports & Airplanes" value="resources" />
        <Tab label="Ratings" value="ratings" />
        <Tab label="Reports" value="reports" />
      </Tabs>

      {tab === "overview" && <StaffOverviewSection />}
      {tab === "flights" && <StaffFlightsSection />}
      {tab === "resources" && <StaffResourcesSection />}
      {tab === "ratings" && <StaffRatingsSection />}
      {tab === "reports" && <StaffReportsSection />}
    </Container>
  );
}
