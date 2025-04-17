from flask_app.extension import db


class Prayer(db.Model):
    __tablename__ = "prayers"


class PrayerResult(db.Model):
    __tablename__ = "prayer_results"
