# Copyright (c) 2025 Beijing Volcano Engine Technology Co., Ltd. and/or its affiliates
# SPDX-License-Identifier: MIT

"""
Configuration Module

This module handles reading and writing veFaaS configuration files.
Supports both `.vefaas/config.json` (vefaas-cli format) and `vefaas.yaml` (legacy format).

Configuration priority:
1. User-provided parameters
2. .vefaas/config.json
3. vefaas.yaml (backward compatibility)

Write strategy: Update both formats on success to prevent config drift.
"""

import json
import os
import logging
from dataclasses import dataclass, field, asdict
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

# Config file paths
VEFAAS_CONFIG_DIR = ".vefaas"
VEFAAS_CONFIG_FILE = "config.json"
VEFAAS_YAML_FILE = "vefaas.yaml"


@dataclass
class TriggerConfig:
    """Trigger configuration (API gateway info)"""
    type: str = "apig"
    system_url: Optional[str] = None
    inner_url: Optional[str] = None
    id: Optional[str] = None


@dataclass
class FunctionConfig:
    """Function configuration"""
    id: str = ""
    runtime: Optional[str] = None
    region: str = "cn-beijing"
    application_id: Optional[str] = None


@dataclass
class VefaasConfig:
    """
    veFaaS configuration structure.
    Compatible with vefaas-cli's .vefaas/config.json format.
    """
    version: str = "1.0"
    function: FunctionConfig = field(default_factory=FunctionConfig)
    triggers: Optional[TriggerConfig] = None

    # Additional fields for MCP compatibility (not in vefaas-cli)
    name: Optional[str] = None
    command: Optional[str] = None

    def to_json_dict(self) -> Dict[str, Any]:
        """Convert to JSON-serializable dict (vefaas-cli format)"""
        result = {
            "version": self.version,
            "function": {
                "id": self.function.id,
                "region": self.function.region,
            }
        }
        if self.function.runtime:
            result["function"]["runtime"] = self.function.runtime
        if self.function.application_id:
            result["function"]["application_id"] = self.function.application_id
        if self.triggers:
            result["triggers"] = {}
            result["triggers"]["type"] = self.triggers.type
            if self.triggers.system_url:
                result["triggers"]["system_url"] = self.triggers.system_url
            if self.triggers.inner_url:
                result["triggers"]["inner_url"] = self.triggers.inner_url
            if self.triggers.id:
                result["triggers"]["id"] = self.triggers.id
        return result

    def to_yaml_dict(self) -> Dict[str, Any]:
        """Convert to YAML-compatible dict (legacy format)"""
        result = {}
        if self.function.id:
            result["function_id"] = self.function.id
        if self.name:
            result["name"] = self.name
        if self.function.region:
            result["region"] = self.function.region
        if self.function.runtime:
            result["runtime"] = self.function.runtime
        if self.command:
            result["command"] = self.command
        if self.function.application_id:
            result["application_id"] = self.function.application_id
        return result


def get_config_paths(project_path: str) -> tuple:
    """Get configuration file paths"""
    config_dir = os.path.join(project_path, VEFAAS_CONFIG_DIR)
    json_path = os.path.join(config_dir, VEFAAS_CONFIG_FILE)
    yaml_path = os.path.join(project_path, VEFAAS_YAML_FILE)
    return config_dir, json_path, yaml_path


