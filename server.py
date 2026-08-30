import os
import sqlite3
import uuid
from datetime import datetime
from pathlib import Path

from flask import Flask, jsonify, redirect, request, send_from_directory, session
from werkzeug.security import check_password_hash, generate_password_hash

ROOT_DIR = Path(__file__).resolve().parent
DB_PATH = Path(os.environ.get('CMMS_DB_PATH', ROOT_DIR / 'cmms.db'))
DEFAULT_ADMIN_USERNAME = os.environ.get('CMMS_ADMIN_USER', 'admin')
DEFAULT_ADMIN_PASSWORD = os.environ.get('CMMS_ADMIN_PASSWORD', 'FixingSpaces123!')
ROOT_ADMIN_USERNAME = os.environ.get('CMMS_ROOT_USER', 'phillip.eubanks@livingspaces.com')
ROOT_ADMIN_PASSWORD = os.environ.get('CMMS_ROOT_PASSWORD', '131171')

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
app.secret_key = os.environ.get('CMMS_SECRET_KEY', 'cmms-local-dev-secret-change-me')

PUBLIC_API = {'/api/login', '/api/signup', '/api/session', '/api/health'}
PUBLIC_PATHS = {'/login.html', '/signup.html', '/favicon.ico'}
PUBLIC_STATIC_SUFFIXES = {'.css', '.js', '.png', '.jpg', '.jpeg', '.svg', '.ico', '.gif', '.webp', '.woff', '.woff2', '.ttf', '.map'}


def make_assets():
    assets = [{"id": "GROUNDS", "name": "Facility Grounds", "group": "Facility"}]
    for i in range(1, 76):
        assets.append({"id": f"IN-D{str(i).zfill(2)}", "name": f"Dock Door {i}", "group": "Inbound Dock Doors"})
    for i in range(101, 176):
        assets.append({"id": f"OUT-D{str(i).zfill(3)}", "name": f"Dock Door {i}", "group": "Outbound Dock Doors"})
    for i in range(1, 6):
        assets.append({"id": f"EPJ{str(i).zfill(2)}", "name": f"EPJ{str(i).zfill(2)}", "group": "PIT - Electric Pallet Jacks"})
    assets.extend([
        {"id": "SD26", "name": "SD26", "group": "PIT - Forklifts & Reach Trucks"},
        {"id": "REACH", "name": "REACH", "group": "PIT - Forklifts & Reach Trucks"},
        {"id": "UTIL-COMP-01", "name": "Ingersoll Rand RSA11-22 Air Compressor", "group": "Facility Utilities"},
        {"id": "REC-AUG-01", "name": "Komar EM-15W Auger-Pak Trash Auger", "group": "Recycling Department"},
        {"id": "REC-GMX-01", "name": "GreenMax M-C300 Styrofoam Extruder", "group": "Recycling Department"},
        {"id": "REC-CON-01", "name": "Harris Above-Ground Conveyor", "group": "Recycling Department"},
        {"id": "REC-BAL-01", "name": "Cram-A-Lot Plastic Baler", "group": "Recycling Department"},
        {"id": "REC-BAL-02", "name": "Harris 29N Series Cardboard Baler", "group": "Recycling Department"},
    ])
    for i in range(1, 21):
        assets.append({"id": f"OP{str(i).zfill(2)}", "name": f"OP{str(i).zfill(2)}", "group": "PIT - Order Pickers"})
    return assets


