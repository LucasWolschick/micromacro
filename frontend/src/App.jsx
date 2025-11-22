import { useState } from "react";
import { Outlet, Route, Routes } from "react-router";

import AccountContext from "./login/AccountContext.js";
import LoginPage from "./login/LoginPage.jsx";
import Topbar from "./Topbar.jsx";
import ProductListingPage from "./product_listing/ProductListingPage.jsx";
import WarehouseListingPage from "./warehouse_listing/WarehouseListingPage.jsx";

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
    <AccountContext value={account}>
      <Topbar setAccount={updateAccount} />
      <Outlet />
      <Routes>
        <Route index element={<ProductListingPage />} />
        <Route path="products" element={<ProductListingPage />} />
        <Route
          path="login"
          element={
            <LoginPage setAccount={(account) => updateAccount(account)} />
          }
        />
        <Route path="warehouses" element={<WarehouseListingPage />} />
      </Routes>
    </AccountContext>
  );
}
