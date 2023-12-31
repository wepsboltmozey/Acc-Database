from flask import Flask, render_template, request, redirect, url_for, flash
import pyodbc

app = Flask(__name__)
app.config['SECRET_KEY'] = 'moses1234'



DB_DRIVER = '{Microsoft Access Driver (*.mdb, *.accdb)}'
DB_FILE = r'C:\Users\WEP\Desktop\Acc Database\database\data\data.accdb'  # Change this to your database file path

# Establish a connection to the database
conn_str = f'DRIVER={DB_DRIVER};DBQ={DB_FILE}'
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()


@app.route('/')
def index():
    # Display the list of records
    cursor.execute('SELECT * FROM Students')
    records = cursor.fetchall()
    return render_template('add.html', records=records)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        reg_number = request.form['reg_number']
        name = request.form['name']
        email = request.form['email']
        contact = request.form['contact']
        sex = request.form['sex']

        try:
            # Check if reg_number already exists
            cursor.execute(f"SELECT * FROM Students WHERE reg_number='{reg_number}'")
            existing_record = cursor.fetchone()

            if existing_record:
                flash('Record with the same reg_number already exists. Please change the registration number.', 'warning')
            else:
                # Insert the new record
                cursor.execute("INSERT INTO Students (reg_number, name, email, contact, sex) "
                               f"VALUES ('{reg_number}', '{name}', '{email}', '{contact}', '{sex}')")
                conn.commit()
                flash('Record added successfully!', 'success')

        except Exception as e:
            flash(f'An error occurred: {str(e)}', 'danger')

    return redirect(url_for('index'))





@app.route('/update', methods=['POST', 'GET'])
def update():
    if request.method == 'POST':
        reg_number = request.form['reg_number']

        try:
            # Assuming you have a cursor and connection set up
            cursor.execute(f"SELECT * FROM Students WHERE reg_number='{reg_number}'")
            record = cursor.fetchone()

            if record:
                # Convert the record to a dictionary for easy access in the template
                record_dict = {
                    'reg_number': record.reg_number,
                    'name': record.name,
                    'email': record.email,
                    'contact': record.contact,
                    'sex': record.sex
                }

                return render_template('update.html', record=record_dict)
            else:
                flash(f'Record with Students {reg_number} not found', 'danger')

        except Exception as e:
            flash(f'An error occurred: {str(e)}', 'danger')

    return render_template('update.html', record=None)


@app.route('/update_record', methods=['POST'])
def update_record():
    if request.method == 'POST':
        reg_number = request.form['reg_number']
        name = request.form['name']
        email = request.form['email']
        contact = request.form['contact']
        sex = request.form['sex']

        try:
            # Update the record in the database
            cursor.execute(f"UPDATE Students SET name='{name}', email='{email}', "
                           f"contact='{contact}', sex='{sex}' WHERE reg_number='{reg_number}'")
            conn.commit()
            flash('Record updated successfully!', 'success')

        except Exception as e:
            flash(f'An error occurred: {str(e)}', 'danger')

    return redirect(url_for('update'))


if __name__ == '__main__':
    app.run(debug=True)
