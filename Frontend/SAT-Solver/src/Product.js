import React from "react";
import "./Product.css";

function Product({info,name,image,button}) {
  return (
    <div className="product">
      <div className="product_info">
        <p>{info}</p>
        <p className="product_name">
          <strong>{name}</strong>
        </p>
      </div>
      <img
        src={image}
        alt=""
      />
      <button>{button}</button>
    </div>
  );
}

export default Product;
