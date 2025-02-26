import React, { useState } from "react";

const InicioSesion = ({ onLogin, isRegister }) => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [username, setUsername] = useState("");
  const [firstName, setFirstName] = useState("");
  const [lastName, setLastName] = useState("");
  const [phoneNumber, setPhoneNumber] = useState("");
  const [address, setAddress] = useState("");
  const [city, setCity] = useState("");
  const [country, setCountry] = useState("");
  const [birthdate, setBirthdate] = useState("");
  
  const handleSubmit = (e) => {
    e.preventDefault();
    if (isRegister) {
      onLogin({
        username,
        email,
        password_hash: password,
        first_name: firstName,
        last_name: lastName,
        phone_number: phoneNumber,
        address,
        city,
        country,
        birthdate,
        is_seller: false,
        is_admin: false,
      });
    } else {
      onLogin(email, password);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      {isRegister && (
        <>
          <input type="text" placeholder="Nombre de usuario" value={username} onChange={(e) => setUsername(e.target.value)} required />
          <input type="text" placeholder="Nombre" value={firstName} onChange={(e) => setFirstName(e.target.value)} required />
          <input type="text" placeholder="Apellido" value={lastName} onChange={(e) => setLastName(e.target.value)} required />
          <input type="text" placeholder="Teléfono" value={phoneNumber} onChange={(e) => setPhoneNumber(e.target.value)} required />
          <input type="text" placeholder="Dirección" value={address} onChange={(e) => setAddress(e.target.value)} required />
          <input type="text" placeholder="Ciudad" value={city} onChange={(e) => setCity(e.target.value)} required />
          <input type="text" placeholder="País" value={country} onChange={(e) => setCountry(e.target.value)} required />
          <input type="date" placeholder="Fecha de nacimiento" value={birthdate} onChange={(e) => setBirthdate(e.target.value)} required />
        </>
      )}
      <input type="email" placeholder="Correo electrónico" value={email} onChange={(e) => setEmail(e.target.value)} required />
      <input type="password" placeholder="Contraseña" value={password} onChange={(e) => setPassword(e.target.value)} required />
      <button type="submit">{isRegister ? "Registrarse" : "Ingresar"}</button>
    </form>
  );
};

export default InicioSesion;
