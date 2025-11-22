import { useContext } from "react";
import { NavLink } from "react-router";

import AccountContext from "./AccountContext";

import "./Login.css";

export default function Login({ setAccount }) {
  const account = useContext(AccountContext);

  const logOut = () => {
    setAccount(null);
  };

  return account === null ? (
    <NavLink to="/login">Entrar</NavLink>
  ) : (
    <div>
      Olá, {account.user} <button onClick={() => logOut()}>Sair</button>
    </div>
  );
}
