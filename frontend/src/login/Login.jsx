import { useContext, useState } from "react";
import AccountContext from "./AccountContext";

export default function Login({ setAccount }) {
  const account = useContext(AccountContext);
  const [loading, setLoading] = useState(false);

  const onLogin = (formData) => {
    const username = formData.get("username");
    const password = formData.get("password");

    setLoading(true);
    fetch("http://localhost:8004/login", {
      method: "POST",
      body: new URLSearchParams({
        username,
        password,
      }),
    })
      .then((result) => result.json())
      .then((data) => setAccount({ user: data.user, token: data.access_token }))
      .then(() => setLoading(false));
  };

  const logOut = () => {
    setAccount(null);
  };

  return loading === false ? (
    account === null ? (
      <form action={onLogin}>
        <label htmlFor="username">Usuário:</label>
        <input type="text" name="username" id="username" />
        <label htmlFor="password">Senha:</label>
        <input type="password" name="password" id="password" />
        <button>Entrar</button>
      </form>
    ) : (
      <div>
        Olá, {account.user} <button onClick={() => logOut()}>Sair</button>
      </div>
    )
  ) : (
    <p>Carregando...</p>
  );
}
