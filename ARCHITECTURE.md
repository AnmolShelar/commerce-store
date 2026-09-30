# Assignment 2 Architecture

```mermaid
flowchart LR
    Dev["Developer"] -->|push code| Repo["GitHub repository"]
    Repo -->|starts workflow| Actions["GitHub Actions<br/>Ubuntu runner"]

    Actions -->|build, start, check| Compose["Docker Compose"]

    subgraph Services["Docker Compose services"]
        Store["Nginx storefront<br/>:8080"]
        Trainer["Model training job"]
        MLflow["MLflow tracking and model registry<br/>:5000"]
        API["Flask prediction API<br/>:8000"]
        Prom["Prometheus<br/>:9090"]
        Grafana["Grafana dashboard<br/>:3000"]
        Data[("MLflow data and model artifacts")]

        Trainer -->|logs experiment and registers model| MLflow
        MLflow <--> Data
        API -->|loads registered model| MLflow
        Prom -->|scrapes /metrics| API
        Grafana -->|queries metrics| Prom
    end

    Compose --> Store
    Compose --> Trainer
    Compose --> MLflow
    Compose --> API
    Compose --> Prom
    Compose --> Grafana

    Actions -->|checks storefront, model, prediction, metrics, dashboard| Store
    Actions -->|checks storefront, model, prediction, metrics, dashboard| API
    Actions -->|checks experiment| MLflow
    Actions -->|checks monitoring| Prom
    Actions -->|checks dashboard| Grafana
