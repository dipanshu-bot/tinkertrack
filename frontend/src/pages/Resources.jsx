import { useEffect, useState } from "react";
import {
    getResources,
    createResource,
    updateResource,
    deleteResource,
    borrowResource,
} from "../api/resourceService";
import EditIcon from "@mui/icons-material/Edit";
import DeleteIcon from "@mui/icons-material/Delete";
import ShoppingCartIcon from "@mui/icons-material/ShoppingCart";

import IconButton from "@mui/material/IconButton";
import Tooltip from "@mui/material/Tooltip";
import {
    Box,
    Typography,
    Paper,
    TextField,
    Button,
} from "@mui/material";

import { DataGrid } from "@mui/x-data-grid";
import AddIcon from "@mui/icons-material/Add";
import Chip from "@mui/material/Chip";
import ResourceDialog from "../components/ResourceDialog";


export default function Resources() {
    const [resources, setResources] = useState([]);
    const [search, setSearch] = useState("");
    const [openDialog, setOpenDialog] = useState(false);
    const [selectedResource, setSelectedResource] = useState(null);
    const [borrowQuantity, setBorrowQuantity] = useState(1);

    useEffect(() => {
        fetchResources();
    }, []);

    const fetchResources = async () => {
        try {
            const res = await getResources();
            setResources(res.data);
        } catch (err) {
            console.error(err);
        }
    };

    const filteredResources = resources.filter((item) =>
        item.name.toLowerCase().includes(search.toLowerCase())
    );

    const columns = [
        {
            field: "id",
            headerName: "ID",
            width: 70,
        },

        {
            field: "name",
            headerName: "Resource",
            minWidth: 220,
            flex: 2,
        },

        {
            field: "category",
            headerName: "Category",
            minWidth: 170,
            flex: 1.5,
        },

        {
            field: "quantity",
            headerName: "Total",
            width: 100,
        },

        {
            field: "available_quantity",
            headerName: "Available",
            width: 120,
        },

        {
            field: "status",
            headerName: "Status",
            width: 170,

            renderCell: (params) => {

                const available = params.row.available_quantity;

                if (available === 0)
                    return <Chip label="Out of Stock" color="error" />;

                if (available < 5)
                    return <Chip label="Low Stock" color="warning" />;

                return <Chip label="Available" color="success" />;
            },
        },

        {
            field: "actions",
            headerName: "Actions",
            width: 170,

            renderCell: (params) => (
                <>
                    <Tooltip title="Edit">
                        <IconButton
                            color="primary"
                            onClick={() => {
                                setSelectedResource(params.row);
                                setOpenDialog(true);
                            }}
                        >
                            <EditIcon />
                        </IconButton>
                    </Tooltip>

                    <Tooltip title="Delete">
                        <IconButton
                            color="error"
                            onClick={async () => {

                                const confirmDelete = window.confirm(
                                    `Delete "${params.row.name}" ?`
                                );

                                if (!confirmDelete) return;

                                try {

                                    await deleteResource(params.row.id);

                                    alert("Resource Deleted");

                                    fetchResources();

                                } catch (err) {

                                    console.error(err);

                                    alert("Delete Failed");

                                }

                            }}
                        >
                            <DeleteIcon />
                        </IconButton>
                    </Tooltip>
                    <Tooltip title="Borrow">
                        <IconButton
                            color="success"
                            onClick={async () => {

                                const qty = prompt("Enter quantity to borrow", "1");

                                if (!qty) return;

                                try {

                                    await borrowResource({
                                        resource_id: params.row.id,
                                        quantity: Number(qty),
                                    });

                                    alert("Resource Borrowed Successfully");

                                    fetchResources();

                                } catch (err) {

                                    console.error(err);

                                    alert("Borrow Failed");

                                }

                            }}
                        >
                            <ShoppingCartIcon />
                        </IconButton>
                    </Tooltip>
                </>
            ),
        }
    ];

    return (
        <Box sx={{ p: 4 }}>

            <Typography
                variant="h4"
                sx={{
                    color: "white",
                    mb: 3,
                    fontWeight: "bold",
                }}
            >
                Resources
            </Typography>

            <Box
                sx={{
                    display: "flex",
                    justifyContent: "space-between",
                    mb: 2,
                }}
            >
                <TextField
                    label="Search Resource"
                    variant="outlined"
                    size="small"
                    value={search}
                    onChange={(e) => setSearch(e.target.value)}
                    sx={{
                        background: "white",
                        borderRadius: 2,
                        width: 300,
                    }}
                />

                <Button
                    variant="contained"
                    startIcon={<AddIcon />}
                    sx={{
                        borderRadius: 2,
                        textTransform: "none",
                        fontWeight: "bold",
                        backgroundColor: "#4CAF50",
                        "&:hover": {
                            backgroundColor: "#45A049",
                        },
                        color: "white",
                    }}
                    onClick={() => {
                        setSelectedResource(null);
                        setOpenDialog(true);
                    }}
                >
                    Add Resource
                </Button>
            </Box>

            <Paper
                sx={{
                    height: 550,
                    width: "100%",
                    minWidth: 1100,
                }}
            >

                <DataGrid
                    rows={filteredResources}
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
                        width: "100%",
                        "& .MuiDataGrid-columnHeaders": {
                            fontWeight: "bold",
                            fontSize: 15,
                        },
                        "& .MuiDataGrid-cell": {
                            fontSize: 14,
                        },
                    }}
                />

            </Paper>
            <ResourceDialog
                open={openDialog}
                resource={selectedResource}
                onClose={() => setOpenDialog(false)}
                onSave={async (data) => {
                    try {

                        if (selectedResource) {

                            await updateResource(selectedResource.id, {
                                ...data,
                                quantity: Number(data.quantity),
                                available_quantity: Number(data.quantity),
                            });

                            alert("Resource Updated Successfully");

                        } else {

                            await createResource({
                                ...data,
                                quantity: Number(data.quantity),
                                available_quantity: Number(data.quantity),
                            });

                            alert("Resource Added Successfully");
                        }

                        fetchResources();
                        setOpenDialog(false);

                    } catch (err) {
                        console.error(err);
                        alert("Failed");
                    }
                }}
            />
        </Box>
    );
}