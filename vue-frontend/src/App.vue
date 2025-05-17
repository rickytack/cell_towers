<script setup>
import {ref} from 'vue'
import OsmMap from './components/OsmMap.vue'
</script>

<template>
  <div class="app">
    <h1>Cell towers</h1>
    <div class="map-container">
      <OsmMap apiUrl="/api/v1"/>
    </div>
  </div>
</template>

<style>
.app {
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
  position: relative; /* Establish stacking context */
}

</style>