def make_manual_parts():
    return [
        {"name": "Crusher blade", "asset": "GreenMax M-C300", "source": "M-C300 Instruction Manual"},
        {"name": "Crusher bearing UCF212", "asset": "GreenMax M-C300", "source": "M-C300 Instruction Manual"},
        {"name": "Spherical roller bearing #22319", "asset": "GreenMax M-C300", "source": "M-C300 Instruction Manual"},
        {"name": "Tapered roller bearing #32319", "asset": "GreenMax M-C300", "source": "M-C300 Instruction Manual"},
        {"name": "16A drive chain", "asset": "GreenMax M-C300", "source": "M-C300 Instruction Manual"},
        {"name": "Heater bands", "asset": "GreenMax M-C300", "source": "M-C300 Instruction Manual"},
        {"name": "Hydraulic hose and fittings", "asset": "Cram-A-Lot HE-60", "source": "HE Series Brochure"},
        {"name": "Main cylinder seal kit", "asset": "Cram-A-Lot HE-60", "source": "HE Series Brochure"},
        {"name": "Door cylinder seal kit", "asset": "Cram-A-Lot HE-60", "source": "HE Series Brochure"},
        {"name": "Adjustable shear blade", "asset": "Cram-A-Lot HE-60", "source": "HE Series Brochure"},
        {"name": "Photocell", "asset": "Cram-A-Lot HE-60", "source": "HE Series Brochure"},
        {"name": "Controller component", "asset": "Cram-A-Lot HE-60", "source": "HE Series Brochure"},
        {"name": "Crusher motor", "asset": "GreenMax M-C300", "source": "M-C300 Instruction Manual"},
        {"name": "Crusher gearbox", "asset": "GreenMax M-C300", "source": "M-C300 Instruction Manual"},
        {"name": "Driving crusher", "asset": "GreenMax M-C300", "source": "M-C300 Instruction Manual"},
        {"name": "Passive crusher", "asset": "GreenMax M-C300", "source": "M-C300 Instruction Manual"},
        {"name": "Connection flange", "asset": "GreenMax M-C300", "source": "M-C300 Instruction Manual"},
        {"name": "Inspection window safety switch", "asset": "GreenMax M-C300", "source": "M-C300 Instruction Manual"},
        {"name": "Crusher bin", "asset": "GreenMax M-C300", "source": "M-C300 Instruction Manual"},
        {"name": "Control box", "asset": "GreenMax M-C300", "source": "M-C300 Instruction Manual"},
        {"name": "Transportation fan", "asset": "GreenMax M-C300", "source": "M-C300 Instruction Manual"},
        {"name": "Wind pipe", "asset": "GreenMax M-C300", "source": "M-C300 Instruction Manual"},
        {"name": "Silo", "asset": "GreenMax M-C300", "source": "M-C300 Instruction Manual"},
        {"name": "Silo bracket", "asset": "GreenMax M-C300", "source": "M-C300 Instruction Manual"},
        {"name": "Extruder motor M1", "asset": "GreenMax M-C300", "source": "M-C300 Instruction Manual"},
        {"name": "Extruder motor M2", "asset": "GreenMax M-C300", "source": "M-C300 Instruction Manual"},
        {"name": "Reducer 1", "asset": "GreenMax M-C300", "source": "M-C300 Instruction Manual"},
        {"name": "Reducer 2", "asset": "GreenMax M-C300", "source": "M-C300 Instruction Manual"},
        {"name": "Extruder screw", "asset": "GreenMax M-C300", "source": "M-C300 Instruction Manual"},
        {"name": "Machine barrel", "asset": "GreenMax M-C300", "source": "M-C300 Instruction Manual"},
        {"name": "Machine head flange", "asset": "GreenMax M-C300", "source": "M-C300 Instruction Manual"},
        {"name": "Oil fill port", "asset": "Cram-A-Lot HE-60", "source": "HE Series Brochure"},
        {"name": "Hydraulic reservoir", "asset": "Cram-A-Lot HE-60", "source": "HE Series Specifications"},
        {"name": "Hydraulic pump", "asset": "Cram-A-Lot HE-60", "source": "HE Series Specifications"},
        {"name": "Programmable controller", "asset": "Cram-A-Lot HE-60", "source": "HE Series Brochure"},
        {"name": "Automatic bale ejection system", "asset": "Cram-A-Lot HE-60", "source": "HE Series Brochure"},
        {"name": "Full-bale warning indicator", "asset": "Cram-A-Lot HE-60", "source": "HE Series Brochure"},
        {"name": "Advance warning indicator", "asset": "Cram-A-Lot HE-60", "source": "HE Series Brochure"},
        {"name": "Intake air filter", "asset": "Ingersoll Rand RSA11-22 Air Compressor", "source": "RSA11-22 Product Information"},
        {"name": "Inlet valve", "asset": "Ingersoll Rand RSA11-22 Air Compressor", "source": "RSA11-22 Product Information"},
        {"name": "Electric motor", "asset": "Ingersoll Rand RSA11-22 Air Compressor", "source": "RSA11-22 Product Information"},
        {"name": "Compressor air end", "asset": "Ingersoll Rand RSA11-22 Air Compressor", "source": "RSA11-22 Product Information"},
        {"name": "Belt drive", "asset": "Ingersoll Rand RSA11-22 Air Compressor", "source": "RSA11-22 Product Information"},
        {"name": "Oil fine separator element", "asset": "Ingersoll Rand RSA11-22 Air Compressor", "source": "RSA11-22 Product Information"},
        {"name": "Oil filter", "asset": "Ingersoll Rand RSA11-22 Air Compressor", "source": "RSA11-22 Product Information"},
        {"name": "Oil cooler", "asset": "Ingersoll Rand RSA11-22 Air Compressor", "source": "RSA11-22 Product Information"},
        {"name": "Air cooler", "asset": "Ingersoll Rand RSA11-22 Air Compressor", "source": "RSA11-22 Product Information"},
        {"name": "Oil temperature regulator", "asset": "Ingersoll Rand RSA11-22 Air Compressor", "source": "RSA11-22 Product Information"},
        {"name": "Cooling fan", "asset": "Ingersoll Rand RSA11-22 Air Compressor", "source": "RSA11-22 Product Information"},
        {"name": "Cooling air inlet filter mat", "asset": "Ingersoll Rand RSA11-22 Air Compressor", "source": "RSA11-22 Product Information"},
        {"name": "Pressure relief valve", "asset": "Ingersoll Rand RSA11-22 Air Compressor", "source": "RSA11-22 Product Information"},
        {"name": "Minimum pressure check valve", "asset": "Ingersoll Rand RSA11-22 Air Compressor", "source": "RSA11-22 Product Information"},
        {"name": "Oil level sight glass", "asset": "Ingersoll Rand RSA11-22 Air Compressor", "source": "RSA11-22 Product Information"},
        {"name": "Final compression temperature sensor", "asset": "Ingersoll Rand RSA11-22 Air Compressor", "source": "RSA11-22 Product Information"},
        {"name": "System pressure sensor", "asset": "Ingersoll Rand RSA11-22 Air Compressor", "source": "RSA11-22 Product Information"},
        {"name": "Emergency stop button", "asset": "Ingersoll Rand RSA11-22 Air Compressor", "source": "RSA11-22 Product Information"},
        {"name": "Solid-lube bearing support system", "asset": "Komar EM-15W Auger-Pak Trash Auger", "source": "Komar EM-15W manufacturer data"},
        {"name": "Chain and bearing lubrication system", "asset": "Komar EM-15W Auger-Pak Trash Auger", "source": "Komar EM-15W manufacturer data"},
    ]


