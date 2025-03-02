import React, { useEffect, useState } from "react";
import ListaCarros from "../componentes/ListaCarros";
import { useNavigate } from "react-router-dom";

const Inicio = () => {
  const [user, setUser] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const storedUser = localStorage.getItem("user");
    if (storedUser) {
      setUser(JSON.parse(storedUser));
    }
  }, []);

  return (
    <div>
      {user?.is_seller && (
        <button className="btn btn-success mb-3" onClick={() => navigate("/vender")}>Vender</button>
      )}
      <ListaCarros />
    </div>
  );
};

export default Inicio;
