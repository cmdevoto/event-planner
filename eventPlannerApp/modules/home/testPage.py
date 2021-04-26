
from flask import redirect, render_template

from . import bp
from ... import dbInterface
from flask_login import current_user, login_user, LoginManager
@bp.route("/test/databaseRetrieveItems")
@login_required
def testDatabaseRetrieveItemsRoute():
    resultingProducts = dbInterface.fetchAll("select * from product", {})
    data = {
        "products": resultingProducts
    }
    return render_template("home/testPage.html", data=data)

@bp.route("/test/databaseInsertItems/<int:prod_id>/<string:item_name>")
def testDatabaseInsertItemsRoute(prod_id, item_name):
    insert_query = "insert into product values (:prod_id, :prod_desc, :manufactr_id, :cost, :price)"
    insert_params = {
        "prod_id": prod_id,
        "prod_desc": item_name,
        "manufactr_id": 253,
        "cost": 10,
        "price": 14.5
        }
    result = dbInterface.commit(insert_query, insert_params)
    return redirect("/test/databaseRetrieveItems")

@bp.route("/test/databaseConnection")
def testDatabaseConnectionRoute():
    if (dbInterface.__getDatabaseConnection__()):
        return "SUCCESS"
    else:
        return "Damn it"
