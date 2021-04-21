
from flask import render_template

from . import bp
from ... import dbInterface

@bp.route("/test/databaseItems")
def testDatabaseItemsRoute():
    resultingProducts = dbInterface.fetchAll("select * from product", {})
    data = {
        products: resultingProducts
    }
    return render_template("home/testPage.html", data=data)

@bp.route("/test/databaseConnection")
def testDatabaseConnectionRoute():
    if (dbInterface.__getDatabaseConnection__()):
        return "SUCCESS"
    else:
        return "Damn it"
