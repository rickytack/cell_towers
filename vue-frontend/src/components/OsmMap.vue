<script setup>
import { onMounted, ref } from 'vue'
import { MapManager } from './map/manager'
import { debounce } from 'lodash-es' // or implement a simple debounce

const props = defineProps({
  apiUrl: {
    type: String,
    required: true
  }
})

const mapElement = ref(null)
const loading = ref(false)
const heatmapVisible = ref(false)
const trianglesVisible = ref(false)
let mapManager

// Debounced load function to prevent rapid successive calls
const loadMapData = debounce(async () => {
  if (!mapManager) return

  try {
    loading.value = true
    await Promise.all([
      trianglesVisible.value ? mapManager.loadTriangles(props.apiUrl) : Promise.resolve(),
      mapManager.loadTowers(props.apiUrl)
    ])
  } catch (error) {
    console.error('Error loading map data:', error)
  } finally {
    loading.value = false
  }
}, 300)

onMounted(async () => {
  try {
    loading.value = true
    mapManager = new MapManager(mapElement.value)

    // Set up event listeners
    mapManager.map.on('moveend zoomend', loadMapData)

    // Initial load with heatmap hidden
    mapManager.toggleHeatmapLayer(false)
    await loadMapData()
  } catch (error) {
    console.error('Error initializing map:', error)
  } finally {
    loading.value = false
  }
})

const toggleHeatmap = () => {
  heatmapVisible.value = !heatmapVisible.value
  mapManager?.toggleHeatmapLayer(heatmapVisible.value)
}


const toggleTriangles = async () => {
  trianglesVisible.value = !trianglesVisible.value

  if (trianglesVisible.value) {
    // Show triangles
    loading.value = true
    try {
      await mapManager.loadTriangles(props.apiUrl)
    } catch (error) {
      console.error('Error loading triangles:', error)
      trianglesVisible.value = false
    } finally {
      loading.value = false
    }
  } else {
    // Hide triangles
    mapManager.clearTriangles()
  }
}

</script>

<template>
  <div class="map-container">
    <div v-if="loading" class="loading">
      <div class="loading-spinner"></div>
      Loading map data...
    </div>
    <div ref="mapElement" class="map"></div>

    <!-- Heatmap Toggle Button -->
    <div class="map-controls">
      <button
        @click="toggleHeatmap"
        :class="{ active: heatmapVisible }"
        class="layer-toggle"
        title="Toggle heatmap visibility"
        :disabled="loading"
      >
        🔥 Heatmap
      </button>
      <button
        @click="toggleTriangles"
        :class="{ active: trianglesVisible }"
        class="layer-toggle"
        title="Toggle triangles visibility"
        :disabled="loading"
      >
        🔺 Triangles
      </button>
    </div>
  </div>
</template>

<style scoped>
.map-container {
  height: 80vh;
  width: 100%;
  position: relative;
}

.map {
  height: 100%;
  width: 100%;
}

.loading {
  position: absolute;
  top: 10px;
  left: 50%;
  transform: translateX(-50%);
  background: rgba(0, 0, 0, 0.7);
  color: white;
  padding: 8px 16px;
  border-radius: 4px;
  z-index: 1001;
  display: flex;
  align-items: center;
  gap: 8px;
}

.loading-spinner {
  width: 16px;
  height: 16px;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  border-top-color: white;
  animation: spin 1s ease-in-out infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.map-controls {
  position: absolute;
  top: 10px;
  right: 10px;
  z-index: 1000;
  display: flex;
  gap: 8px;
}

.layer-toggle {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 6px 12px;
  background: white;
  border: 1px solid #ddd;
  border-radius: 4px;
  cursor: pointer;
  box-shadow: 0 1px 5px rgba(0, 0, 0, 0.2);
  transition: all 0.2s ease;
}

.layer-toggle:hover:not(:disabled) {
  background: #f5f5f5;
}

.layer-toggle.active {
  background: #e3f2fd;
  border-color: #90caf9;
  color: #1976d2;
}

.layer-toggle:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
</style>