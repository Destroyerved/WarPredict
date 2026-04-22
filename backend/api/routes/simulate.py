from fastapi import APIRouter, HTTPException
from ..schemas import SimulationScenario, SimulationResponse
from ...simulation.scenario_engine import ScenarioEngine, ScenarioConfig

router = APIRouter(prefix="/simulate", tags=["simulation"])

engine = ScenarioEngine()


@router.post("/war", response_model=SimulationResponse)
async def run_war_simulation(scenario: SimulationScenario):
    try:
        config = ScenarioConfig(
            country_a=scenario.country_a,
            country_b=scenario.country_b,
            military_a=scenario.military_a,
            military_b=scenario.military_b,
            economy_a=scenario.economy_a,
            economy_b=scenario.economy_b,
            resolve_a=scenario.resolve_a,
            resolve_b=scenario.resolve_b,
            alliances_a=scenario.alliances_a,
            alliances_b=scenario.alliances_b,
            nuclear_enabled=scenario.nuclear_enabled,
            sanctions=scenario.sanctions
        )
        
        result = engine.run_scenario(config)
        
        return SimulationResponse(**result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/countries")
async def get_available_countries():
    return {"countries": engine.get_available_countries()}


@router.get("/country/{country_id}")
async def get_country_info(country_id: str):
    info = engine.get_country_info(country_id)
    if not info:
        raise HTTPException(status_code=404, detail="Country not found")
    return info