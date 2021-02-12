#DATABASE_URL = 'postgres://ggqoskolpxtanp:13a0257a5f12b9d5dd0d57c1d993ff7b27e7c774746ce1661aa90f3082a17aaf@ec2-3-211-245-154.compute-1.amazonaws.com:5432/d516q9uaepdk5u'

...
# Database initialization
if os.environ.get('DATABASE_URL') is None:
    basedir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
else:
    SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
