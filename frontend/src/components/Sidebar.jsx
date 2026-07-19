import { NavLink } from "react-router-dom";

import DashboardIcon from "@mui/icons-material/Dashboard";
import InventoryIcon from "@mui/icons-material/Inventory";
import EventAvailableIcon from "@mui/icons-material/EventAvailable";
import HistoryIcon from "@mui/icons-material/History";

import "./DashboardLayout.css";

export default function Sidebar() {
    return (
        <div className="sidebar">

            <h2>TinkerTrack</h2>

            <NavLink to="/dashboard">
                <DashboardIcon />
                <span>Dashboard</span>
            </NavLink>

            <NavLink to="/resources">
                <InventoryIcon />
                <span>Resources</span>
            </NavLink>

            <NavLink to="/reservations">
                <EventAvailableIcon />
                <span>Reservations</span>
            </NavLink>

            <NavLink to="/borrow-history">
                <HistoryIcon />
                <span>Borrow History</span>
            </NavLink>

        </div>
    );
}