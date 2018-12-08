import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    #SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or os.path.join(basedir, 'tree.db')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join('/home/vivek/Dev/RanchiMall/rmfzeTracking_testnet', 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False