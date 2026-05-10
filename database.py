"""
Nexus Vanguard V7.0 — Database Models & CRUD
"""
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class ScanRecord(db.Model):
    __tablename__ = "scans"
    id            = db.Column(db.Integer, primary_key=True)
    target_ip     = db.Column(db.String(45), nullable=False)
    start_port    = db.Column(db.Integer, default=1)
    end_port      = db.Column(db.Integer, default=1024)
    open_count    = db.Column(db.Integer, default=0)
    critical_count= db.Column(db.Integer, default=0)
    high_count    = db.Column(db.Integer, default=0)
    elapsed       = db.Column(db.Float,   default=0.0)
    scanned_at    = db.Column(db.DateTime, default=datetime.utcnow)
    ports = db.relationship(
        "PortRecord", backref="scan", lazy=True,
        cascade="all, delete-orphan"
    )

    def to_dict(self):
        return {
            "id":             self.id,
            "target_ip":      self.target_ip,
            "start_port":     self.start_port,
            "end_port":       self.end_port,
            "open_count":     self.open_count,
            "critical_count": self.critical_count,
            "high_count":     self.high_count,
            "elapsed":        self.elapsed,
            "scanned_at":     self.scanned_at.strftime("%Y-%m-%d %H:%M:%S"),
        }


class PortRecord(db.Model):
    __tablename__ = "ports"
    id       = db.Column(db.Integer, primary_key=True)
    scan_id  = db.Column(db.Integer, db.ForeignKey("scans.id"), nullable=False)
    port     = db.Column(db.Integer)
    service  = db.Column(db.String(64))
    banner   = db.Column(db.String(256))
    risk     = db.Column(db.String(16))
    cve      = db.Column(db.String(32))
    cve_desc = db.Column(db.String(256))

    def to_dict(self):
        return {
            "port":     self.port,
            "service":  self.service,
            "banner":   self.banner,
            "risk":     self.risk,
            "cve":      self.cve,
            "cve_desc": self.cve_desc,
        }


def save_scan(app, ip, start_port, end_port, open_ports, elapsed):
    with app.app_context():
        crit = sum(1 for p in open_ports if p.get("risk") == "CRITICAL")
        high = sum(1 for p in open_ports if p.get("risk") == "HIGH")
        rec  = ScanRecord(
            target_ip=ip, start_port=start_port, end_port=end_port,
            open_count=len(open_ports), critical_count=crit,
            high_count=high, elapsed=elapsed,
        )
        db.session.add(rec)
        db.session.flush()
        for p in open_ports:
            db.session.add(PortRecord(
                scan_id=rec.id, port=p["port"],
                service=p.get("service",""), banner=p.get("banner",""),
                risk=p.get("risk","LOW"), cve=p.get("cve"),
                cve_desc=p.get("cve_desc"),
            ))
        db.session.commit()
        return rec.id