def read_config(project_path: str) -> Optional[VefaasConfig]:
    """
    Read veFaaS configuration from project directory.

    Priority:
    1. .vefaas/config.json (vefaas-cli format)
    2. vefaas.yaml (legacy MCP format)

    Returns:
        VefaasConfig if found, None otherwise
    """
    config_dir, json_path, yaml_path = get_config_paths(project_path)

    # Try .vefaas/config.json first
    if os.path.exists(json_path):
        try:
            with open(json_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            func_data = data.get("function", {})
            triggers_data = data.get("triggers")

            config = VefaasConfig(
                version=data.get("version", "1.0"),
                function=FunctionConfig(
                    id=func_data.get("id", ""),
                    runtime=func_data.get("runtime"),
                    region=func_data.get("region", "cn-beijing"),
                    application_id=func_data.get("application_id"),
                ),
            )

            if triggers_data:
                config.triggers = TriggerConfig(
                    type=triggers_data.get("type", "apig"),
                    system_url=triggers_data.get("system_url"),
                    inner_url=triggers_data.get("inner_url"),
                    id=triggers_data.get("id"),
                )

            logger.info(f"[config] Loaded from .vefaas/config.json: function_id={config.function.id}")
            return config
        except Exception as e:
            logger.warning(f"[config] Failed to read .vefaas/config.json: {e}")

    # Fallback to vefaas.yaml
    if os.path.exists(yaml_path):
        try:
            # Simple YAML parsing (key: value format)
            data = {}
            with open(yaml_path, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#"):
                        continue
                    if ":" in line:
                        key, value = line.split(":", 1)
                        data[key.strip()] = value.strip()

            config = VefaasConfig(
                function=FunctionConfig(
                    id=data.get("function_id", ""),
                    runtime=data.get("runtime"),
                    region=data.get("region", "cn-beijing"),
                    application_id=data.get("application_id"),
                ),
                name=data.get("name"),
                command=data.get("command"),
            )

            logger.info(f"[config] Loaded from vefaas.yaml: function_id={config.function.id}")
            return config
        except Exception as e:
            logger.warning(f"[config] Failed to read vefaas.yaml: {e}")

    return None


def write_config(project_path: str, config: VefaasConfig) -> None:
    """
    Write veFaaS configuration to project directory.

    Writes to BOTH formats to prevent config drift:
    1. .vefaas/config.json (vefaas-cli compatible)
    2. vefaas.yaml (legacy MCP format)
    """
    config_dir, json_path, yaml_path = get_config_paths(project_path)

    # Ensure .vefaas directory exists
    os.makedirs(config_dir, exist_ok=True)

    # Write .vefaas/config.json
    try:
        json_data = config.to_json_dict()
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(json_data, f, indent=2, ensure_ascii=False)
        logger.info(f"[config] Saved .vefaas/config.json")
    except Exception as e:
        logger.warning(f"[config] Failed to write .vefaas/config.json: {e}")

    # Write vefaas.yaml
    try:
        yaml_data = config.to_yaml_dict()
        with open(yaml_path, "w", encoding="utf-8") as f:
            for key, value in yaml_data.items():
                if value is not None:
                    f.write(f"{key}: {value}\n")
        logger.info(f"[config] Saved vefaas.yaml")
    except Exception as e:
        logger.warning(f"[config] Failed to write vefaas.yaml: {e}")

    # Ensure .vefaas is in .gitignore
    _ensure_gitignore(project_path)


def _ensure_gitignore(project_path: str) -> None:
    """Ensure .vefaas/ is in .gitignore"""
    gitignore_path = os.path.join(project_path, ".gitignore")

    try:
        content = ""
        if os.path.exists(gitignore_path):
            with open(gitignore_path, "r", encoding="utf-8") as f:
                content = f.read()

        # Check if .vefaas is already ignored
        import re
        if not re.search(r'(^|\n)\s*(?:/)?.vefaas(?:/)?', content):
            with open(gitignore_path, "a", encoding="utf-8") as f:
                if content and not content.endswith("\n"):
                    f.write("\n")
                f.write(".vefaas/\n")
            logger.info(f"[config] Added .vefaas/ to .gitignore")
    except Exception as e:
        logger.debug(f"[config] Failed to update .gitignore: {e}")


def get_linked_ids(project_path: str) -> tuple:
    """
    Get linked function_id and application_id from config.

    Returns:
        (function_id, application_id) tuple, None values if not found
    """
    config = read_config(project_path)
    if config:
        func_id = config.function.id if config.function.id else None
        app_id = config.function.application_id if config.function.application_id else None
        return func_id, app_id
    return None, None


def get_linked_region(project_path: str) -> Optional[str]:
    """Get linked region from config"""
    config = read_config(project_path)
    if config and config.function.region:
        return config.function.region
    return None
