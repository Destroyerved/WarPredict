import numpy as np
import random
from typing import List, Dict, Any

class NationAgent:
    STATUS_PEACE = "peace"
    STATUS_WAR = "war"
    STATUS_CEASEFIRE = "ceasefire"
    STATUS_COLLAPSED = "collapsed"
    
    unique_id_counter = 0
    
    def __init__(self, country_id: str, military: float, economy: float, resolve: float, alliances: List[int]):
        NationAgent.unique_id_counter += 1
        self.unique_id = NationAgent.unique_id_counter
        self.country_id = country_id
        self.military_strength = military
        self.economic_health = economy
        self.resolve = resolve
        self.alliances = alliances
        self.status = self.STATUS_PEACE
        self.casualties = 0
        self.war_exhaustion = 0.0
        self.enemies = []
    
    def step(self):
        if self.status == self.STATUS_WAR:
            self.update_war_state()
        elif self.status == self.STATUS_CEASEFIRE:
            self.check_ceasefire_renewal()
    
    def update_war_state(self):
        attrition = np.random.uniform(1, 5) * (100 - self.military_strength) / 100
        self.military_strength = max(0, self.military_strength - attrition)
        
        economic_cost = np.random.uniform(0.5, 2.0)
        self.economic_health = max(0, self.economic_health - economic_cost)
        
        self.war_exhaustion = min(100, self.war_exhaustion + np.random.uniform(0.5, 2.0))
        
        new_casualties = int(np.random.uniform(10, 100) * (100 - self.military_strength) / 100)
        self.casualties += new_casualties
        
        if self.war_exhaustion > 80:
            self.consider_peace_offer()
        
        if self.military_strength < 10 or self.economic_health < 10:
            self.status = self.STATUS_COLLAPSED
    
    def consider_peace_offer(self):
        peace_prob = self.war_exhaustion / 100
        if random.random() < peace_prob * 0.3:
            self.status = self.STATUS_CEASEFIRE
    
    def check_ceasefire_renewal(self):
        if random.random() < 0.2:
            self.status = self.STATUS_WAR
    
    def declare_war(self, enemy_id: int):
        self.status = self.STATUS_WAR
        if enemy_id not in self.enemies:
            self.enemies.append(enemy_id)
    
    def get_state(self) -> Dict[str, Any]:
        return {
            "country_id": self.country_id,
            "status": self.status,
            "military_strength": round(self.military_strength, 2),
            "economic_health": round(self.economic_health, 2),
            "resolve": round(self.resolve, 2),
            "war_exhaustion": round(self.war_exhaustion, 2),
            "casualties": self.casualties,
            "alliances": self.alliances
        }


class WarSimulationModel:
    def __init__(self, num_agents: int = 10):
        self.num_agents = num_agents
        self.agents_list: List[NationAgent] = []
        self.history: List[Dict] = []
        self.step_count = 0
    
    def add_nation(self, country_id: str, military: float, economy: float, 
                   resolve: float, alliances: List[int]) -> NationAgent:
        agent = NationAgent(country_id, military, economy, resolve, alliances)
        self.agents_list.append(agent)
        return agent
    
    def get_agent(self, agent_id: int) -> NationAgent:
        for agent in self.agents_list:
            if agent.unique_id == agent_id:
                return agent
        return None
    
    def step(self):
        self.step_count += 1
        self.history.append({
            "step": self.step_count,
            "agents": [a.get_state() for a in self.agents_list]
        })
        for agent in self.agents_list:
            agent.step()
    
    def run_simulation(self, max_steps: int = 100) -> List[Dict]:
        for _ in range(max_steps):
            self.step()
            
            war_agents = [a for a in self.agents_list if a.status == NationAgent.STATUS_WAR]
            if len(war_agents) == 0:
                break
        
        return self.history
    
    def get_results(self) -> Dict[str, Any]:
        war_agents = [a for a in self.agents_list if a.status == NationAgent.STATUS_WAR]
        collapsed = [a for a in self.agents_list if a.status == NationAgent.STATUS_COLLAPSED]
        
        winner = None
        if len(war_agents) == 1:
            winner = war_agents[0].country_id
        elif len(war_agents) == 0 and len(collapsed) == len(self.agents_list):
            winner = "mutual_destruction"
        
        return {
            "final_state": [a.get_state() for a in self.agents_list],
            "steps": self.step_count,
            "total_casualties": sum(a.casualties for a in self.agents_list),
            "winner": winner,
            "history": self.history
        }