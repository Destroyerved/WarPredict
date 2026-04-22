from typing import List, Dict, Any, Optional
from .agent_based_model import WarSimulationModel, NationAgent
from .alliance_cascade import AllianceNetwork, create_default_alliance_network

class ScenarioConfig:
    def __init__(self, country_a: str, country_b: str,
                 military_a: float = 50, military_b: float = 50,
                 economy_a: float = 50, economy_b: float = 50,
                 resolve_a: float = 50, resolve_b: float = 50,
                 alliances_a: List[str] = None, alliances_b: List[str] = None,
                 nuclear_enabled: bool = False, sanctions: List[str] = None):
        self.country_a = country_a
        self.country_b = country_b
        self.military_a = military_a
        self.military_b = military_b
        self.economy_a = economy_a
        self.economy_b = economy_b
        self.resolve_a = resolve_a
        self.resolve_b = resolve_b
        self.alliances_a = alliances_a or []
        self.alliances_b = alliances_b or []
        self.nuclear_enabled = nuclear_enabled
        self.sanctions = sanctions or []


class ScenarioEngine:
    def __init__(self):
        self.alliance_network = create_default_alliance_network()
    
    def create_scenario(self, config: ScenarioConfig) -> WarSimulationModel:
        model = WarSimulationModel()
        country_to_agent_id = {}
        
        # Add primary combatants
        agent_a = model.add_nation(config.country_a, config.military_a, 
                                   config.economy_a, config.resolve_a, [])
        agent_b = model.add_nation(config.country_b, config.military_b,
                                   config.economy_b, config.resolve_b, [])
        
        country_to_agent_id[config.country_a] = agent_a.unique_id
        country_to_agent_id[config.country_b] = agent_b.unique_id
        
        # Add alliance countries as agents
        all_allies = set(config.alliances_a + config.alliances_b)
        for ally_country in all_allies:
            if ally_country not in country_to_agent_id:
                ally_agent = model.add_nation(ally_country, 40, 40, 40, [])
                country_to_agent_id[ally_country] = ally_agent.unique_id
        
        # Convert country codes to agent IDs and set alliances
        alliance_ids_a = [country_to_agent_id[c] for c in config.alliances_a if c in country_to_agent_id]
        alliance_ids_b = [country_to_agent_id[c] for c in config.alliances_b if c in country_to_agent_id]
        
        agent_a.alliances = alliance_ids_a
        agent_b.alliances = alliance_ids_b
        
        if config.nuclear_enabled:
            agent_a.nuclear_capable = True
            agent_b.nuclear_capable = True
        
        return model
    
    def run_scenario(self, config: ScenarioConfig, max_steps: int = 100) -> Dict[str, Any]:
        model = self.create_scenario(config)
        
        agent_a = model.agents_list[0]
        agent_b = model.agents_list[1]
        
        agent_a.declare_war(agent_b.unique_id)
        
        if config.alliances_a:
            cascade_result = self.alliance_network.simulate_cascade(
                config.country_a, config.country_b
            )
        else:
            cascade_result = {"cascade_result": [], "total_nations_drawn": 0}
        
        history = model.run_simulation(max_steps)
        
        return {
            "scenario": {
                "country_a": config.country_a,
                "country_b": config.country_b,
                "nuclear_enabled": config.nuclear_enabled
            },
            "simulation_results": model.get_results(),
            "alliance_cascade": cascade_result,
            "nuclear_deterrence": self._apply_nuclear_deterrence(config) if config.nuclear_enabled else None
        }
    
    def _apply_nuclear_deterrence(self, config: ScenarioConfig) -> Dict:
        if config.nuclear_enabled:
            military_diff = abs(config.military_a - config.military_b)
            if military_diff > 30:
                stronger = config.country_a if config.military_a > config.military_b else config.country_b
                return {
                    "deterrence_active": True,
                    "winner_due_to_nuclear": stronger,
                    "escalation_probability": 0.1
                }
        return {"deterrence_active": False}
    
    def compare_scenarios(self, scenarios: List[ScenarioConfig]) -> List[Dict]:
        results = []
        for scenario in scenarios:
            result = self.run_scenario(scenario)
            results.append(result)
        return results
    
    def get_available_countries(self) -> List[str]:
        return list(self.alliance_network.graph.nodes())
    
    def get_country_info(self, country: str) -> Dict:
        if country in self.alliance_network.graph.nodes():
            return self.alliance_network.graph.nodes[country]
        return {}