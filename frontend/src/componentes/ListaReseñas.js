import React, { useEffect, useState } from "react";
import api from "../api";

const ListaReseñas = () => {
  const [reseñas, setReseñas] = useState([]);

  useEffect(() => {
    const obtenerReseñas = async () => {
      try {
        const response = await api.get("/reviews/");
        setReseñas(response.data);
      } catch (error) {
        console.error("Error al obtener las reseñas", error);
      }
    };

    obtenerReseñas();
  }, []);

  return (
    <div>
      <h2>Lista de Reseñas</h2>
      <ul>
        {reseñas.map((reseña) => (
          <li key={reseña.id}>{reseña.comentario}</li>
        ))}
      </ul>
    </div>
  );
};

export default ListaReseñas;
