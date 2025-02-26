import React from "react";
import ListaCarros from "../componentes/ListaCarros";
import ListaReseñas from "../componentes/ListaReseñas";

const Inicio = () => {
  return (
    <div>
      <h2>Bienvenido</h2>
      <ListaCarros />
      <ListaReseñas />
    </div>
  );
};

export default Inicio;