def make_default_inventory():
    prefixes = {
        'GreenMax M-C300': 'FS-GMX',
        'Cram-A-Lot HE-60': 'FS-HE',
        'Ingersoll Rand RSA11-22 Air Compressor': 'FS-IR',
        'Komar EM-15W Auger-Pak Trash Auger': 'FS-KOM',
    }
    counts = {}
    inventory = []
    for part in make_manual_parts():
        prefix = prefixes.get(part['asset'], 'FS-OTH')
        counts[prefix] = counts.get(prefix, 0) + 1
        inventory.append({
            'id': f"{prefix}-{counts[prefix]:03d}",
            'name': part['name'],
            'partNumber': f"{prefix}-{counts[prefix]:03d}",
            'manufacturerPartNumber': '',
            'asset': part['asset'],
            'quantity': 0,
            'cost': 0,
            'reorder': 0,
            'source': part['source'],
        })
    return inventory


def get_db_connection():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()
    conn.execute(
        '''
        CREATE TABLE IF NOT EXISTS assets (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            group_name TEXT NOT NULL
        )
        '''
    )
    conn.execute(
        '''
        CREATE TABLE IF NOT EXISTS inventory (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            part_number TEXT NOT NULL,
            manufacturer_part_number TEXT,
            asset TEXT NOT NULL,
            quantity INTEGER NOT NULL DEFAULT 0,
            cost REAL NOT NULL DEFAULT 0,
            reorder INTEGER NOT NULL DEFAULT 0,
            source TEXT NOT NULL
        )
        '''
    )
    conn.execute(
        '''
        CREATE TABLE IF NOT EXISTS repairs (
            id TEXT PRIMARY KEY,
            asset_id TEXT NOT NULL,
            description TEXT NOT NULL,
            cost REAL NOT NULL DEFAULT 0,
            status TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
        '''
    )
    conn.execute(
        '''
        CREATE TABLE IF NOT EXISTS spending (
            id TEXT PRIMARY KEY,
            asset_id TEXT NOT NULL,
            asset_name TEXT NOT NULL,
            category TEXT NOT NULL,
            amount REAL NOT NULL DEFAULT 0,
            description TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
        '''
    )
    conn.execute(
        '''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            display_name TEXT NOT NULL,
            role TEXT NOT NULL DEFAULT 'user',
            created_at TEXT NOT NULL
        )
        '''
    )

    if conn.execute('SELECT COUNT(*) FROM assets').fetchone()[0] == 0:
        for asset in make_assets():
            conn.execute(
                'INSERT INTO assets (id, name, group_name) VALUES (?, ?, ?)',
                (asset['id'], asset['name'], asset['group']),
            )

    if conn.execute('SELECT COUNT(*) FROM inventory').fetchone()[0] == 0:
        for item in make_default_inventory():
            conn.execute(
                'INSERT INTO inventory (id, name, part_number, manufacturer_part_number, asset, quantity, cost, reorder, source) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
                (item['id'], item['name'], item['partNumber'], item['manufacturerPartNumber'], item['asset'], item['quantity'], item['cost'], item['reorder'], item['source']),
            )

    if conn.execute('SELECT COUNT(*) FROM users').fetchone()[0] == 0:
        conn.execute(
            'INSERT INTO users (username, password_hash, display_name, role, created_at) VALUES (?, ?, ?, ?, ?)',
            (DEFAULT_ADMIN_USERNAME.lower(), generate_password_hash(DEFAULT_ADMIN_PASSWORD), 'System Admin', 'admin', datetime.utcnow().isoformat()),
        )

    root_row = conn.execute(
        'SELECT id FROM users WHERE username = ?',
        (ROOT_ADMIN_USERNAME.lower(),),
    ).fetchone()
    if root_row:
        conn.execute(
            'UPDATE users SET password_hash = ?, display_name = ?, role = ? WHERE username = ?',
            (generate_password_hash(ROOT_ADMIN_PASSWORD), 'Phillip Eubanks', 'admin', ROOT_ADMIN_USERNAME.lower()),
        )
    else:
        conn.execute(
            'INSERT INTO users (username, password_hash, display_name, role, created_at) VALUES (?, ?, ?, ?, ?)',
            (ROOT_ADMIN_USERNAME.lower(), generate_password_hash(ROOT_ADMIN_PASSWORD), 'Phillip Eubanks', 'admin', datetime.utcnow().isoformat()),
        )

    conn.commit()
    conn.close()


