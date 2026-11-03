from decimal import Decimal, InvalidOperation
from flask import flash, redirect, render_template, request, url_for
from sqlalchemy import func
from app.extensions import db
from app.models import Producto
from . import bp_productos


def leer_formulario():
    nombre = request.form.get("nombre", "").strip()
    try:
        precio = Decimal(request.form.get("precio", ""))
        stock = int(request.form.get("stock", ""))
    except (InvalidOperation, ValueError):
        return None, "El precio y el stock deben ser números válidos."
    if not nombre or precio <= 0 or stock < 0:
        return None, "Ingresa un nombre, un precio mayor a cero y un stock válido."
    return {"nombre": nombre, "precio": precio, "stock": stock}, None


@bp_productos.get("/")
def listar():
    termino = request.args.get("q", "").strip()
    consulta = Producto.query
    if termino:
        consulta = consulta.filter(func.lower(Producto.nombre).contains(termino.lower()))
    productos = consulta.order_by(Producto.nombre).all()
    return render_template("productos/lista.html", productos=productos, termino=termino)


@bp_productos.route("/nuevo", methods=["GET", "POST"])
def nuevo():
    if request.method == "POST":
        datos, error = leer_formulario()
        if error:
            flash(error, "danger")
        else:
            db.session.add(Producto(**datos))
            db.session.commit()
            flash("El producto se registró correctamente.", "success")
            return redirect(url_for("productos.listar"))
    return render_template("productos/formulario.html", producto=None)


@bp_productos.route("/<int:producto_id>/editar", methods=["GET", "POST"])
def editar(producto_id):
    producto = db.get_or_404(Producto, producto_id)
    if request.method == "POST":
        datos, error = leer_formulario()
        if error:
            flash(error, "danger")
        else:
            for campo, valor in datos.items():
                setattr(producto, campo, valor)
            db.session.commit()
            flash("El producto se actualizó correctamente.", "success")
            return redirect(url_for("productos.listar"))
    return render_template("productos/formulario.html", producto=producto)


@bp_productos.post("/<int:producto_id>/eliminar")
def eliminar(producto_id):
    producto = db.get_or_404(Producto, producto_id)
    if producto.pedidos:
        flash("No se puede eliminar un producto que aparece en pedidos registrados.", "warning")
    else:
        db.session.delete(producto)
        db.session.commit()
        flash("El producto se eliminó correctamente.", "success")
    return redirect(url_for("productos.listar"))
