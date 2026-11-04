from decimal import Decimal, InvalidOperation
from flask import flash, redirect, render_template, request, url_for
from app.extensions import db
from app.models import Cliente, Pedido, Producto
from . import bp_pedidos

@bp_pedidos.get("/")
def listar():
    pedidos = Pedido.query.order_by(Pedido.fecha.desc(), Pedido.id.desc()).all()
    return render_template("pedidos/lista.html", pedidos=pedidos)

@bp_pedidos.route("/nuevo", methods=["GET", "POST"])
def nuevo():
    clientes = Cliente.query.order_by(Cliente.nombre).all()
    productos = Producto.query.filter(Producto.stock > 0).order_by(Producto.nombre).all()
    if request.method == "POST":
        try:
            cliente_id = int(request.form.get("cliente_id", ""))
            producto_id = int(request.form.get("producto_id", ""))
            cantidad = int(request.form.get("cantidad", ""))
        except ValueError:
            flash("Selecciona un cliente, un producto y una cantidad válida.", "danger")
            return render_template("pedidos/formulario.html", clientes=clientes, productos=productos)
        cliente = db.session.get(Cliente, cliente_id)
        producto = db.session.get(Producto, producto_id)
        if not cliente or not producto or cantidad < 1:
            flash("Los datos del pedido no son válidos.", "danger")
        elif producto.stock < cantidad:
            flash("No hay stock suficiente para completar el pedido.", "danger")
        else:
            try:
                monto = Decimal(producto.precio) * cantidad
            except (InvalidOperation, TypeError):
                flash("No se pudo calcular el monto del pedido.", "danger")
            else:
                pedido = Pedido(monto=monto, cliente=cliente, producto=producto)
                producto.stock -= cantidad
                db.session.add(pedido)
                db.session.commit()
                flash("El pedido se registró y el inventario se actualizó.", "success")
                return redirect(url_for("pedidos.listar"))
    return render_template("pedidos/formulario.html", clientes=clientes, productos=productos)

@bp_pedidos.post("/<int:pedido_id>/eliminar")
def eliminar(pedido_id):
    pedido = db.get_or_404(Pedido, pedido_id)
    db.session.delete(pedido)
    db.session.commit()
    flash("El pedido se eliminó correctamente.", "success")
    return redirect(url_for("pedidos.listar"))
