let map;
let linePolylines = {};
let routePolyline = null;
let stationMarkers = {};

const lineColors = {
  'Western': '#10b981',
  'Central': '#f59e0b',
  'Harbour': '#06b6d4'
};

function initMap(graph) {
  // Center map in Mumbai
  map = L.map('map-container', {
    zoomControl: true,
    maxBounds: [
      [18.85, 72.7],
      [19.55, 73.2]
    ]
  }).setView([19.0760, 72.8777], 11);

  // Sleek dark-mode tile layer
  L.tileLayer('https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png', {
    attribution: '&copy; CartoDB',
    maxZoom: 18,
    minZoom: 10
  }).addTo(map);

  // Define custom icons using SVGs
  const stationIcon = L.icon({
    iconUrl: '/assets/icons/station_marker.svg',
    iconSize: [16, 16],
    iconAnchor: [8, 8],
    popupAnchor: [0, -8]
  });

  const coords = graph.coordinates;

  // Draw Polylines for each line
  const lines = ['Western', 'Central', 'Harbour'];
  lines.forEach(async (line) => {
    try {
      const resp = await fetch(`/railway-data/${line.toLowerCase()}_line.json`);
      const stations = await resp.json();
      
      const points = [];
      stations.forEach((s) => {
        const latlng = coords[s.name];
        if (latlng) {
          points.push(latlng);
          
          // Create marker if it doesn't already exist
          if (!stationMarkers[s.name]) {
            const marker = L.marker(latlng, { icon: stationIcon })
              .addTo(map)
              .bindTooltip(s.name, {
                permanent: false,
                direction: 'top',
                className: 'leaflet-tooltip-dark'
              });
              
            marker.on('click', () => {
              handleStationClick(s.name);
            });
            
            stationMarkers[s.name] = marker;
          }
        }
      });
      
      const polyline = L.polyline(points, {
        color: lineColors[line],
        weight: 4,
        opacity: 0.7,
        lineJoin: 'round'
      }).addTo(map);
      
      linePolylines[line] = polyline;
    } catch (e) {
      console.error(`Failed to draw polyline for line ${line}:`, e);
    }
  });
}

function handleStationClick(stationName) {
  // Dispatched to ui.js handler
  if (window.onMapStationSelect) {
    window.onMapStationSelect(stationName);
  }
}

function updateMapMarkers(source, destination, routePath) {
  const sourceIcon = L.icon({
    iconUrl: '/assets/icons/source_marker.svg',
    iconSize: [28, 28],
    iconAnchor: [14, 14]
  });

  const destIcon = L.icon({
    iconUrl: '/assets/icons/dest_marker.svg',
    iconSize: [28, 28],
    iconAnchor: [14, 14]
  });

  const stationIcon = L.icon({
    iconUrl: '/assets/icons/station_marker.svg',
    iconSize: [16, 16],
    iconAnchor: [8, 8]
  });

  // Reset all markers to standard
  for (const [name, marker] of Object.entries(stationMarkers)) {
    marker.setIcon(stationIcon);
  }

  // Update selected source and destination icons
  if (source && stationMarkers[source]) {
    stationMarkers[source].setIcon(sourceIcon);
  }
  if (destination && stationMarkers[destination]) {
    stationMarkers[destination].setIcon(destIcon);
  }

  // Draw or remove route polyline
  if (routePolyline) {
    map.removeLayer(routePolyline);
    routePolyline = null;
  }

  if (routePath && routePath.length > 1) {
    const coords = routePath.map(name => window.railwayGraph.coordinates[name]).filter(Boolean);
    
    routePolyline = L.polyline(coords, {
      color: '#60a5fa', // Bright blue route highlighting
      weight: 6,
      opacity: 0.9,
      dashArray: '8, 8',
      lineCap: 'round',
      lineJoin: 'round'
    }).addTo(map);

    // Zoom map to fit the route bounds
    const bounds = L.latLngBounds(coords);
    map.fitBounds(bounds, { padding: [50, 50] });
  }
}
