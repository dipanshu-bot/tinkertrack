import { useState } from "react";
import api from "../api/axios";
import ResourceForm from "../components/ResourceForm";
export default function ResourceForm({ onSuccess }) {
    const [form, setForm] = useState({
        name: "",
        description: "",
        category: "",
        quantity: "",
        available_quantity: "",
    });

    const handleChange = (e) => {
        setForm({
            ...form,
            [e.target.name]: e.target.value,
        });
    };

    const handleSubmit = async (e) => {
        e.preventDefault();

        try {
            await api.post("/resources/", {
                ...form,
                quantity: Number(form.quantity),
                available_quantity: Number(form.available_quantity),
            });

            alert("Resource Added Successfully");

            setForm({
                name: "",
                description: "",
                category: "",
                quantity: "",
                available_quantity: "",
            });

            if (onSuccess) onSuccess();

        } catch (err) {
            console.log(err);
            alert("Failed to add resource");
        }
    };

    return (
        <form
            onSubmit={handleSubmit}
            style={{
                display: "flex",
                flexDirection: "column",
                gap: "12px",
                marginBottom: "30px",
            }}
        >
            <h2>Add Resource</h2>

            <input
                name="name"
                placeholder="Name"
                value={form.name}
                onChange={handleChange}
            />

            <input
                name="description"
                placeholder="Description"
                value={form.description}
                onChange={handleChange}
            />

            <input
                name="category"
                placeholder="Category"
                value={form.category}
                onChange={handleChange}
            />

            <input
                type="number"
                name="quantity"
                placeholder="Quantity"
                value={form.quantity}
                onChange={handleChange}
            />

            <input
                type="number"
                name="available_quantity"
                placeholder="Available Quantity"
                value={form.available_quantity}
                onChange={handleChange}
            />

            <button type="submit">
                Add Resource
            </button>
        </form>
    );
}
export default function Resources() {
    return (
        <div style={{ padding: "30px" }}>
            <h1>Resources</h1>

            <ResourceForm />

        </div>
    );
}