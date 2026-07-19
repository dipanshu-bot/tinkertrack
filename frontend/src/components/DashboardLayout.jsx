import { Outlet } from "react-router-dom";
import Sidebar from "./Sidebar";
import Navbar from "./Navbar";

export default function DashboardLayout(){

    return(

        <div style={{display:"flex"}}>

            <Sidebar/>

            <div
                style={{
                    marginLeft:"240px",
                    width:"100%",
                    padding:"25px",
                    background:"#0f172a",
                    minHeight:"100vh"
                }}
            >

                <Navbar/>

                <Outlet/>

            </div>

        </div>

    );

}