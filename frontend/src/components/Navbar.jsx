import PersonIcon from "@mui/icons-material/Person";
import "./DashboardLayout.css";

export default function Navbar() {

  return (

    <div className="navbar">

      <h2>Shared Resource Management System</h2>

      <div className="profile">

        <PersonIcon/>

        <span>Admin</span>

      </div>

    </div>

  );

}