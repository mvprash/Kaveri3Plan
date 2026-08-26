# -*- coding: utf-8 -*-
from pypdf import PdfReader
from pathlib import Path

path = Path(r"E:\Prashanth\Official\Kaveri 3.0\Kaveri3Plan\Books\Building Microservices Designing Fine-Grained Systems 2nd By Sam Newman.pdf")
r = PdfReader(str(path))
print("pages", len(r.pages))

# Find chapter headings
for i, p in enumerate(r.pages):
    t = p.extract_text() or ""
    lines = [ln.strip() for ln in t.splitlines() if ln.strip()]
    if not lines:
        continue
    joined = " | ".join(lines[:4])
    if lines[0].startswith("Chapter ") or (len(lines) > 1 and lines[0].startswith("Part ")):
        print(f"{i+1}: {joined[:140]}")

keywords = [
    "API gateway", "service mesh", "Kubernetes", "Kafka", "gRPC", "OpenAPI",
    "Prometheus", "Jaeger", "Vault", "Istio", "Kong", "circuit breaker", "Pact",
    "Docker", "GraphQL", "Backend for Frontend", "BFF", "saga", "Camunda",
    "Redis", "Consul", "Nginx", "Envoy", "OpenTelemetry", "Zipkin", "mTLS",
    "OAuth", "JWT", "RabbitMQ", "SQS", "schema registry", "Swagger",
    "service discovery", "load balancer", "CDN", "Terraform", "Helm", "FaaS",
    "Lambda", "Chaos", "Hystrix", "Resilience4j", "Fluentd", "Elasticsearch",
    "Grafana", "SPIFFE", "message broker", "consumer-driven", "sidecar",
    "mutual TLS", "DNS", "etcd", "ZooKeeper", "ActiveMQ", "NATS", "Avro",
    "Protocol Buffers", "protobuf", "GraphQL", "Apollo", "Zuul", "Ambassador",
    "Traefik", "Linkerd", "AWS API Gateway", "Azure API Management",
    "Cloudflare", "NGINX", "HAProxy", "Jenkins", "GitHub Actions", "CircleCI",
    "Spinnaker", "Argo", "Nomad", "OpenShift", "Cloud Foundry", "Knative",
    "Serverless", "S3", "object store", "CDC", "Debezium", "Outbox",
    "distributed tracing", "correlation ID", "log aggregation", "ELK",
    "Splunk", "New Relic", "Datadog", "Honeycomb", "Lightstep",
    "JSON Web Token", "OpenID Connect", "OIDC", "SAML", "API keys",
    "rate limiting", "bulkhead", "timeout", "retry", "idempotency",
    "Swagger", "RAML", "AsyncAPI", "GraphQL Federation",
]

hits = {}
for i, p in enumerate(r.pages):
    t = (p.extract_text() or "").lower()
    for k in keywords:
        if k.lower() in t:
            hits.setdefault(k, []).append(i + 1)

print("\n=== TOOL HITS ===")
for k in sorted(hits, key=lambda x: (hits[x][0], x)):
    pages = hits[k]
    shown = pages[:20]
    extra = f" (+{len(pages)-20} more)" if len(pages) > 20 else ""
    print(f"{k}: {shown}{extra}")
