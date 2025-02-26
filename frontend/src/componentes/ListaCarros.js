import React, { useEffect, useState } from "react";
import api from "../api";

const ListaCarros = () => {
  const [carros, setCarros] = useState([]);

  useEffect(() => {
    const obtenerCarros = async () => {
      try {
        const response = await api.get("/carros/");
        setCarros(response.data);
      } catch (error) {
        console.error("Error al obtener los carros", error);
      }
    };

    obtenerCarros();
  }, []);

  return (
    <div>
      <h2>Lista de Carros</h2>
      <ul>
        {carros.map((carro) => (
          <li key={carro.id}>{carro.nombre}</li>
        ))}
      </ul>
    </div>
  );
};

export default ListaCarros;
