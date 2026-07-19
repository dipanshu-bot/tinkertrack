import { useEffect, useState } from "react";
import api from "../api/axios";
import StatCard from "../components/StatCard";

export default function Dashboard() {

    const [stats, setStats] = useState({
        total_users: 0,
        total_resources: 0,
        total_borrow_records: 0,
        active_borrows: 0,
        returned_borrows: 0,
        available_items: 0,
        borrowed_items: 0,
    });

    useEffect(() => {
        fetchStats();
    }, []);

    const fetchStats = async () => {
        try {
            const res = await api.get("/dashboard/stats");

            console.log("Dashboard Response:", res.data);

            setStats(res.data);
        } catch (err) {
            console.log(err.response);

            console.error("Dashboard Error:", err);
        }
    };

    return (
        <div>

            <h1
                style={{
                    color: "white",
                    marginBottom: "30px",
                    textAlign: "center",
                }}
            >
                TinkerTrack Dashboard
            </h1>

            <div
                style={{
                    display: "grid",
                    gridTemplateColumns: "repeat(4,1fr)",
                    gap: "20px",
                }}
            >
                <StatCard title="Resources" value={stats.total_resources} color="#4CAF50" />

                <StatCard title="Borrow Records" value={stats.total_borrow_records} color="#FF9800" />

                <StatCard title="Available Items" value={stats.available_items} color="#2196F3" />

                <StatCard title="Users" value={stats.total_users} color="#E91E63" />

                <StatCard title="Active Borrows" value={stats.active_borrows} color="#9C27B0" />

                <StatCard title="Returned Borrows" value={stats.returned_borrows} color="#00BCD4" />

                <StatCard title="Borrowed Items" value={stats.borrowed_items} color="#F44336" />
            </div>

        </div>
    );
}