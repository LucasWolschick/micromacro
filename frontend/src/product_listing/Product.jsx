import "./Product.css";

export default function Product({ product, onSelected }) {
  const formattedPrice = product.price.toLocaleString(undefined, {
    style: "currency",
    currency: "BRL",
  });
  const productStock = product.stock.total_quantity;
  return (
    <div className="product">
      <div>
        <b>{product.description}</b> - {formattedPrice} - {productStock} un.{" "}
      </div>
      <button className="details-button" onClick={() => onSelected()}>
        ✏️
      </button>
    </div>
  );
}
