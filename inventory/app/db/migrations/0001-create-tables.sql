CREATE TABLE warehouses (
    id SERIAL PRIMARY KEY NOT NULL,
    description TEXT NOT NULL
);

CREATE TABLE stocks (
    id SERIAL PRIMARY KEY NOT NULL,
    product_id INT NOT NULL,
    warehouse_id INT NOT NULL,
    stock NUMERIC NOT NULL,

    CONSTRAINT product_id_warehouse_id_unique UNIQUE (product_id, warehouse_id),
    CONSTRAINT warehouse_id_warehouses_fk FOREIGN KEY (warehouse_id) REFERENCES warehouses (id)
);