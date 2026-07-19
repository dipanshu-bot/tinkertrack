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

export default function BorrowHistory() {
    const [history, setHistory] = useState([]);
    const [search, setSearch] = useState("");

    useEffect(() => {
        fetchHistory();
    }, []);

    const fetchHistory = async () => {
        try {
            const res = await api.get("/borrow/history");
            setHistory(res.data);
        } catch (err) {
            console.error(err);
        }
    };

    const filteredHistory = history.filter((item) =>
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
            field: "quantity",
            headerName: "Quantity",
            width: 120,
        },

        {
            field: "borrowed_at",
            headerName: "Borrowed At",
            flex: 1.5,
            valueFormatter: (value) =>
                value ? new Date(value).toLocaleString() : "",
        },

        {
            field: "returned_at",
            headerName: "Returned At",
            flex: 1.5,
            valueFormatter: (value) =>
                value ? new Date(value).toLocaleString() : "--",
        },

        {
            field: "status",
            headerName: "Status",
            width: 150,

            renderCell: (params) =>
                params.row.returned_at ? (
                    <Chip label="Returned" color="success" />
                ) : (
                    <Chip label="Borrowed" color="warning" />
                ),
        },
    ];

    return (
        <Box sx={{ p: 4 }}>

            <Typography
                variant="h4"
                sx={{
                    color: "white",
                    mb: 3,
                    fontWeight: "bold",
                    textAlign: "center",
                }}
            >
                Borrow History
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
                    rows={filteredHistory}
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