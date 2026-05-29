
# Local Kubernetes Monitoring Stack

A complete monitoring solution deployed on Minikube using Prometheus for metrics collection and Grafana for visualization.

## Project Overview

This project demonstrates a production-like monitoring setup on local Kubernetes, featuring:
- **Prometheus**: Metrics collection and storage
- **Grafana**: Real-time visualization and dashboarding
- **Custom Flask App**: Application exposing Prometheus metrics

## Architecture
┌─────────────────────────────────────────┐
│        Minikube (Local K8s)             │
├─────────────────────────────────────────┤
│                                         │
│  ┌──────────┐  ┌──────────┐            │
│  │ Flask    │  │Prometheus│            │
│  │ App      │  │          │            │
│  │:5001     │  │:9090     │            │
│  └──────────┘  └──────────┘            │
│       │              ▲                  │
│       └──────────────┘                  │
│       (scrapes /metrics)                │
│                                         │
│  ┌──────────────────┐                   │
│  │    Grafana       │                   │
│  │    :3000         │                   │
│  │ (reads from      │                   │
│  │  Prometheus)     │                   │
│  └──────────────────┘                   │
│                                         │
└─────────────────────────────────────────┘

## Project Structure
kubertest/
├── README.md
├── app-py/
│   ├── app.py                 # Flask application
│   ├── requirements.txt       # Python dependencies
│   └── Dockerfile            # Container image definition
└── k8s/
├── namespace.yaml
├── prometheus-config.yaml
├── prometheus-deployment.yaml
├── prometheus-service.yaml
├── grafana-deployment.yaml
├── grafana-service.yaml
├── mi-app-deployment.yaml
└── mi-app-service.yaml

## Prerequisites

- Docker installed
- Minikube installed
- kubectl installed
- ~4GB RAM available

## Installation & Setup

### 1. Start Minikube

```bash
minikube start
minikube status
```

### 2. Build Application Image

```bash
cd ~/kubertest/app-py
docker build --no-cache -t app-py:latest .
minikube image load app-py:latest
```

### 3. Deploy to Kubernetes

```bash
cd ~/kubertest/k8s
kubectl apply -f .
```

Verify all pods are running:

```bash
kubectl get pods -n appmonitoring
```

Expected output:
NAME                         READY   STATUS    RESTARTS   AGE
prometheus-7565956c4c-66wsn  1/1     Running   0          2m
grafana-5f8c7d9f9c-k8x9p     1/1     Running   0          2m
mi-app-6cc87d6ddd-ds97b      1/1     Running   0          2m

## Accessing the Services

### Prometheus

```bash
kubectl port-forward -n appmonitoring svc/prometheus 9090:9090
```

Access: `http://localhost:9090`

### Grafana

```bash
kubectl port-forward -n appmonitoring svc/grafana 3000:3000
```

Access: `http://localhost:3000`
- Username: `admin`
- Password: `admin`

### Application

```bash
kubectl port-forward -n appmonitoring svc/mi-app 5001:5001
```

Access: `http://localhost:5001`

## Dashboards

### 1. HTTP Requests Dashboard

Monitors HTTP traffic metrics:
- **Total Requests**: Cumulative count of all HTTP requests
- **Requests per Second**: Rate of incoming requests (RPS)
- **HTTP Latency**: Average request response time

### 2. Resources Dashboard

Monitors application resource consumption:
- **CPU Usage**: CPU time consumed over time
- **Memory Usage**: Memory used by the application

## Metrics Exposed

The custom Flask application exposes the following metrics:

| Metric | Type | Description |
|--------|------|-------------|
| `http_requests_total` | Counter | Total number of HTTP requests |
| `http_request_duration_seconds` | Histogram | Request duration buckets and statistics |
| `process_cpu_seconds_total` | Counter | CPU seconds consumed |
| `process_resident_memory_bytes` | Gauge | Memory used in bytes |

## Generating Test Data

Generate traffic to populate metrics:

```bash
# Generate 100 requests with 0.1s delay between them
for i in {1..100}; do curl http://localhost:5001/; sleep 0.1; done
```

Or for larger load:

```bash
# Generate 10,000 requests
for i in {1..10000}; do curl http://localhost:5001/ & done
```

## How It Works

1. **Flask App**: Runs in a pod and serves traffic on port 5001
2. **Prometheus Client**: Exposes metrics on `/metrics` endpoint (port 8000)
3. **Prometheus Server**: Scrapes `/metrics` every 15 seconds (configurable in `prometheus-config.yaml`)
4. **Grafana**: Queries Prometheus and visualizes data in real-time

### Metric Collection Flow
Flask App (5001)
↓
Prometheus (9090) scrapes /metrics every 15s
↓
Stores in TSDB (Time Series Database)
↓
Grafana (3000) queries Prometheus
↓
Displays in Dashboards

## Useful Commands

```bash
# View all pods
kubectl get pods -n appmonitoring

# View pod logs
kubectl logs -n appmonitoring -l app=app-py

# Check Prometheus targets
kubectl port-forward -n appmonitoring svc/prometheus 9090:9090
# Visit http://localhost:9090/targets

# Delete deployment
kubectl delete deployment mi-app -n appmonitoring

# Restart a pod
kubectl delete pod <pod-name> -n appmonitoring

# Stop Minikube
minikube stop

# Delete Minikube cluster
minikube delete
```

## Troubleshooting

### Pod stuck in ErrImageNeverPull
```bash
# Ensure image is loaded in Minikube
minikube image ls | grep app-py

# If not present, load it
minikube image load app-py:latest
```

### No data in Grafana
1. Verify Prometheus is scraping your app: `http://localhost:9090/targets`
2. Check that requests are being sent to the app
3. Allow 1-2 minutes for initial data collection

### Port-forward not working
- Ensure you have multiple terminal windows open
- Each `kubectl port-forward` command blocks the terminal

## Next Steps

- Add alerting rules to Prometheus
- Create additional dashboards for business metrics
- Deploy to a real Kubernetes cluster
- Implement auto-scaling based on metrics

## Portfolio Items

Working Kubernetes cluster (Minikube)
Custom application with Prometheus metrics
Complete monitoring stack (Prometheus + Grafana)
Professional dashboards showing real-time metrics
Infrastructure as Code (YAML manifests)
Documentation and setup guides

## Author

Created as a demonstration of my skills for Monitoring and Observability, also to validate my Kubernetes and Docker habilities

## References

- [Prometheus Documentation](https://prometheus.io/docs/)
- [Grafana Documentation](https://grafana.com/docs/)
- [Kubernetes Best Practices](https://kubernetes.io/docs/concepts/configuration/overview/)
