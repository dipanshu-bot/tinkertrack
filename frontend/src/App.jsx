import { BrowserRouter, Routes, Route } from "react-router-dom";

import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import Resources from "./pages/Resources";
import Reservations from "./pages/Reservations";
import BorrowHistory from "./pages/BorrowHistory";

import DashboardLayout from "./components/DashboardLayout";

export default function App() {
  return (
    <BrowserRouter>

      <Routes>

        <Route path="/" element={<Login />} />

        <Route element={<DashboardLayout />}>

          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/resources" element={<Resources />} />
          <Route path="/reservations" element={<Reservations />} />
          <Route path="/borrow-history" element={<BorrowHistory />} />

        </Route>

      </Routes>

    </BrowserRouter>
  );
}