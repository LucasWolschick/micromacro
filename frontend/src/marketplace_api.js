const MARKETPLACE_BASE_URL = import.meta.env.VITE_MARKETPLACE_BASE_URL;

export function login({ username, password }) {
  return fetch(`${MARKETPLACE_BASE_URL}/login`, {
    method: "POST",
    body: new URLSearchParams({
      username,
      password,
    }),
  }).then((result) => result.json());
}

export function updateStock({ sku, token, warehouseId, quantity }) {
  return fetch(`${MARKETPLACE_BASE_URL}/products/${sku}/stock`, {
    method: "PUT",
    headers: {
      Authorization: `Bearer ${token}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      warehouse_id: warehouseId,
      quantity,
    }),
  }).then((result) => result.json());
}

export function listProducts() {
  return fetch(`${MARKETPLACE_BASE_URL}/products`).then((response) =>
    response.json()
  );
}

export function listWarehouses() {
  return fetch(`${MARKETPLACE_BASE_URL}/inventory/warehouses`).then(
    (response) => response.json()
  );
}

export function addProduct({ token, productName, productPrice }) {
  return fetch(`${MARKETPLACE_BASE_URL}/products`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${token}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      description: productName,
      price: productPrice,
    }),
  }).then((response) => response.json());
}

export function createWarehouse({ token, description }) {
  return fetch(`${MARKETPLACE_BASE_URL}/inventory/warehouses`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${token}`,
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ description }),
  });
}