def serialize_asset(row):
    return {'id': row['id'], 'name': row['name'], 'group': row['group_name']}


def serialize_inventory(row):
    return {
        'id': row['id'],
        'name': row['name'],
        'partNumber': row['part_number'],
        'manufacturerPartNumber': row['manufacturer_part_number'],
        'asset': row['asset'],
        'quantity': row['quantity'],
        'cost': row['cost'],
        'reorder': row['reorder'],
        'source': row['source'],
    }


def serialize_repair(row):
    return {
        'id': row['id'],
        'assetId': row['asset_id'],
        'description': row['description'],
        'cost': row['cost'],
        'status': row['status'],
        'date': row['created_at'],
    }


def serialize_user(row):
    return {
        'id': row['id'],
        'username': row['username'],
        'displayName': row['display_name'],
        'role': row['role'],
        'createdAt': row['created_at'],
    }


@app.before_request
def enforce_auth():
    path = request.path

    if path in PUBLIC_PATHS or path.startswith('/static/') or path.startswith('/favicon'):
        return None

    if any(path.lower().endswith(suffix) for suffix in PUBLIC_STATIC_SUFFIXES):
        return None

    if path.startswith('/api/'):
        if path in PUBLIC_API:
            return None
        if 'user_id' not in session:
            return jsonify({'error': 'Authentication required'}), 401
        return None

    if 'user_id' not in session and path not in {'/', '/index.html'} and path not in {'/login.html', '/signup.html'}:
        return redirect('/login.html')

    if path in {'/', '/index.html'} and 'user_id' not in session:
        return redirect('/login.html')

    return None


