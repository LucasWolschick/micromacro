import Login from "./Login";

export default function LoginPage({ setAccount }) {
  return (
    <div className="container">
      <Login setAccount={setAccount} />
    </div>
  );
}
