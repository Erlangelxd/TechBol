# TechBol

Sistema web modular para administrar productos, clientes y pedidos con Flask, SQLAlchemy, SQLite y Bootstrap.

## Requisitos

Python 3.10 o posterior.

## Preparar el entorno

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

En Windows PowerShell activa el entorno con `venv\Scripts\Activate.ps1`.

## Crear la base de datos

```bash
flask --app run db init
flask --app run db migrate -m "Crea las tablas iniciales de TechBol"
flask --app run db upgrade
```

## Cargar datos de demostración

```bash
flask --app run datos-demo
```

## Iniciar la aplicación

```bash
flask --app run run --debug
```

Abre `http://127.0.0.1:5000` en el navegador. La aplicación permite registrar, editar, buscar y eliminar productos y clientes, además de crear y consultar pedidos. El monto del pedido se calcula con el precio del producto y la cantidad, y se descuenta el stock disponible.