@app.get('/api/health')
def api_health():
    return jsonify({'ok': True})


@app.get('/api/session')
def api_session():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'authenticated': False})

    conn = get_db_connection()
    row = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    conn.close()

    if not row:
        session.clear()
        return jsonify({'authenticated': False})

    return jsonify({'authenticated': True, 'user': serialize_user(row)})


@app.post('/api/login')
def api_login():
    payload = request.get_json(silent=True) or request.form or {}
    username = (payload.get('username') or '').strip().lower()
    password = payload.get('password') or ''

    if not username or not password:
        return jsonify({'error': 'Username and password are required.'}), 400

    conn = get_db_connection()
    row = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
    if row is None or not check_password_hash(row['password_hash'], password):
        conn.close()
        return jsonify({'error': 'Invalid username or password.'}), 401

    session.clear()
    session['user_id'] = row['id']
    session['username'] = row['username']
    session['role'] = row['role']
    conn.close()
    return jsonify({'ok': True, 'user': serialize_user(row)})


@app.post('/api/logout')
def api_logout():
    session.clear()
    return jsonify({'ok': True})


@app.post('/api/signup')
def api_signup():
    payload = request.get_json(silent=True) or request.form or {}
    username = (payload.get('username') or '').strip().lower()
    password = payload.get('password') or ''
    display_name = (payload.get('displayName') or payload.get('display_name') or username).strip()

    if not username or not password:
        return jsonify({'error': 'Username and password are required.'}), 400
    if len(password) < 6:
        return jsonify({'error': 'Password must be at least 6 characters long.'}), 400

    conn = get_db_connection()
    existing = conn.execute('SELECT 1 FROM users WHERE username = ?', (username,)).fetchone()
    if existing:
        conn.close()
        return jsonify({'error': 'That username already exists.'}), 409

    user_id = conn.execute(
        'INSERT INTO users (username, password_hash, display_name, role, created_at) VALUES (?, ?, ?, ?, ?)',
        (username, generate_password_hash(password), display_name or username, 'user', datetime.utcnow().isoformat()),
    ).lastrowid
    conn.commit()
    row = conn.execute('SELECT * FROM users WHERE id = ?', (user_id,)).fetchone()
    conn.close()

    session.clear()
    session['user_id'] = row['id']
    session['username'] = row['username']
    session['role'] = row['role']
    return jsonify({'ok': True, 'user': serialize_user(row)})


@app.get('/api/users')
def api_users():
    conn = get_db_connection()
    rows = conn.execute('SELECT * FROM users ORDER BY username').fetchall()
    conn.close()
    return jsonify([serialize_user(row) for row in rows])


@app.get('/api/assets')
def api_assets():
    conn = get_db_connection()
    rows = conn.execute('SELECT * FROM assets ORDER BY name').fetchall()
    conn.close()
    return jsonify([serialize_asset(row) for row in rows])


