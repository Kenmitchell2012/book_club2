from flask_app import app
from flask import render_template, redirect, url_for, request, flash, session
from flask_app.models.user import User
from flask_app.models.book import Book


@app.route('/createbook', methods=['POST'])
def create_book():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    print(session['user_id'])
    if not Book.validate_book(request.form):
        alert = 'Please fill all the fields'
        return redirect(url_for('dashboard', alert=alert))
    new_book = {
        'user_id': session['user_id'],
        'creator': session['user_id'],
        'title': request.form['title'],
        'description': request.form['description'],
    }
    print(new_book)
    Book.save_book(new_book)
    return redirect(url_for('dashboard'))

# edit book
@app.route('/edit/<int:book_id>')
def edit_book(book_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    book = Book.get_book_by_id(book_id)
    user = User.get_by_id(session['user_id'])
    return render_template('edit_book.html', book=book, user=user)

# update book
@app.route('/update/<int:book_id>', methods=['POST'])
def update(book_id):
    if 'user_id' not in session:
        return redirect(url_for('login'))
    print("From update route", session['user_id'])
    if not Book.validate_book(request.form):
        return redirect(f'/edit/{book_id}')
    data = {
        'user_id': session['user_id'],
        'title': request.form['title'],
        'description': request.form['description']
    }
    print(data)
    Book.update_book(book_id, data)
    flash('Book successfully updated', 'update_book')
    return redirect(url_for('dashboard'))

# view book
@app.route('/view/<int:book_id>')
def view_book(book_id):
    if 'user_id' not in session:
        return redirect('/login')
    user_id = session['user_id']
    user = User.get_by_id(user_id)
    book = Book.get_book_by_id(book_id)
    return render_template('view.html', book=book, user=user)

# delete book
@app.route('/delete/<int:book_id>')
def delete_book(book_id):
    if 'user_id' not in session:
        return redirect('/login')

    book = Book.get_book_by_id(book_id)
    book.delete_book(book_id)
    flash('success', 'Book deleted successfully', 'delete')
    return redirect('/dashboard')