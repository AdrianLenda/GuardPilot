# ADR 0001 – Tech Stack and Structure
**Status:** Accepted  
**Context:** Need a rapid, secure, on-prem proxy + dashboard with EU AI Act alignment.  
**Decision:** Python FastAPI backend; Streamlit UI; PostgreSQL; Parquet + SHA-256 hash chain; Caddy for TLS/OIDC; Dockerized.  
**Consequences:** Fast iteration with Python, strong ecosystem (spaCy, WeasyPrint). Streamlit allows quick UI without JS. Caddy simplifies TLS/OIDC.
