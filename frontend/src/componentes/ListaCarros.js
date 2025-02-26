import React, { useEffect, useState } from "react";
import api from "../api";

const ListaCarros = () => {
  const [carros, setCarros] = useState([]);
  const [reseñas, setReseñas] = useState([]);

  useEffect(() => {
    const obtenerCarros = async () => {
      try {
        const response = await api.get("/carros/");
        setCarros(response.data);
      } catch (error) {
        console.error("Error al obtener los carros", error);
      }
    };

    const obtenerReseñas = async () => {
      try {
        const response = await api.get("/reviews/");
        console.log("Reseñas recibidas:", response.data); // Depuración
        setReseñas(response.data);
      } catch (error) {
        console.error("Error al obtener las reseñas", error);
      }
    };

    obtenerCarros();
    obtenerReseñas();
  }, []);

  return (
    <div>
      <h2>Lista de Carros</h2>
      {carros.map((carro) => (
        <div key={carro.id} style={{ border: "1px solid #ddd", padding: "10px", marginBottom: "10px" }}>
          <h3>{carro.model}</h3>
          <p><strong>Ubicación:</strong> {carro.location}</p>
          <p><strong>Precio:</strong> ${carro.price}</p>
          <p><strong>Año:</strong> {carro.year}</p>
          <p><strong>Kilometraje:</strong> {carro.km} km</p>
          <img src={carro.image_url} alt={carro.model} width="200" height="200" />
          
          {/* Mostrar reseñas asociadas */}
          <h4>Reseñas:</h4>
          <ul>
            {reseñas
              .filter((res) => res.carro_id === carro.id)
              .map((res) => (
                <li key={res.id}>
                  <strong>Calificación:</strong> {res.rating} ⭐ - {res.comment}
                </li>
              ))}
          </ul>

          {/* Si no hay reseñas, mostrar mensaje */}
          {reseñas.filter((res) => res.carro_id === carro.id).length === 0 && (
            <p>No hay reseñas para este carro.</p>
          )}
        </div>
      ))}
    </div>
  );
};

export default ListaCarros;
