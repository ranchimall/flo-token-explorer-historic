from app import db

class Transactions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(64), index=True)
    parentid = db.Column(db.Integer, index=True)
    transferBalance = db.Column(db.Integer)

    def __repr__(self):
        return '<User {}>'.format(self.address)

class Transferlogs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    primaryIDReference = db.Column(db.Integer)
    transferDescription = db.Column(db.String, index=True)
    transferIDConsumed = db.Column(db.String, index=True)
    blockchainReference = db.Column(db.String)

    def __repr__(self):
        return '<User {}>'.format(self.primaryIDReference)

class Webtable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    transferDescription = db.Column(db.String, index=True)
    blockchainReference = db.Column(db.String, index=True, unique=True)

    def __repr__(self):
        return '<User {}>'.format(self.transferDescription)