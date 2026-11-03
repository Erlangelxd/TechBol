from flask import flash, redirect, render_template, request, url_for
from sqlalchemy import func
from app.extensions import db
from app.models import Cliente
from . import bp_clientes


@bp_clientes.get("/")
def listar():
    termino = request.args.get("q", "").strip()
    consulta = Cliente.query
    if termino:
        consulta = consulta.filter(func.lower(Cliente.nombre).contains(termino.lower()))
    return render_template("clientes/lista.html", clientes=consulta.order_by(Cliente.nombre).all(), termino=termino)


@bp_clientes.route("/nuevo", methods=["GET", "POST"])
def nuevo():
    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        telefono = request.form.get("telefono", "").strip()
        if not nombre or not telefono:
            flash("Completa el nombre y el teléfono.", "danger")
        else:
            db.session.add(Cliente(nombre=nombre, telefono=telefono))
            db.session.commit()
            flash("El cliente se registró correctamente.", "success")
            return redirect(url_for("clientes.listar"))
    return render_template("clientes/formulario.html", cliente=None)


@bp_clientes.route("/<int:cliente_id>/editar", methods=["GET", "POST"])
def editar(cliente_id):
    cliente = db.get_or_404(Cliente, cliente_id)
    if request.method == "POST":
        nombre = request.form.get("nombre", "").strip()
        telefono = request.form.get("telefono", "").strip()
        if not nombre or not telefono:
            flash("Completa el nombre y el teléfono.", "danger")
        else:
            cliente.nombre = nombre
            cliente.telefono = telefono
            db.session.commit()
            flash("El cliente se actualizó correctamente.", "success")
            return redirect(url_for("clientes.listar"))
    return render_template("clientes/formulario.html", cliente=cliente)


@bp_clientes.post("/<int:cliente_id>/eliminar")
def eliminar(cliente_id):
    cliente = db.get_or_404(Cliente, cliente_id)
    if cliente.pedidos:
        flash("No se puede eliminar un cliente que tiene pedidos registrados.", "warning")
    else:
        db.session.delete(cliente)
        db.session.commit()
        flash("El cliente se eliminó correctamente.", "success")
    return redirect(url_for("clientes.listar"))
