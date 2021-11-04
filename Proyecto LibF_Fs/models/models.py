from typing import NamedTuple, Optional

class Cliente:
    def __init__(self, id_cli, usuario_cli, contraseña_cli):
        self.id_cli = id_cli
        self.usuario_cli = usuario_cli
        self.contraseña_cli = contraseña_cli
    def _repr_(self):
        return f'<Cliente: {self.usuario_cli}>'

class Empleado:
    def __init__(self, id_emp, usuario_emp, contraseña_emp):
        self.id_emp = id_emp
        self.usuario_emp = usuario_emp
        self.contraseña_emp = contraseña_emp
    def __repr__(self):
        return f'<Empleado: {self.usuario_emp}>'

class Libro:
    def __init__(self, id_Libro, nombre_Libro, fecha_Publicacion_Libro, autor_Libro, categoria_Libro, editorial_Libro, stock_Libro, precio_Libro):
        self.id_Libro = id_Libro
        self.nombre_Libro = nombre_Libro
        self.fecha_Publicacion_Libro = fecha_Publicacion_Libro
        self.autor_Libro = autor_Libro
        self.categoria_Libro = categoria_Libro
        self.editorial_Libro = editorial_Libro
        self.stock_Libro = stock_Libro
        self.precio_Libro = precio_Libro

    def __repr__(self):
        return f'<Libro: {self.nombre_Libro}>'


class Compra:
    def __init__(self, id_Compra, fechaCompra, precio_Total_Compra, proveedor_Compra):
        self.id_Compra = id_Compra
        self.fechaCompra = fechaCompra
        self.precio_Total_Compra = precio_Total_Compra
        self.proveedor_Compra = proveedor_Compra
    def _repr_(self):
        return f'<Compra: {self.precio_Total_Compra}>'


class Autor:
    def __init__(self, id_Autor, nombre_Autor, apellido_Autor, fecha_Nacimiento_Autor, nacionalidad_Autor):
        self.id_Autor = id_Autor
        self.nombre_Autor = nombre_Autor
        self.apellido_Autor = apellido_Autor
        self.fecha_Nacimiento_Autor = fecha_Nacimiento_Autor
        self.nacionalidad_Autor = nacionalidad_Autor
    def __repr__(self):
        return f'<Autor: {self.nombre_Autor}>'


class Proveedor:
    def __init__(self, id_Proveedor, desc_Proveedor, direccionProveedor, localidad_Proveedor):
        self.id_Proveedor = id_Proveedor
        self.desc_Proveedor = desc_Proveedor
        self.direccionProveedor = direccionProveedor
        self.localidad_Proveedor = localidad_Proveedor
    def __repr__(self):
        return f'<Proveedor: {self.desc_Proveedor}>'


class Comentario:
    def __init__(self, id_Comentario, comentarios, fecha_Comentario):
        self.id_Comentario = id_Comentario
        self.comentarios = comentarios
        self.fecha_Comentario = fecha_Comentario
    def __repr__(self):
        return f'<Comentario: {self.comentarios}>'