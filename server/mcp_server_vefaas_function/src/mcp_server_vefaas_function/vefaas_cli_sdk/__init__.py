# Copyright (c) 2025 Beijing Volcano Engine Technology Co., Ltd. and/or its affiliates
# SPDX-License-Identifier: MIT

"""veFaaS CLI SDK - Ported capabilities from vefaas-cli (TypeScript)"""

from .detector import auto_detect, DetectionResult
from .deploy import (
    DeployConfig,
    DeployResult,
    VeFaaSClient,
    deploy_application,
    get_console_url,
    get_application_console_url,
    extract_access_url_from_cloud_resource,
    wait_for_function_release,
    wait_for_application_deploy,
    wait_for_dependency_install,
)
from .config import (
    VefaasConfig,
    FunctionConfig,
    TriggerConfig,
    read_config,
    write_config,
    get_linked_ids,
    get_linked_region,
)

__all__ = [
    # Detector
    "auto_detect",
    "DetectionResult",
    # Deploy
    "DeployConfig",
    "DeployResult",
    "VeFaaSClient",
    "deploy_application",
    "get_console_url",
    "get_application_console_url",
    "extract_access_url_from_cloud_resource",
    "wait_for_function_release",
    "wait_for_application_deploy",
    "wait_for_dependency_install",
    # Config
    "VefaasConfig",
    "FunctionConfig",
    "TriggerConfig",
    "read_config",
    "write_config",
    "get_linked_ids",
    "get_linked_region",
]
