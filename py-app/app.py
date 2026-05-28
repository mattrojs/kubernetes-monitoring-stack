from flask import Flask, request
from prometheus_client import Counter, Histogram, start_http_server
import time

app = Flask(__name__)

# Métricas
request_count = Counter('http_requests_total', 'Total HTTP requests', ['method', 'endpoint'])
request_duration = Histogram('http_request_duration_seconds', 'HTTP request duration', buckets=(0.1, 0.5, 1.0, 2.0))

@app.before_request
def before_request():
    request.start_time = time.time()

@app.after_request
def after_request(response):
    duration = time.time() - request.start_time
    request_duration.observe(duration)
    request_count.labels(method='GET', endpoint='test').inc()
    return response

@app.route('/')
def hello():
    return 'Hello World', 200

@app.route('/health')
def health():
    return {'status': 'healthy'}, 200

if __name__ == '__main__':
    start_http_server(8000)
    app.run(host='0.0.0.0', port=5001)