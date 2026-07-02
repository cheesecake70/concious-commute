import json
import os
import heapq

class RailwayGraph:
    def __init__(self, data_dir="data/railway"):
        self.graph = {}  # node -> list of (neighbor, weight, line)
        self.load_data(data_dir)
        self.add_transfers()

    def load_data(self, data_dir):
        lines = {
            "Western": "western_line.json",
            "Central": "central_line.json",
            "Harbour": "harbour_line.json"
        }
        
        for line_name, filename in lines.items():
            filepath = os.path.join(data_dir, filename)
            if not os.path.exists(filepath):
                continue
            with open(filepath, "r", encoding="utf-8") as f:
                stations = json.load(f)
                
            for i in range(len(stations)):
                current = stations[i]
                curr_node = (current["name"], line_name)
                if curr_node not in self.graph:
                    self.graph[curr_node] = []
                    
                if i > 0:
                    prev = stations[i-1]
                    prev_node = (prev["name"], line_name)
                    weight = current["travel_time_from_previous"]
                    
                    # Connect bi-directionally
                    self.graph[curr_node].append((prev_node, weight, line_name))
                    self.graph[prev_node].append((curr_node, weight, line_name))

    def add_transfers(self):
        # Identify stations that appear on multiple lines and link them
        station_lines = {}
        for (station_name, line_name) in self.graph.keys():
            if station_name not in station_lines:
                station_lines[station_name] = []
            station_lines[station_name].append(line_name)
            
        for station_name, lines in station_lines.items():
            if len(lines) > 1:
                # Add 5-minute transfer penalty between lines at the same station
                for i in range(len(lines)):
                    for j in range(i + 1, len(lines)):
                        node1 = (station_name, lines[i])
                        node2 = (station_name, lines[j])
                        self.graph[node1].append((node2, 5, "Transfer"))
                        self.graph[node2].append((node1, 5, "Transfer"))

    def get_stations(self):
        # Returns set of unique station names
        return sorted(list(set(name for (name, _) in self.graph.keys())))

    def get_lines_for_station(self, station_name):
        return sorted(list(set(line for (name, line) in self.graph.keys() if name == station_name)))

    def calculate_travel_time(self, source, destination, is_peak=False):
        """
        Calculates travel time using Dijkstra's algorithm.
        If is_peak is True, we add a 15% delay to the travel time to account for rush hour.
        Returns (duration_minutes, path_nodes) or (None, None) if unreachable.
        """
        if source == destination:
            return 0, [source]

        # Find all nodes corresponding to source and destination stations
        source_nodes = [node for node in self.graph.keys() if node[0] == source]
        dest_nodes = [node for node in self.graph.keys() if node[0] == destination]

        if not source_nodes or not dest_nodes:
            return None, None

        # Dijkstra from multiple source nodes
        # Priority queue stores (cost, current_node, path)
        pq = []
        for src in source_nodes:
            heapq.heappush(pq, (0, src, [src[0]]))

        visited = set()

        while pq:
            cost, curr, path = heapq.heappop(pq)

            if curr in visited:
                continue
            visited.add(curr)

            # Check if we reached destination station
            if curr[0] == destination:
                return cost, path

            for neighbor, weight, line in self.graph.get(curr, []):
                if neighbor not in visited:
                    new_cost = cost + weight
                    # Build path avoiding duplicate consecutive station names (due to transfers)
                    new_path = list(path)
                    if neighbor[0] != path[-1]:
                        new_path.append(neighbor[0])
                    heapq.heappush(pq, (new_cost, neighbor, new_path))

        return None, None
