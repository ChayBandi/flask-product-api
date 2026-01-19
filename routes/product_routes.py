

from flask_restx import Namespace, Resource, fields
from flask import request
from db_config import get_connection, release_connection

product_ns = Namespace("products", description="Product operations")

#used for post model
product_model = product_ns.model("Product", {
    "product_name": fields.String(required=True),
    "mrp": fields.Float(required=True),
    "quantity": fields.Integer(required=True)
})
# used for put method 
product_update_model = product_ns.model("ProductUpdate", {
    "mrp": fields.Float(required=False, description="Updated price"),
    "quantity": fields.Integer(required=False, description="Updated quantity")
})

#post model 
@product_ns.route("/")
class ProductList(Resource):

    @product_ns.expect(product_model)
    def post(self):
        data = request.json
        conn = get_connection()
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO products (product_name, mrp, quantity) VALUES (%s, %s, %s)",
            (data["product_name"], data["mrp"], data["quantity"])
        )

        conn.commit()
        cur.close()
        release_connection(conn)

        return {"message": "Product added successfully"}, 201

    def get(self):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("SELECT product_id, product_name, mrp, quantity FROM products")
        rows = cur.fetchall()

        products = []
        for r in rows:
            products.append({
                "product_id": r[0],
                "product_name": r[1],
                "mrp": float(r[2]),
                "quantity": r[3]
            })

        cur.close()
        release_connection(conn)

        return products

#put model

@product_ns.route("/<int:product_id>")
class Product(Resource):

    @product_ns.expect(product_update_model)
    def put(self, product_id):
        data = request.json

        if not data:
            return {"error": "Request body is required"}, 400

        fields = []
        values = []

        if "mrp" in data:
            fields.append("mrp = %s")
            values.append(data["mrp"])

        if "quantity" in data:
            fields.append("quantity = %s")
            values.append(data["quantity"])

        if not fields:
            return {"error": "No valid fields to update"}, 400

        values.append(product_id)

        query = f"""
            UPDATE products
            SET {', '.join(fields)}
            WHERE product_id = %s
        """

        conn = get_connection()
        cur = conn.cursor()
        cur.execute(query, tuple(values))

        if cur.rowcount == 0:
            return {"error": "Product not found"}, 404

        conn.commit()
        cur.close()
        release_connection(conn)

        return {"message": "Product updated successfully"}
    
    #delete model

    def delete(self, product_id):
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("DELETE FROM products WHERE product_id = %s", (product_id,))
        conn.commit()

        cur.close()
        release_connection(conn)

        return {"message": "Product deleted"}
    


