import flask
from flask_restful import Api, Resource
import program

app = flask.Flask(__name__)
api = Api(app)


class RequestDataProduct(Resource):
    def get(self, store, name):
        try:
            data = program.DB().get(store, name)
            if len(data) > 0:
                return data, 200
            else:
                return {"message": "Product not found"}, 404
        except Exception as e:
            return {"error": str(e)}, 500

    def post(self):
        try:
            data = flask.request.get_json()
            store = data.get('store')
            name = data.get('name')
            price = data.get('price')

            if not store or not name or not price:
                return {"message": "Missing data: 'store', 'name' or 'price'"}, 400

            program.DB().post(store, name, price)
            return {"message": "Product added successfully"}, 201
        except Exception as e:
            return {"error": str(e)}, 500

    def put(self, store, name):
        try:
            data = flask.request.get_json()
            new_price = data.get('price')

            if not new_price:
                return {"message": "Missing 'price' field"}, 400

            existing_data = program.DB().get(store, name)
            if len(existing_data) == 0:
                return {"message": "Product not found"}, 404

            # Оновлення продукту
            program.DB().cursor.execute(f"""
                UPDATE {store} SET price = ? WHERE name = ?
            """, (new_price, name))
            program.DB().conn.commit()

            return {"message": "Product updated successfully"}, 200
        except Exception as e:
            return {"error": str(e)}, 500

    def delete(self, store, name):
        try:
            existing_data = program.DB().get(store, name)
            if len(existing_data) == 0:
                return {"message": "Product not found"}, 404

            # Видалення продукту
            program.DB().cursor.execute(f"""
                DELETE FROM {store} WHERE name = ?
            """, (name,))
            program.DB().conn.commit()

            return {"message": "Product deleted successfully"}, 200
        except Exception as e:
            return {"error": str(e)}, 500


class RequestDataStore(Resource):
    def get(self, store):
        try:
            data = program.DB().get_all_from_store(store)
            return data, 200
        except Exception as e:
            return {"error": str(e)}, 500


api.add_resource(RequestDataProduct, "/data/", '/data/<store>/<name>')
api.add_resource(RequestDataStore, '/store/<store>')
app.run(debug=True)

