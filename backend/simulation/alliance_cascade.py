import networkx as nx
import random
from typing import List, Dict, Tuple, Set

class AllianceNetwork:
    def __init__(self):
        self.graph = nx.DiGraph()
        self.alliance_types = {
            "NATO": {"color": "#3b82f6", "strength": 1.0},
            "CIS": {"color": "#ef4444", "strength": 0.8},
            "CSTO": {"color": "#f59e0b", "strength": 0.7},
            "EU": {"color": "#10b981", "strength": 0.9},
            "bilateral": {"color": "#8b5cf6", "strength": 0.5}
        }
    
    def add_nation(self, country_id: str, data: Dict = None):
        self.graph.add_node(country_id, **(data or {}))
    
    def add_alliance(self, country_a: str, country_b: str, alliance_type: str = "bilateral", strength: float = None):
        if alliance_type not in self.alliance_types:
            alliance_type = "bilateral"
        
        if strength is None:
            strength = self.alliance_types[alliance_type]["strength"]
        
        self.graph.add_edge(country_a, country_b, 
                           alliance_type=alliance_type, 
                           strength=strength)
        self.graph.add_edge(country_b, country_a,
                           alliance_type=alliance_type,
                           strength=strength)
    
    def get_allies(self, country: str) -> List[str]:
        return list(self.graph.neighbors(country))
    
    def get_alliance_strength(self, country_a: str, country_b: str) -> float:
        if self.graph.has_edge(country_a, country_b):
            return self.graph[country_a][country_b].get("strength", 0.0)
        return 0.0
    
    def simulate_cascade(self, aggressor: str, defender: str, max_cascade_depth: int = 3) -> Dict:
        triggered = {aggressor}
        cascade_chain = [(aggressor, "initial_aggressor")]
        
        current_level = {aggressor}
        
        for depth in range(max_cascade_depth):
            next_level = set()
            
            for country in current_level:
                allies = self.get_allies(country)
                for ally in allies:
                    if ally not in triggered:
                        alliance_strength = self.get_alliance_strength(country, ally)
                        trigger_prob = 0.3 + (alliance_strength * 0.5)
                        
                        if random.random() < trigger_prob:
                            next_level.add(ally)
                            triggered.add(ally)
                            cascade_chain.append((ally, f"depth_{depth}"))
            
            current_level = next_level
            
            if not current_level:
                break
        
        return {
            "initial_conflict": [aggressor, defender],
            "cascade_result": list(triggered),
            "cascade_depth": len(cascade_chain) - 1,
            "chain": cascade_chain,
            "total_nations_drawn": len(triggered)
        }
    
    def get_network_stats(self) -> Dict:
        return {
            "total_nations": self.graph.number_of_nodes(),
            "total_alliances": self.graph.number_of_edges(),
            "density": nx.density(self.graph),
            "clustering_coefficient": nx.average_clustering(self.graph.to_undirected())
        }
    
    def get_visualization_data(self) -> Dict:
        nodes = []
        for node in self.graph.nodes():
            nodes.append({
                "id": node,
                "data": self.graph.nodes[node]
            })
        
        links = []
        for u, v, data in self.graph.edges(data=True):
            links.append({
                "source": u,
                "target": v,
                "alliance_type": data.get("alliance_type", "bilateral"),
                "strength": data.get("strength", 0.5)
            })
        
        return {"nodes": nodes, "links": links}


def create_default_alliance_network() -> AllianceNetwork:
    network = AllianceNetwork()
    
    nations = {
        "USA": {"group": "NATO", "nuclear": True},
        "GBR": {"group": "NATO", "nuclear": True},
        "FRA": {"group": "NATO", "nuclear": True},
        "DEU": {"group": "NATO", "nuclear": False},
        "POL": {"group": "NATO", "nuclear": False},
        "CAN": {"group": "NATO", "nuclear": False},
        "RUS": {"group": "CIS", "nuclear": True},
        "CHN": {"group": "neutral", "nuclear": True},
        "IND": {"group": "neutral", "nuclear": True},
        "PAK": {"group": "neutral", "nuclear": True},
    }
    
    for country, data in nations.items():
        network.add_nation(country, data)
    
    nato_countries = ["USA", "GBR", "FRA", "DEU", "POL", "CAN"]
    for i, c1 in enumerate(nato_countries):
        for c2 in nato_countries[i+1:]:
            network.add_alliance(c1, c2, "NATO")
    
    cis_countries = ["RUS"]
    for c in cis_countries:
        network.add_alliance("RUS", c, "CIS")
    
    network.add_alliance("USA", "GBR", "bilateral", 0.9)
    network.add_alliance("USA", "FRA", "bilateral", 0.8)
    network.add_alliance("CHN", "PAK", "bilateral", 0.7)
    network.add_alliance("CHN", "RUS", "bilateral", 0.6)
    
    return network