import { useState, useEffect, useRef, useContext } from "react";

import Product from "./Product.jsx";
import ProductDetails from "./ProductDetails.jsx";
import AccountContext from "../login/AccountContext.js";

import "./ProductListing.css";
import {
  addProduct,
  listProducts,
  listWarehouses,
} from "../marketplace_api.js";

export default function ProductListing() {
  const [loadingState, setLoadingState] = useState("loading");
  const [productData, setProductData] = useState([]);
  const [warehouseData, setWarehouseData] = useState([]);
  const [selectedProductSku, setSelectedProductSku] = useState(null);

  const [productName, setProductName] = useState("");
  const [productPrice, setProductPrice] = useState(0.0);

  const account = useContext(AccountContext);

  const dialog = useRef();

  const fetchData = () => {
    setLoadingState("loading");
    Promise.all([
      listProducts().then((json) => setProductData(json)),
      listWarehouses().then((result) => setWarehouseData(result)),
    ])
      .then(() => setLoadingState("loaded"))
      .catch(() => setLoadingState("failed"));
  };

  const onAddProduct = (event) => {
    if (event.target.returnValue !== "add") return;
    if (account === null) return;
    if (productName.trim() === "") return;
    if (productPrice < 0.0) return;

    addProduct({ token: account.token, productName, productPrice }).then(() =>
      fetchData()
    );

    setProductName("");
    setProductPrice(0.0);
  };

  useEffect(() => {
    fetchData();
  }, []);

  const selectedProduct =
    selectedProductSku !== null
      ? productData.find((product) => product.sku == selectedProductSku)
      : null;

  return (
    <>
      {loadingState === "loading" ? (
        <p>Carregando produtos...</p>
      ) : loadingState === "failed" ? (
        <p>Não foi possível carregar os produtos</p>
      ) : (
        <>
          <ul>
            {productData.map((product) => (
              <li key={product.sku}>
                <Product
                  product={product}
                  onSelected={() => setSelectedProductSku(product.sku)}
                ></Product>
              </li>
            ))}
          </ul>

          {account && (
            <button onClick={() => dialog.current.showModal()}>
              Adicionar produto
            </button>
          )}

          {selectedProduct && (
            <ProductDetails
              product={selectedProduct}
              warehouseData={warehouseData}
              onClose={() => setSelectedProductSku(null)}
              onEdited={() => fetchData()}
            />
          )}

          <dialog ref={dialog} onClose={onAddProduct}>
            <h2>Adicionar produto</h2>
            <form method="dialog">
              <label htmlFor="description">Nome:</label>
              <input
                type="text"
                name="description"
                id="description"
                value={productName}
                onChange={(e) => setProductName(e.target.value)}
              />
              <label htmlFor="price">Preço:</label>
              <input
                type="number"
                name="price"
                id="price"
                value={productPrice}
                onChange={(e) => setProductPrice(e.target.value)}
              />

              <button value="cancel">Cancelar</button>
              <button value="add">Adicionar</button>
            </form>
          </dialog>
        </>
      )}
    </>
  );
}
