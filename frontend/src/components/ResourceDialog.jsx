import {
    Dialog,
    DialogTitle,
    DialogContent,
    DialogActions,
    TextField,
    Button,
} from "@mui/material";

import { useState, useEffect } from "react";

export default function ResourceDialog({
    open,
    onClose,
    onSave,
    resource,
}) {
    const [form, setForm] = useState({
        name: "",
        category: "",
        quantity: "",
        description: "",
    });

    useEffect(() => {
        if (resource) {
            setForm(resource);
        } else {
            setForm({
                name: "",
                category: "",
                quantity: "",
                description: "",
            });
        }
    }, [resource]);

    const handleChange = (e) => {
        setForm({
            ...form,
            [e.target.name]: e.target.value,
        });
    };

    return (
        <Dialog
            open={open}
            onClose={onClose}
            fullWidth
            maxWidth="sm"
        >
            <DialogTitle>
                {resource ? "Edit Resource" : "Add Resource"}
            </DialogTitle>

            <DialogContent>

                <TextField
                    fullWidth
                    margin="normal"
                    label="Name"
                    name="name"
                    value={form.name}
                    onChange={handleChange}
                />

                <TextField
                    fullWidth
                    margin="normal"
                    label="Category"
                    name="category"
                    value={form.category}
                    onChange={handleChange}
                />

                <TextField
                    fullWidth
                    margin="normal"
                    label="Quantity"
                    type="number"
                    name="quantity"
                    value={form.quantity}
                    onChange={handleChange}
                />

                <TextField
                    fullWidth
                    margin="normal"
                    label="Description"
                    multiline
                    rows={3}
                    name="description"
                    value={form.description}
                    onChange={handleChange}
                />

            </DialogContent>

            <DialogActions>

                <Button
                    variant="contained"
                    onClick={() => onSave(form)}
                >
                    {resource ? "Update Resource" : "Add Resource"}
                </Button>
            </DialogActions>

        </Dialog>
    );
}