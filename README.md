# GraphHopper Docker 🗺️

Lightweight, production-ready Docker image for **[GraphHopper Routing Engine 11.0](https://github.com/graphhopper/graphhopper)** based on **Eclipse Temurin Java 21** and **Alpine Linux**.

## 🚀 Features
- 🪶 **Ultra-lightweight:** Alpine-based image (~160 MB).
- ☕ **Java 21 LTS:** High-performance G1GC & String Deduplication tuned for fast memory reclamation.
- 📦 **Multi-Architecture:** Automated GitHub Actions CI built directly for `ghcr.io`.
- ☸️ **Kubernetes & HA Ready:** Compatible with Kubernetes Persistent Volumes (Longhorn).

## 🛠️ Usage

```bash
docker run -d -p 8989:8989 \
  -v /path/to/cache:/graphhopper/cache \
  ghcr.io/morta5/graphhopper-docker:latest
```
