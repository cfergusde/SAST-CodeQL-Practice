import sqlite3
from flask import Flask, request, render_template_string

app = Flask(__name__)

# Initialize the database
def init_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT,
        password TEXT
    )''')
    # Insert some test data
    cursor.execute("INSERT OR IGNORE INTO users VALUES (1, 'admin', 'secretpassword')")
    conn.commit()
    conn.close()


# Vulnerable function with SQL Injection
@app.route('/search', methods=['GET'])
def search_users():
    username = request.args.get('username', '')
    
    # Vulnerable SQL query construction (string concatenation)
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    
    # VULNERABILITY: Direct concatenation of user input into SQL query
    query = "SELECT * FROM users WHERE username LIKE '%" + username + "%'"
    
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    
    # Display results
    template = '''
    <h1>Search Results for: {{ username }}</h1>
    <ul>
    {% for user in results %}
        <li>{{ user }}</li>
    {% endfor %}
    </ul>
    '''
    
    return render_template_string(template, username=username, results=results)

# Another vulnerability: Path traversal
@app.route('/getfile', methods=['GET'])
def get_file():
    filename = request.args.get('filename', '')
    
    # VULNERABILITY: Path traversal vulnerability
    try:
        with open(filename, 'r') as f:
            content = f.read()
        return content
    except Exception as e:
        return f"Error: {str(e)}"

# Flask template injection vulnerability
@app.route('/render', methods=['GET'])
def render_template():
    template_data = request.args.get('template', '')
    
    # VULNERABILITY: Template injection
    return render_template_string(template_data)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)