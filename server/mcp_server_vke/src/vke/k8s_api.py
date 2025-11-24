# coding=utf-8
import http
import json
import time
import base64
import os
from datetime import datetime

from kubernetes.client import api_client
import yaml
from kubernetes import client, config

from .api.api import VkeAPI

allow_write = os.getenv("ALLOW_WRITE", "false").lower() == "true"


def retrive_kubeconfig(service: VkeAPI, cluster_id: str) -> str:
    """
    Retrive the public kubeconfig of the cluster.
    """
    list_kubeconfig_req = {
        "PageNumber": 1,
        "PageSize": 100,
        "Filter": {
            "ClusterIds": [cluster_id],
            "Types": ["Public"],
        },
    }

    response = service.mcp_post(
        "VkeMcpListKubeconfigs", {}, json.dumps(list_kubeconfig_req)
    )
    response = json.loads(response)
    result = response["Result"]
    total_count = result["TotalCount"]
    if total_count == 0:
        raise ValueError(f"no public kubeconfig found for cluster {cluster_id}")

    for item in result["Items"]:
        if item["ClusterId"] != cluster_id:
            continue
        if item["Type"] != "Public":
            continue
        if not item["Kubeconfig"]:
            continue

        expire_dt = datetime.strptime(item["ExpireTime"], "%Y-%m-%dT%H:%M:%S%z")
        if expire_dt.timestamp() < time.time():
            continue

        return item["Kubeconfig"]

    raise ValueError(
        f"no valid public kubeconfig found for cluster {cluster_id}, you should create one first"
    )


def new_api_client(service: VkeAPI, cluster_id: str) -> client.ApiClient:
    """
    Initialize the k8s API client for the given cluster.
    """
    kubeconfig_b64 = retrive_kubeconfig(service, cluster_id)
    if not kubeconfig_b64:
        raise ValueError("failed to retrieve kubeconfig")

    try:
        kubeconfig_yaml = base64.b64decode(kubeconfig_b64).decode("utf-8")
        kubeconfig_dict = yaml.safe_load(kubeconfig_yaml)

        api_client = config.new_client_from_config_dict(kubeconfig_dict)
    except base64.binascii.Error as e:
        raise ValueError(f"Invalid base64 encoding: {str(e)}")
    except yaml.YAMLError as e:
        raise ValueError(f"Invalid kubeconfig YAML: {str(e)}")
    except Exception as e:
        raise ValueError(
            f"Unexpected error while initializing k8s API client: {str(e)}"
        )

    api_client.user_agent = "vke-mcp-server"

    return api_client


def new_rest_url(
    kind: str,
    api_version: str,
    namespace: str = "",
    name: str = "",
) -> str:
    """
    Make the resource path for k8s API.
    """
    # Correctly determine the base path for core APIs vs. other APIs
    if "/" in api_version:
        base_path = f"/apis/{api_version}"
    else:
        base_path = f"/api/{api_version}"

    if namespace:
        path = f"{base_path}/namespaces/{namespace}/{kind}s"
    else:
        path = f"{base_path}/{kind}s"

    if name:
        path += f"/{name}"

    return path.lower()


def get_resources(
    api_client: api_client.ApiClient,
    kind: str,
    api_version: str,
    namespace: str = "",
    name: str = "",
    label_selectors: str = "",
    field_selectors: str = "",
    limit: int = 500,
) -> dict:
    """
    Get or list, when name is not specified, K8s resources from the given K8s cluster.
    """
    resource_path = new_rest_url(kind, api_version, namespace, name)

    params = {}
    if label_selectors:
        params["labelSelector"] = label_selectors
    if field_selectors:
        params["fieldSelector"] = field_selectors
    if limit:
        params["limit"] = limit

    return api_client.call_api(
        resource_path,
        "GET",
        query_params=params,
        response_type=object,
        _return_http_data_only=True,
    )


def delete_resource(
    api_client: api_client.ApiClient,
    kind: str,
    api_version: str,
    namespace: str,
    name: str,
) -> dict:
    """
    Delete K8s resources from the given K8s cluster.
    """
    if not allow_write:
        raise ValueError("delete operation is not allowed")

    if not name:
        raise ValueError("name is required for delete operation")

    resource_path = new_rest_url(kind, api_version, namespace, name)
    return api_client.call_api(
        resource_path,
        http.HTTPMethod.DELETE,
        response_type=object,
        _return_http_data_only=True,
    )


