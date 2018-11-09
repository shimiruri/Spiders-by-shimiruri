from flask import Flask, g
from proxies_storage import RedisClient


__all__ = ['app']
app = Flask(__name__)


def get_conn():
    g.redis = RedisClient()
    return g.redis


@app.route('/')
def homepage():
    return '<h2>Welcome to Proxy Pool System</h2>'


@app.route('/random')
def get_proxy():
    """
    Get proxy random.
    :return: Proxy of random
    """
    conn = get_conn()
    return conn.random()


@app.route('/count')
def get_counts():
    """
    Get all proxies count number.
    :return: Proxies pool count.
    """
    conn = get_conn()
    return str(conn.count())


if __name__ == '__main__':
    app.run()
