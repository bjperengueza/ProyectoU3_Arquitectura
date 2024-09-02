import requests
from flask import Blueprint, render_template, request, redirect, url_for, flash

users_routes = Blueprint('users_routes', __name__)

API_BASE_URL = 'http://localhost:4300/api/users'

@users_routes.route('/')
def list_users():
    response = requests.get(API_BASE_URL)
    if response.status_code == 200:
        users = response.json()
        return render_template('user_list.html', users=users)
    else:
        flash("Error fetching users", "error")
        return render_template('user_list.html', users=[])

@users_routes.route('/<int:id>')
def get_user(id):
    response = requests.get(f'{API_BASE_URL}/{id}')
    if response.status_code == 200:
        user = response.json()
        return render_template('user_detail.html', user=user)
    else:
        flash("User not found", "error")
        return redirect(url_for('users_routes.list_users'))

@users_routes.route('/create', methods=['GET', 'POST'])
def create_user():
    if request.method == 'POST':
        user_data = {
            "username": request.form['username'],
            "email": request.form['email'],
            "password": request.form['password']
        }
        response = requests.post(API_BASE_URL, json=user_data)
        if response.status_code == 201:
            flash("User created successfully", "success")
            return redirect(url_for('users_routes.list_users'))
        else:
            flash(response.json().get('error', 'Error creating user'), "error")
    return render_template('user_form.html')

@users_routes.route('/<int:id>/edit', methods=['GET', 'POST'])
def edit_user(id):
    if request.method == 'POST':
        user_data = {
            "username": request.form['username'],
            "email": request.form['email'],
            "password": request.form.get('password')  # Password is optional on edit
        }
        response = requests.put(f'{API_BASE_URL}/{id}', json=user_data)
        if response.status_code == 200:
            flash("User updated successfully", "success")
            return redirect(url_for('users_routes.list_users'))
        else:
            flash(response.json().get('error', 'Error updating user'), "error")

    response = requests.get(f'{API_BASE_URL}/{id}')
    if response.status_code == 200:
        user = response.json()
        return render_template('user_form.html', user=user)
    else:
        flash("User not found", "error")
        return redirect(url_for('users_routes.list_users'))

@users_routes.route('/<int:id>/delete', methods=['POST'])
def delete_user(id):
    response = requests.delete(f'{API_BASE_URL}/{id}')
    if response.status_code == 200:
        flash("User deleted successfully", "success")
    else:
        flash(response.json().get('error', 'Error deleting user'), "error")
    return redirect(url_for('users_routes.list_users'))
