import { useState } from "react";

import ProductListing from "./product_listing/ProductListing.jsx";
import WarehouseListing from "./warehouse_listing/WarehouseListing.jsx";
import AccountContext from "./login/AccountContext.js";
import Login from "./login/Login.jsx";

export default function App() {
  const [account, setAccount] = useState(() => {
    try {
      const val = sessionStorage.getItem("userCredentials");
      return val ? JSON.parse(val) : null;
    } catch (error) {
      console.error("Error retrieving logged in user:", error);
      sessionStorage.removeItem("userCredentials");
      return null;
    }
  });

  const updateAccount = (account) => {
    if (account === null) {
      sessionStorage.removeItem("userCredentials");
    } else {
      sessionStorage.setItem("userCredentials", JSON.stringify(account));
    }
    setAccount(account);
  };

  return (
    <>
      <AccountContext value={account}>
        <h1>Micromacro</h1>
        <Login setAccount={(account) => updateAccount(account)} />
        <WarehouseListing />
        <ProductListing />
      </AccountContext>
    </>
  );
}
