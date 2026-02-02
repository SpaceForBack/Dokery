from flask import Flask, jsonify
import redis
import time
import os

app = Flask(__name__)

redis_host = os.environ.get('REDIS_HOST', 'redis')
cache = redis.Redis(host=redis_host, port=6379)

def get_hit_count():
    retries = 5
    while True:
        try:
            return cache.incr('hits')
        except redis.exceptions.ConnectionError as exc:
            if retries == 0:
                raise exc
            retries -= 1
            time.sleep(0.5)

@app.route('/')
def home():
    try:
        count = get_hit_count()
    except redis.exceptions.ConnectionError:
        count = "Błąd połączenia z bazą"
        
    return jsonify({
        "message": "Przy programowaniu nie ucierpaiło żadne zwierzę",
        "visits": count,
        "status": "success"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)