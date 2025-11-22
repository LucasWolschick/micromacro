import { Link } from "react-router";

import LoginWidget from "./login/LoginWidget.jsx";

import "./Topbar.css";

export default function Topbar({ setAccount }) {
  return (
    <header>
      <nav className="container">
        <Link to="/">
          <h1>Micromacro</h1>
        </Link>
        <Link to="/products">Produtos</Link>
        <Link to="/warehouses">Centros de distribuição</Link>
        <LoginWidget setAccount={(account) => setAccount(account)} />
      </nav>
    </header>
  );
}
