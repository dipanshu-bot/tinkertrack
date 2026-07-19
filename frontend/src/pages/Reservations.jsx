import { useEffect, useState } from "react";
import api from "../api/axios";

import {
    Box,
    Typography,
    TextField,
    Paper,
    Chip,
} from "@mui/material";

import { DataGrid } from "@mui/x-data-grid";

export default function Reservations() {
    const [reservations, setReservations] = useState([]);
    const [search, setSearch] = useState("");

    useEffect(() => {
        fetchReservations();
    }, []);

    const fetchReservations = async () => {
        try {
            const res = await api.get("/reservations/my");
            setReservations(res.data);
        } catch (err) {
            console.error(err);
        }
    };

    const filteredReservations = reservations.filter((item) =>
        String(item.resource_id)
            .toLowerCase()
            .includes(search.toLowerCase())
    );

    const columns = [
        {
            field: "id",
            headerName: "ID",
            width: 80,
        },

        {
            field: "resource_id",
            headerName: "Resource",
            flex: 1,
        },

        {
            field: "start_time",
            headerName: "Start Time",
            flex: 1.5,
            valueFormatter: (value) =>
                value ? new Date(value).toLocaleString() : "",
        },

        {
            field: "end_time",
            headerName: "End Time",
            flex: 1.5,
            valueFormatter: (value) =>
                value ? new Date(value).toLocaleString() : "",
        },

        {
            field: "status",
            headerName: "Status",
            width: 150,

            renderCell: (params) => {
                const now = new Date();
                const end = new Date(params.row.end_time);

                return end > now ? (
                    <Chip label="Active" color="success" />
                ) : (
                    <Chip label="Expired" color="error" />
                );
            },
        },
    ];

    return (
        <Box sx={{ p: 4 }}>
            <Typography
                variant="h4"
                sx={{
                    color: "white",
                    fontWeight: "bold",
                    textAlign: "center",
                    mb: 3,
                }}
            >
                Reservations
            </Typography>

            <TextField
                label="Search by Resource ID"
                size="small"
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                sx={{
                    width: 300,
                    background: "white",
                    borderRadius: 2,
                    mb: 3,
                }}
            />

            <Paper sx={{ height: 500 }}>
                <DataGrid
                    rows={filteredReservations}
                    columns={columns}
                    pageSizeOptions={[5, 10, 20]}
                    initialState={{
                        pagination: {
                            paginationModel: {
                                pageSize: 5,
                            },
                        },
                    }}
                    sx={{
                        border: 0,
                        "& .MuiDataGrid-row:hover": {
                            backgroundColor: "#f5f5f5",
                        },
                    }}
                />
            </Paper>
        </Box>
    );
}