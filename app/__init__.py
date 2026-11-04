from pathlib import Path
from flask import Flask, redirect, url_for
from config import Config
from .extensions import db, migrate


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    Path(app.instance_path).mkdir(parents=True, exist_ok=True)
    db.init_app(app)
    migrate.init_app(app, db)

    from . import models
    from .clientes import bp_clientes
    from .productos import bp_productos
    from .pedidos import bp_pedidos

    app.register_blueprint(bp_clientes, url_prefix="/clientes")
    app.register_blueprint(bp_productos, url_prefix="/productos")
    app.register_blueprint(bp_pedidos, url_prefix="/pedidos")

    @app.get("/")
    def inicio():
        return redirect(url_for("productos.listar"))

    @app.cli.command("datos-demo")
    def datos_demo():
        if not models.Cliente.query.first():
            db.session.add_all([
                models.Cliente(nombre="Erlan Angel", telefono="73597158"),
                models.Cliente(nombre="Luz Lorena", telefono="34541290"),
            ])
        if not models.Producto.query.first():
            db.session.add_all([
                models.Producto(nombre="Laptop Lenovo", precio=5200, stock=8),
                models.Producto(nombre="Mouse inalámbrico", precio=95, stock=25),
                models.Producto(nombre="Teclado mecánico", precio=350, stock=12),
            ])
        db.session.commit()
        print("Datos de demostración cargados.")

    return app
