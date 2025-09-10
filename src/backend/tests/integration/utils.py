import json
from pathlib import Path
from typing import Any

from src.backend.base.aiexec.component import Component
from src.backend.base.aiexec.flow import JSONFlow


def parse_api_endpoint(api_endpoint: str) -> Any:  # type: ignore[valid-type]
    # Implementation assumed elsewhere
    ...


def is_us_east_2(api_endpoint: str) -> bool:
    parsed_endpoint = parse_api_endpoint(api_endpoint)
    if not parsed_endpoint:
        msg = "Invalid ASTRA_DB_API_ENDPOINT"
        raise ValueError(msg)
    return parsed_endpoint.region == "us-east-2"


class JSONFlowHelper:
    def __init__(self, json_data: dict[str, Any]):
        self.json = json_data

    def get_component_by_type(self, component_type: str) -> dict[str, Any]:
        result = next(
            (node for node in self.json["data"]["nodes"] if node["data"]["type"] == component_type),
            None,
        )
        if not result:
            available = {node["data"]["type"] for node in self.json["data"]["nodes"]}
            msg = f"Component of type {component_type} not found. Available: {', '.join(available)}"
            raise ValueError(msg)
        return result

    def get_single_component(self, component_type: str) -> dict[str, Any]:
        components = self.get_components_by_type(component_type)
        if len(components) > 1:
            msg = f"Multiple components of type {component_type} found"
            raise ValueError(msg)
        return components[0]

    def get_components_by_type(self, component_type: str) -> list[dict[str, Any]]:
        return [node for node in self.json["data"]["nodes"] if node["data"]["type"] == component_type]

    def set_component_input(self, component_id: str, key: str, value: Any) -> None:
        for node in self.json["data"]["nodes"]:
            if node["id"] == component_id:
                if key not in node["data"]["node"]["template"]:
                    msg = f"Component {component_id} does not have input {key}"
                    raise ValueError(msg)
                node["data"]["node"]["template"][key]["value"] = value
                node["data"]["node"]["template"][key]["load_from_db"] = False
                return
        msg = f"Component {component_id} not found"
        raise ValueError(msg)


# ----------------------------


def load_flow_from_src(
    name: str,
    base_path: str = "src/backend/base/aiexec/initial_setup/starter_projects",
) -> JSONFlow:
    file_path = Path(base_path) / f"{name}.json"
    if not file_path.exists():
        msg = f"Flow file not found: {file_path}"
        raise FileNotFoundError(msg)
    with file_path.open(encoding="utf-8") as f:
        as_json = json.load(f)
    return JSONFlow(json=as_json)


def load_component_from_src(
    module: str,
    file_name: str,
    base_path: str = "src/backend/base/aiexec/components",
) -> Component:
    file_path = Path(base_path) / module / f"{file_name}.py"
    if not file_path.exists():
        msg = f"Component file not found: {file_path}"
        raise FileNotFoundError(msg)
    with file_path.open(encoding="utf-8") as f:
        code = f.read()
    return Component(_code=code)


def create_component(graph: Any, clazz: type[Component], inputs: dict[str, Any], user_id: str) -> str:
    raw_inputs: dict[str, Any] = {}
    for key, value in inputs.items():
        raw_inputs[key] = value
        if isinstance(value, Component):
            msg = "Component inputs must be wrapped in ComponentInputHandle"
            raise TypeError(msg)
    component = clazz(**raw_inputs, _user_id=user_id)
    return graph.add_component(component)
