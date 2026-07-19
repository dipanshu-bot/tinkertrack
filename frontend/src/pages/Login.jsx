import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../api/axios";

export default function Login() {
    const navigate = useNavigate();

    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");

    const handleLogin = async (e) => {
        e.preventDefault();

        try {
            const formData = new URLSearchParams();
            formData.append("username", username);
            formData.append("password", password);

            const res = await api.post("/auth/login", formData, {
                headers: {
                    "Content-Type": "application/x-www-form-urlencoded",
                },
            });

            console.log("Login response:", res.data);

            localStorage.setItem("token", res.data.access_token);

            console.log("Stored token:", localStorage.getItem("token"));

            alert("Login Successful!");

            navigate("/dashboard");
        } catch (err) {
            alert("Invalid username or password");
            console.log(err);
        }
    };

    return (
        <div
            style={{
                display: "flex",
                justifyContent: "center",
                marginTop: "100px",
            }}
        >
            <form
                onSubmit={handleLogin}
                style={{
                    display: "flex",
                    flexDirection: "column",
                    width: "300px",
                    gap: "15px",
                }}
            >
                <h2>TinkerTrack Login</h2>

                <input
                    placeholder="Username"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                />

                <input
                    type="password"
                    placeholder="Password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                />

                <button type="submit">Login</button>
            </form>
        </div>
    );
}