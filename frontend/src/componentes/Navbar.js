import React from "react";
import { Link, useNavigate } from "react-router-dom";

const Navbar = () => {
  const token = localStorage.getItem("token");
  const user = JSON.parse(localStorage.getItem("user"));
  const navigate = useNavigate();

  const handleLogout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("user");
    navigate("/");
  };

  const handleQuieroVender = () => {
    if (token) {
      navigate("/vender"); // Si está autenticado, lo lleva a vender
    } else {
      navigate("/registro"); // Si no, lo manda a registrarse
    }
  };

  return (
    <nav className="navbar navbar-expand-lg navbar-light bg-light">
      <div className="container-fluid">
        <Link className="navbar-brand" to="/inicio">
          🚗 SegCloud
        </Link>
        <div className="d-flex">
          <button 
	  className="btn me-2" 
	  style={{ backgroundColor: "#2b6d6f", color: "white" }}
	  onClick={handleQuieroVender}
		>
	  Quiero Vender
	</button>

          {user && user.is_seller && (
            <Link className="btn btn-success me-2" to="/vender">
              Vender
            </Link>
          )}

          {token && (
            <button className="btn btn-danger" onClick={handleLogout}>
              Cerrar Sesión
            </button>
          )}
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
