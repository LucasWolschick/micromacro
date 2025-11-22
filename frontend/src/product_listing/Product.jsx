export default function Product({ product, onSelected }) {
  const formattedPrice = product.price.toLocaleString(undefined, {
    style: "currency",
    currency: "BRL",
  });
  const productStock = product.stock.total_quantity;
  return (
    <div>
      <b>{product.description}</b> - {formattedPrice} - {productStock} un.{" "}
      <button onClick={() => onSelected()}>Detalhes</button>
    </div>
  );
}
