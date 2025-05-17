# Cell Tower Visualization Service

<div style="display: flex; justify-content: space-between;">
  <img src="screenshots/heatmap-visualization.png" alt="Heatmap" style="width: 48%;"/>
  <img src="screenshots/triangulation.png" alt="Triangulation" style="width: 48%;"/>
</div>

A  visualization service for cell tower data with heatmap and triangulation capabilities.

## Features
| Feature |
|---------|
| 📡 **Interactive Visualization**  |
| 🔥 **Heatmap Generation** |
| 📐 **Tower Triangulation** |

## Tech Stack

### Frontend
- Vue.js 3

### Backend
- FastAPI (Python)
- C++/CGAL (Heavy computations)
- PostgreSQL
- gRPC

## Deploy 
```
cd docker
docker-compose up
```
