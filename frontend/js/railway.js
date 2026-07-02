class RailwayClientGraph {
  constructor() {
    this.graph = {}; // node -> [ { node, weight, line } ]
    this.coordinates = {};
    this.stations = new Set();
  }

  async initialize() {
    try {
      // 1. Fetch Coordinates
      const coordResp = await fetch('/railway-data/station_coordinates.json');
      this.coordinates = await coordResp.json();

      // 2. Fetch Line Files
      const lines = {
        'Western': '/railway-data/western_line.json',
        'Central': '/railway-data/central_line.json',
        'Harbour': '/railway-data/harbour_line.json'
      };

      for (const [lineName, url] of Object.entries(lines)) {
        const resp = await fetch(url);
        const stationsList = await resp.json();
        
        for (let i = 0; i < stationsList.length; i++) {
          const curr = stationsList[i];
          const currNode = `${curr.name}_${lineName}`;
          this.stations.add(curr.name);
          
          if (!this.graph[currNode]) {
            this.graph[currNode] = [];
          }

          if (i > 0) {
            const prev = stationsList[i - 1];
            const prevNode = `${prev.name}_${lineName}`;
            const weight = curr.travel_time_from_previous;

            // Link bi-directionally
            this.graph[currNode].push({ node: prevNode, weight, line: lineName });
            this.graph[prevNode].push({ node: currNode, weight, line: lineName });
          }
        }
      }

      // 3. Add transfers (Dadar, Kurla, CSMT, Masjid, Sandhurst Road)
      const stationLines = {};
      for (const nodeKey of Object.keys(this.graph)) {
        const [stationName, lineName] = nodeKey.split('_');
        if (!stationLines[stationName]) {
          stationLines[stationName] = [];
        }
        stationLines[stationName].push(lineName);
      }

      for (const [stationName, linesList] of Object.entries(stationLines)) {
        if (linesList.length > 1) {
          for (let i = 0; i < linesList.length; i++) {
            for (let j = i + 1; j < linesList.length; j++) {
              const node1 = `${stationName}_${linesList[i]}`;
              const node2 = `${stationName}_${linesList[j]}`;
              // 5 minutes transfer penalty
              this.graph[node1].push({ node: node2, weight: 5, line: 'Transfer' });
              this.graph[node2].push({ node: node1, weight: 5, line: 'Transfer' });
            }
          }
        }
      }
      return true;
    } catch (e) {
      console.error("Failed to initialize Railway Client Graph:", e);
      return false;
    }
  }

  getStations() {
    return Array.from(this.stations).sort();
  }

  getStationsForLine(lineName) {
    const stations = [];
    for (const nodeKey of Object.keys(this.graph)) {
      const [stationName, line] = nodeKey.split('_');
      if (line === lineName) {
        stations.push(stationName);
      }
    }
    // We should return them in correct sequence by matching the line JSON data.
    // However, unique array sorting is a safe fallback.
    return Array.from(new Set(stations));
  }

  calculateTravelTime(source, destination, isPeak = false) {
    if (source === destination) {
      return { duration: 0, path: [source] };
    }

    const sourcePrefix = source + '_';
    const destPrefix = destination + '_';

    const sourceNodes = Object.keys(this.graph).filter(n => n.startsWith(sourcePrefix));
    const destNodes = Object.keys(this.graph).filter(n => n.startsWith(destPrefix));

    if (sourceNodes.length === 0 || destNodes.length === 0) {
      return { duration: null, path: null };
    }

    // Dijkstra Priority Queue simulation
    const pq = [];
    const visited = new Set();

    for (const src of sourceNodes) {
      pq.push({ cost: 0, node: src, path: [src.split('_')[0]] });
    }

    while (pq.length > 0) {
      // Sort to get the minimum cost node (min-priority queue simulation)
      pq.sort((a, b) => a.cost - b.cost);
      const { cost, node, path } = pq.shift();

      if (visited.has(node)) continue;
      visited.add(node);

      const [currStation, currLine] = node.split('_');

      if (currStation === destination) {
        return { duration: cost, path };
      }

      const neighbors = this.graph[node] || [];
      for (const neighbor of neighbors) {
        if (!visited.has(neighbor.node)) {
          const neighborStation = neighbor.node.split('_')[0];
          const newCost = cost + neighbor.weight;
          const newPath = [...path];
          if (neighborStation !== path[path.length - 1]) {
            newPath.append ? newPath.append(neighborStation) : newPath.push(neighborStation);
          }
          pq.push({ cost: newCost, node: neighbor.node, path: newPath });
        }
      }
    }

    return { duration: null, path: null };
  }
}
