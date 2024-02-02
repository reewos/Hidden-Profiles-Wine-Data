### 1. Compose image and execute in background
```
docker compose up --build -d
```
or
```
docker pull reewos/hidden-profiles-wine-data-server
docker run -d -p 8000:8000 --name hidden-profiles-wine-data-server-1 reewos/hidden-profiles-wine-data-server:latest
```
### 2. Run with terminal
```
docker exec -it hidden-profiles-wine-data-server-1 /bin/sh
```
### 3. Inside terminal, execute
```
python main.py
```

### 4. Results paths

* Path model: "/app/models/voting_model.pkl"
* Path results: "/app/datasets/results.csv"
