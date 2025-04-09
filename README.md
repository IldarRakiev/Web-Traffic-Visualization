# Web Traffic Globe Visualization

Interactive 3D visualization of global web traffic using Three.js, Flask, and Docker.

## Features
- 3D globe with realistic Earth texture
- Visualize traffic sources by geographic location
- Color-coded points (green=normal, red=suspicious)
- Real-time statistics dashboard
- Interactive controls (rotation, zoom, filters)

## Quick Start

### Prerequisites
- Docker
- Docker Compose

### Installation & Run

1. Clone the repository:
```bash
git clone https://github.com/your-username/your-repo.git
cd your-repo
```

2. Start the system:
```bash
docker-compose up
```

3. Access the visualization:
   - Open `http://localhost:5000` in your browser
   - The sender will automatically begin transmitting data

## Project Structure
```
.
├── server.py            # Flask backend
├── sender.py            # Data sender script
├── static/
│   └── index.html       # Three.js visualization
├── ip_addresses.csv     # Sample traffic data
├── requirements.txt     # Python dependencies
└── docker-compose.yml   # Container configuration
```

## Key Commands

| Command | Description |
|---------|-------------|
| `docker-compose up` | Start all services |
| `docker-compose up --build` | Rebuild and start |
| `docker-compose down` | Stop all containers |

## Customization
- To use your own data: replace `ip_addresses.csv`
- Adjust visualization parameters in `static/index.html`:
  - `maxPointLifetime` - how long points remain visible
  - `rotationSpeed` - globe auto-rotation speed
  - Color codes in `addPoint()` function

## Troubleshooting
- If ports are busy: change `5000:5000` in docker-compose.yml
- No data showing? Check sender logs: `docker-compose logs sender`
- Browser caching issues? Hard refresh (Ctrl+F5)
