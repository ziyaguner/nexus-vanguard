"""
Nexus Vanguard V7.0 Enterprise — Flask-SocketIO Backend
Auth: Flask-Login | DB: SQLAlchemy | WS: Threading mode
"""
import threading
import webbrowser
from functools import wraps

from flask import (Flask, jsonify, redirect, render_template,
                   request, url_for)
from flask_login import (LoginManager, UserMixin, current_user,
                         login_required, login_user, logout_user)
from flask_socketio import SocketIO, disconnect, emit

import scanner as sc
from database import PortRecord, ScanRecord, db, save_scan

# ── App ───────────────────────────────────────────────────────
app = Flask(__name__)
app.config["SECRET_KEY"]                  = "nv-v7-enterprise-2026-xK9#mP"
app.config["SQLALCHEMY_DATABASE_URI"]     = "sqlite:///nexus_vanguard.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

login_manager = LoginManager(app)
login_manager.login_view = "login"

socketio = SocketIO(app, cors_allowed_origins="*", async_mode="threading",
                    logger=False, engineio_logger=False)

# ── Single Admin User ─────────────────────────────────────────
ADMIN_USER = "admin"
ADMIN_PASS = "nexus2026"

class _User(UserMixin):
    id = "admin"

_admin = _User()

@login_manager.user_loader
def _load_user(uid):
    return _admin if uid == "admin" else None

# ── Active scan state ─────────────────────────────────────────
_stop_flags:   dict = {}   # sid -> [bool]
_scan_buffers: dict = {}   # sid -> {ip, start, end, ports[]}

# ── HTTP Routes ───────────────────────────────────────────────
@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    error = None
    if request.method == "POST":
        if (request.form.get("username") == ADMIN_USER and
                request.form.get("password") == ADMIN_PASS):
            login_user(_admin, remember=True)
            return redirect(url_for("index"))
        error = "Invalid credentials — try admin / nexus2026"
    return render_template("login.html", error=error)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

@app.route("/")
@login_required
def index():
    return render_template("index.html")

@app.route("/api/history")
@login_required
def api_history():
    rows = ScanRecord.query.order_by(ScanRecord.scanned_at.desc()).limit(100).all()
    return jsonify([r.to_dict() for r in rows])

@app.route("/api/history/<int:scan_id>/ports")
@login_required
def api_scan_ports(scan_id):
    ports = PortRecord.query.filter_by(scan_id=scan_id).all()
    return jsonify([p.to_dict() for p in ports])

# ── SocketIO Auth Decorator ───────────────────────────────────
def _ws_auth(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated:
            disconnect()
            return
        return f(*args, **kwargs)
    return wrapper

# ── SocketIO Events ───────────────────────────────────────────
@socketio.on("connect")
@_ws_auth
def on_connect():
    emit("server_ready", {"user": ADMIN_USER, "version": "7.0"})

@socketio.on("disconnect")
def on_disconnect():
    sid = request.sid
    flag = _stop_flags.pop(sid, None)
    if flag:
        flag[0] = True
    _scan_buffers.pop(sid, None)

@socketio.on("start_scan")
@_ws_auth
def on_start_scan(data):
    sid = request.sid
    flag = _stop_flags.get(sid)
    if flag:
        flag[0] = True

    ip      = str(data.get("ip", "")).strip()
    start   = max(1,     int(data.get("start",   1)))
    end     = min(65535, int(data.get("end",   1024)))
    threads = max(1, min(100, int(data.get("threads", 100))))

    if not ip:
        emit("scan_error", {"msg": "IP address is required"}); return
    if start > end:
        emit("scan_error", {"msg": "Invalid port range"}); return

    sf = [False]
    _stop_flags[sid]  = sf
    _scan_buffers[sid] = {"ip": ip, "start": start, "end": end, "ports": []}
    emit("scan_started", {"ip": ip, "total": end - start + 1})

    def on_progress(done, total, speed, elapsed):
        socketio.emit("scan_progress",
                      {"done": done, "total": total,
                       "speed": speed, "elapsed": elapsed}, to=sid)

    def on_port(result):
        _scan_buffers[sid]["ports"].append(result)
        socketio.emit("port_found", result, to=sid)

    def on_done(elapsed):
        buf = _scan_buffers.pop(sid, {})
        try:
            save_scan(app, ip, start, end, buf.get("ports", []), elapsed)
        except Exception as e:
            print(f"[DB ERR] {e}")
        socketio.emit("scan_done", {"elapsed": elapsed}, to=sid)
        _stop_flags.pop(sid, None)

    threading.Thread(
        target=sc.scan_range,
        args=(ip, start, end, threads, on_progress, on_port, on_done, sf),
        daemon=True,
    ).start()

@socketio.on("cancel_scan")
@_ws_auth
def on_cancel(data=None):
    sid = request.sid
    flag = _stop_flags.pop(sid, None)
    if flag:
        flag[0] = True
    _scan_buffers.pop(sid, None)
    emit("scan_cancelled", {})

# ── Entry Point ───────────────────────────────────────────────
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    threading.Timer(1.3, lambda: webbrowser.open("http://127.0.0.1:5001")).start()
    print("\n  [NEXUS VANGUARD V7.0 ENTERPRISE] -> http://127.0.0.1:5001\n")
    socketio.run(app, host="0.0.0.0", port=5001, debug=False,
                 allow_unsafe_werkzeug=True)
