export default function StatCard({ title, value, color }) {
    return (
        <div
            style={{
                background: "#222",
                padding: "20px",
                borderRadius: "12px",
                color: "white",
                boxShadow: "0 4px 10px rgba(0,0,0,.3)",
            }}
        >
            <h3 style={{ color }}>{title}</h3>

            <h1>{value}</h1>
        </div>
    );
}