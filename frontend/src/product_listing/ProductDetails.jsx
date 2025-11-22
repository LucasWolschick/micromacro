import { useContext, useState } from "react";
import AccountContext from "../login/AccountContext";

import "./ProductDetails.css";

function ProductStockListing({ warehouse, sku, quantity, onEdited }) {
  const [editing, setEditing] = useState(false);

  const account = useContext(AccountContext);

  const onSubmitted = (e) => {
    setEditing(false);

    if (account === null) return;

    const quantity = e.get("quantity");

    if (quantity < 0) return;

    fetch(`http://localhost:8004/products/${sku}/stock`, {
      method: "PUT",
      headers: {
        Authorization: `Bearer ${account.token}`,
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        warehouse_id: warehouse.id,
        quantity,
      }),
    }).then(() => onEdited());
  };

  return account && editing ? (
    <div className="product-stock-listing">
      <b>
        {warehouse.description} (D-{warehouse.id}):{" "}
      </b>
      <form action={onSubmitted}>
        <input
          type="number"
          name="quantity"
          id="quantity"
          defaultValue={quantity}
        />
        <button type="submit">Atualizar</button>
        <button onClick={() => setEditing(false)}>Cancelar</button>
      </form>
    </div>
  ) : (
    <div className="product-stock-listing">
      <b>
        {warehouse.description} (D-{warehouse.id})
      </b>
      <div>
        {quantity} un.{" "}
        {account && <button onClick={() => setEditing(true)}>Editar</button>}
      </div>
    </div>
  );
}

export default function ProductDetails({
  product,
  warehouseData,
  onClose,
  onEdited,
}) {
  const warehouses = new Map();
  warehouseData.forEach((warehouse) => {
    warehouses.set(warehouse.id, warehouse);
  });
  return (
    <div className="product-details">
      <h2>Detalhes do produto</h2>
      <p>SKU-{product.sku}</p>
      <p>
        <b>Nome: </b> {product.description}
      </p>
      <p>
        <b>Preço: </b>{" "}
        {product.price.toLocaleString(undefined, {
          style: "currency",
          currency: "BRL",
        })}
      </p>
      <p>
        <b>Quantidade em estoque: </b>
        {product.stock.total_quantity} unidade(s)
      </p>
      <ul>
        {warehouses.values().map((warehouse) => {
          const productStocks = product.stock.deposits.find(
            (deposit) => deposit.warehouse == warehouse.id
          );
          return (
            <li key={warehouse.id}>
              <ProductStockListing
                warehouse={warehouse}
                sku={product.sku}
                quantity={productStocks?.quantity ?? 0}
                onEdited={onEdited}
              />
            </li>
          );
        })}
      </ul>
      <button onClick={() => onClose()}>Fechar</button>
    </div>
  );
}