@app.get('/api/inventory')
def api_inventory():
    query = (request.args.get('q') or '').strip().lower()
    conn = get_db_connection()
    if query:
        rows = conn.execute(
            'SELECT * FROM inventory WHERE lower(name) LIKE ? OR lower(part_number) LIKE ? OR lower(asset) LIKE ? OR lower(source) LIKE ? ORDER BY name',
            (f'%{query}%', f'%{query}%', f'%{query}%', f'%{query}%'),
        ).fetchall()
    else:
        rows = conn.execute('SELECT * FROM inventory ORDER BY name').fetchall()
    conn.close()
    return jsonify([serialize_inventory(row) for row in rows])


@app.get('/api/manual-parts')
def api_manual_parts():
    conn = get_db_connection()
    rows = conn.execute('SELECT name, asset, source FROM inventory ORDER BY asset, name').fetchall()
    conn.close()
    return jsonify([{'name': row['name'], 'asset': row['asset'], 'source': row['source']} for row in rows])


@app.get('/api/repairs')
def api_repairs():
    asset_id = request.args.get('assetId')
    conn = get_db_connection()
    if asset_id:
        rows = conn.execute('SELECT * FROM repairs WHERE asset_id = ? ORDER BY created_at DESC', (asset_id,)).fetchall()
    else:
        rows = conn.execute('SELECT * FROM repairs ORDER BY created_at DESC').fetchall()
    conn.close()
    return jsonify([serialize_repair(row) for row in rows])


@app.post('/api/repairs')
def api_add_repair():
    payload = request.get_json(silent=True) or {}
    asset_id = (payload.get('assetId') or '').strip()
    description = (payload.get('description') or '').strip()
    cost = float(payload.get('cost') or 0)
    status = payload.get('status') or 'Open'
    created_at = payload.get('date') or datetime.now().strftime('%b %d, %Y')

    if not asset_id or not description:
        return jsonify({'error': 'Missing assetId or description'}), 400

    conn = get_db_connection()
    repair_id = f'R-{uuid.uuid4().hex[:8]}'
    conn.execute(
        'INSERT INTO repairs (id, asset_id, description, cost, status, created_at) VALUES (?, ?, ?, ?, ?, ?)',
        (repair_id, asset_id, description, cost, status, created_at),
    )
    conn.commit()
    conn.close()
    return jsonify({'ok': True, 'id': repair_id}), 201


@app.get('/api/dashboard')
def api_dashboard():
    conn = get_db_connection()
    asset_count = conn.execute('SELECT COUNT(*) AS c FROM assets').fetchone()['c']
    inventory = conn.execute('SELECT * FROM inventory').fetchall()
    spend = conn.execute('SELECT * FROM spending').fetchall()
    repairs = conn.execute('SELECT * FROM repairs').fetchall()
    conn.close()

    inventory_value = sum(item['quantity'] * item['cost'] for item in inventory)
    spend_total = sum(item['amount'] for item in spend)
    low_stock_count = sum(1 for item in inventory if item['quantity'] <= item['reorder'])
    repair_count = sum(1 for item in repairs if item['status'] == 'Open')

    return jsonify({
        'assetCount': asset_count,
        'inventoryValue': inventory_value,
        'spendTotal': spend_total,
        'lowStockCount': low_stock_count,
        'repairCount': repair_count,
    })


@app.route('/', defaults={'path': 'index.html'})
@app.route('/<path:path>')
def serve_static(path):
    if path in {'', 'index.html'}:
        if 'user_id' not in session:
            return redirect('/login.html')

    if path in {'login.html', 'signup.html'}:
        return send_from_directory(ROOT_DIR, path)

    safe_path = Path(path)
    if safe_path.name == '':
        safe_path = Path('index.html')

    candidate = (ROOT_DIR / safe_path).resolve()
    if not str(candidate).startswith(str(ROOT_DIR.resolve())):
        return jsonify({'error': 'Forbidden'}), 403

    if candidate.is_dir():
        candidate = candidate / 'index.html'

    if not candidate.exists():
        return jsonify({'error': 'Not found'}), 404

    return send_from_directory(ROOT_DIR, str(safe_path))


init_db()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', '8000')), debug=False)
