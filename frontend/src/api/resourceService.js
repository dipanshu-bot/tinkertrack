import api from "./axios";

export const getResources = () =>
    api.get("/resources/");

export const createResource = (data) =>
    api.post("/resources/", data);

export const updateResource = (id, data) =>
    api.put(`/resources/${id}`, data);

export const deleteResource = (id) =>
    api.delete(`/resources/${id}`);
export const borrowResource = (data) =>
    api.post("/borrow/", data);