import { useState, useEffect, useRef, useContext } from "react";
import AccountContext from "../login/AccountContext";

import "./WarehouseListing.css";
import { listWarehouses } from "../marketplace_api";

export default function WarehouseListing() {
  const [warehouseDataState, setWarehouseDataState] = useState("loading");
  const [warehouseData, setWarehouseData] = useState([]);
  const [warehouseName, setWarehouseName] = useState("");

  const account = useContext(AccountContext);

  const dialog = useRef();

  const fetchWarehouses = () => {
    setWarehouseDataState("loading");
    listWarehouses()
      .then((warehouses) => setWarehouseData(warehouses))
      .then(() => setWarehouseDataState("loaded"))
      .catch(() => setWarehouseDataState("failed"));
  };

  const addWarehouse = (event) => {
    if (account === null) return;

    if (event.target.returnValue !== "add") return;

    if (warehouseName.trim() === "") return;

    createWarehouse({
      token: account.token,
      description: warehouseName.trim(),
    }).then(() => fetchWarehouses());

    setWarehouseName("");
  };

  useEffect(() => {
    fetchWarehouses();
  }, []);

  return (
    <>
      {warehouseDataState === "loading" ? (
        <i>Carregando...</i>
      ) : (
        <>
          <ul>
            {warehouseData.map((warehouse) => (
              <li key={warehouse.id}>
                {warehouse.description} (D-{warehouse.id})
              </li>
            ))}
          </ul>
          {account && (
            <button onClick={() => dialog.current.showModal()}>
              Adicionar centro
            </button>
          )}
        </>
      )}
      <dialog ref={dialog} onClose={addWarehouse}>
        <h2>Adicionar centro de distribuição</h2>
        <form method="dialog">
          <label htmlFor="nome">Nome: </label>
          <input
            required
            type="text"
            name="nome"
            id="nome"
            value={warehouseName}
            onChange={(e) => setWarehouseName(e.target.value)}
          />
          <button value="cancel" formNoValidate>
            Cancelar
          </button>
          <button value="add">Adicionar</button>
        </form>
      </dialog>
    </>
  );
}
