export default function DashboardCard({ title, children }) {
    return (
        <div
            style={{
                background: "#1f1f1f",
                color: "white",
                borderRadius: "12px",
                padding: "20px",
                marginTop: "20px",
            }}
        >
            <h3>{title}</h3>

            <hr />

            {children}
        </div>
    );
}