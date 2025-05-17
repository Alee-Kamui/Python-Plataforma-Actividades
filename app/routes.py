from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.forms import TareaForm, RegistroForm, LoginForm
from app.models import Tarea, Usuario
from app import db

main = Blueprint('main', __name__)

@main.route('/')
def inicio():
    return redirect(url_for('main.ver_tareas'))

@main.route('/crear-tarea', methods=['GET', 'POST'])
@login_required
def crear_tarea():
    form = TareaForm()
    if form.validate_on_submit():
        nueva_tarea = Tarea(
            titulo=form.titulo.data,
            descripcion=form.descripcion.data,
            asignado_a=form.asignado_a.data
        )
        db.session.add(nueva_tarea)
        db.session.commit()
        flash("Tarea creada exitosamente", "success")
        return redirect(url_for('main.ver_tareas'))
    return render_template('crear_tarea.html', form=form)

@main.route('/tareas')
@login_required
def ver_tareas():
    page = request.args.get('page', 1, type=int)
    tareas = Tarea.query.order_by(Tarea.id.desc()).paginate(
        page=page,
        per_page=10,
        error_out=False
    )
    return render_template('tareas.html', tareas=tareas)

@main.route('/buscar-tareas', methods=['GET'])
@login_required
def buscar_tareas():
    query = request.args.get('q', '').strip()
    tareas = Tarea.query.filter(
        (Tarea.titulo.ilike(f'%{query}%')) |
        (Tarea.asignado_a.ilike(f'%{query}%'))
    ).order_by(Tarea.id.desc()).paginate(
        page=request.args.get('page', 1, type=int),
        per_page=5,
        error_out=False
    )
    return render_template('tareas.html', tareas=tareas, query=query)

@main.route('/registro', methods=['GET', 'POST'])
def registro():
    form = RegistroForm()
    if form.validate_on_submit():
        if Usuario.query.filter_by(email=form.email.data).first():
            flash('Ese correo ya está registrado', 'danger')
            return redirect(url_for('main.registro'))
        usuario = Usuario(
            nombre=form.nombre.data,
            email=form.email.data,
            rol=form.rol.data
        )
        usuario.set_password(form.contraseña.data)
        db.session.add(usuario)
        db.session.commit()
        flash('Usuario registrado correctamente. Ahora puedes iniciar sesión.', 'success')
        return redirect(url_for('main.login'))
    return render_template('registro.html', form=form)

@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        usuario = Usuario.query.filter_by(email=form.email.data).first()
        if usuario and usuario.check_password(form.contraseña.data):
            login_user(usuario)
            flash(f'Bienvenido {usuario.nombre}', 'success')
            return redirect(url_for('main.ver_tareas'))
        else:
            flash('Credenciales inválidas', 'danger')
    return render_template('login.html', form=form)

@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Sesión cerrada correctamente', 'info')
    return redirect(url_for('main.login'))