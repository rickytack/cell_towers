import L from 'leaflet'
import "leaflet.heat"
import axios from 'axios'

import {
  TILE_LAYER_URL,
  INITIAL_VIEW,
  RADIO_TYPE_COLORS
} from './config'


export class MapManager {
  constructor(mapElement) {
    if (!mapElement) {
      throw new Error('Map container element is required')
    }

    try {
      this.map = L.map(mapElement, {
        attributionControl: false,
        preferCanvas: true
      }).setView(INITIAL_VIEW.center, INITIAL_VIEW.zoom)

      this.markers = []
      this.points = []
      this.triangles = []
      this.heatmap = null

      this.initBaseLayer()
      this.initHeatmapLayer()
    } catch (error) {
      console.error('Error initializing MapManager:', error)
      throw error
    }
  }

  getRadioColor = (radioType) => {
    return RADIO_TYPE_COLORS[radioType] || RADIO_TYPE_COLORS.default || '#3388ff'
  }

  createMarker = (tower) => {
    if (!tower) {
      console.error('Invalid parameters for createMarker')
      return null
    }

    try {
      const marker = L.circleMarker([tower.lat, tower.lon], {
        radius: 4,
        fillColor: this.getRadioColor(tower.radio),
        color: '#fff',
        weight: 2,
        fillOpacity: 0.8
      }).bindPopup(`
        <b>Cell Tower #${tower.id || 'N/A'}</b><br>
        Type: <div style="color:${this.getRadioColor(tower.radio)}">${tower.radio || 'Unknown'}</div>
        Created: <div>${tower.created || 'Unknown'}</div>
        Updated: <div>${tower.updated || 'Unknown'}</div>
      `).addTo(this.map)

      marker.towerData = tower
      return marker
    } catch (error) {
      console.error('Error creating marker:', error)
      return null
    }
  }

  initBaseLayer() {
    try {
      L.tileLayer(TILE_LAYER_URL, {
        maxZoom: 19,
        subdomains: ['a', 'b', 'c'],
        detectRetina: true
      }).addTo(this.map)

      L.control.attribution({
        prefix: false
      }).addAttribution(
        '© <a href="https://osm.org/copyright" target="_blank" rel="noopener">OpenStreetMap</a>'
      ).addTo(this.map)
    } catch (error) {
      console.error('Error initializing base layer:', error)
    }
  }

  getTowerWeight(radio_type) {
    if (!radio_type) return 0

    switch (radio_type.toUpperCase()) {
      case "GSM":
        return 0.4
      case "CDMA":
        return 0.6
      case "UMTS":
        return 0.7
      case "WCDMA":
        return 0.8
      case "LTE":
      case "NR":
        return 1
      default:
        return 0.2
    }
  }

  async loadTowers(apiUrl) {
  if (!apiUrl) {
    console.error('API URL is required');
    return;
  }

  this.clearMarkers();
  const bounds = this.map.getBounds();

  try {
    const params = {
      bottom_left_lat: bounds.getSouth(),
      bottom_left_lon: bounds.getWest(),
      top_right_lat: bounds.getNorth(),
      top_right_lon: bounds.getEast()
    };

    const response = await axios.get(`${apiUrl}/towers/area`, { params });

    if (!response.data?.towers) {
      console.error('Invalid towers data format');
      return;
    }

    this.markers = response.data.towers
      .map(tower => this.createMarker(tower))
      .filter(marker => marker !== null);

    // Update points array
    this.points = this.markers.map(marker => {
      const markerLatLng = marker.getLatLng();
      return [
        markerLatLng.lat,
        markerLatLng.lng,
        this.getTowerWeight(marker.towerData.radio)
      ];
    });

    // Only update heatmap if it's currently visible
    if (this.heatmap && this.map.hasLayer(this.heatmap)) {
      this.heatmap.setLatLngs(this.points);
    }
    } catch (error) {
      console.error('Error loading towers:', error);
      throw error;
    }
  }

  async loadTriangles(apiUrl) {
    if (!apiUrl) {
      console.error('API URL is required');
      return;
    }

  try {
    // Clear existing triangles
    this.clearTriangles();

    // Get current map bounds
    const bounds = this.map.getBounds();
    const params = {
      bottom_left_lat: bounds.getSouth(),
      bottom_left_lon: bounds.getWest(),
      top_right_lat: bounds.getNorth(),
      top_right_lon: bounds.getEast()
    };

    // Make API request
    const response = await axios.get(`${apiUrl}/towers/triangles`, { params });
    const trianglesData = response.data?.triangles;

    if (!trianglesData || !Array.isArray(trianglesData)) {
      console.error('Invalid triangles data format');
      return;
    }

    // Draw new triangles
    this.triangles = trianglesData.map(triangle => {
      try {
        // Convert points to LatLng format
        const latLngs = triangle.points.map(point =>
          L.latLng(point.lat, point.lon)
        );

        // Create and style the triangle polygon
        const polygon = L.polygon(latLngs, {
          color: '#3388ff',
          weight: 1,
          opacity: 0.7,
          fillColor: '#3388ff',
          fillOpacity: 0.2
        }).addTo(this.map);


        return polygon;
      } catch (error) {
        console.error('Error creating triangle:', error);
        return null;
      }
    }).filter(triangle => triangle !== null);

  } catch (error) {
    console.error('Error loading triangles:', error);
    throw error;
  }
}

clearTriangles() {
  this.triangles.forEach(triangle => {
    try {
      if (triangle && this.map.hasLayer(triangle)) {
        this.map.removeLayer(triangle);
      }
    } catch (error) {
      console.error('Error removing triangle:', error);
    }
  });
  this.triangles = [];
}

  clearMarkers() {
    this.markers.forEach(marker => {
      try {
        if (marker && this.map.hasLayer(marker)) {
          this.map.removeLayer(marker)
        }
      } catch (error) {
        console.error('Error removing marker:', error)
      }
    })
    this.markers = []
  }

  initHeatmapLayer() {
    try {
      this.heatmap = L.heatLayer([], {
        radius: 15,
        blur: 30,
        maxZoom: INITIAL_VIEW.zoom,
        gradient: {
          0.4: 'blue',
          0.6: 'cyan',
          0.7: 'lime',
          0.8: 'yellow',
          1.0: 'red'
        }
      }).addTo(this.map)
    } catch (error) {
      console.error('Error initializing heatmap layer:', error)
    }
  }

  toggleHeatmapLayer(visible) {
  if (!this.heatmap) return;

  try {
    if (visible) {
      if (!this.map.hasLayer(this.heatmap)) {
        this.map.addLayer(this.heatmap);
      }
      // Update data if we have points
      if (this.points.length > 0) {
        this.heatmap.setLatLngs(this.points);
      }
    } else {
      if (this.map.hasLayer(this.heatmap)) {
        this.map.removeLayer(this.heatmap);
      }
    }
  } catch (error) {
    console.error('Error toggling heatmap layer:', error);
  }
}

}