def update_resource(
    api_client: api_client.ApiClient,
    kind: str,
    api_version: str,
    body: object,
    namespace: str = "",
    name: str = "",
) -> dict:
    """
    Update K8s resources from the given K8s cluster.
    """
    if not allow_write:
        raise ValueError("update operation is not allowed")

    if not name:
        raise ValueError("name is required for update operation")

    resource_path = new_rest_url(kind, api_version, namespace, name)
    return api_client.call_api(
        resource_path,
        http.HTTPMethod.PUT,
        response_type=object,
        body=body,
        _return_http_data_only=True,
    )


def create_resource(
    api_client: api_client.ApiClient,
    kind: str,
    api_version: str,
    body: object,
    namespace: str,
) -> dict:
    """
    Create K8s resources from the given K8s cluster.
    """
    resource_path = new_rest_url(kind, api_version, namespace, "")
    return api_client.call_api(
        resource_path,
        http.HTTPMethod.POST,
        response_type=object,
        body=body,
        _return_http_data_only=True,
    )


def patch_resource(
    api_client: api_client.ApiClient,
    kind: str,
    api_version: str,
    body: object,
    namespace: str,
    name: str,
) -> dict:
    """
    Patch K8s resources from the given K8s cluster.
    """
    if not name:
        raise ValueError("name is required for patch operation")

    resource_path = new_rest_url(kind, api_version, namespace, name)

    try:
        # First try with strategic merge patch
        return api_client.call_api(
            resource_path,
            http.HTTPMethod.PATCH,
            response_type=object,
            header_params={"Content-Type": "application/strategic-merge-patch+json"},
            body=body,
            _return_http_data_only=True,
        )
    except Exception as e:
        if "415" in str(e) or "Unsupported Media Type" in str(e):
            return api_client.call_api(
                resource_path,
                http.HTTPMethod.PATCH,
                response_type=object,
                header_params={"Content-Type": "application/merge-patch+json"},
                body=body,
                _return_http_data_only=True,
            )
        else:
            raise ValueError(
                f"Unexpected error while patching resource {name} of kind {kind} in namespace {namespace}: {str(e)}"
            )


def _apply_yaml_object(
    api_client: api_client.ApiClient,
    yaml_object: dict,
    namespace: str = "",
    force: bool = False,
) -> dict:
    """
    Apply a single K8s resource from the given K8s cluster.
    """
    kind = yaml_object.get("kind", "")
    api_version = yaml_object.get("apiVersion", "")
    metadata = yaml_object.get("metadata", {})

    namespace = metadata.get("namespace", namespace)
    name = metadata.get("name", "")

    exist = True
    try:
        # Try to get the resource to check if it exists
        get_resources(
            api_client,
            namespace=namespace,
            name=name,
            kind=kind,
            api_version=api_version,
        )
    except Exception as e:
        if "NotFound" in str(e):
            exist = False
        else:
            raise ValueError(
                f"Unexpected error while getting resource {name} of kind {kind} in namespace {namespace}: {str(e)}"
            )

    if exist and force:
        if not allow_write:
            raise ValueError("update operation is not allowed")

        # If the resource exists and force is True, patch the resource
        return patch_resource(
            api_client,
            kind,
            api_version,
            body=yaml_object,
            namespace=namespace,
            name=name,
        )
    else:
        # If the resource does not exist or force is False, create the resource
        return create_resource(
            api_client,
            kind,
            api_version,
            body=yaml_object,
            namespace=namespace,
        )


def apply_from_yaml(
    api_client: api_client.ApiClient,
    yaml_objects: list,
    namespace: str = "",
    force: bool = False,
) -> dict:
    """
    Apply K8s resources from the given K8s cluster.
    """
    results = []
    for yaml_object in yaml_objects:
        if not yaml_object:
            continue

        results.append(
            _apply_yaml_object(
                api_client,
                yaml_object,
                namespace,
                force,
            )
        )

    return results
