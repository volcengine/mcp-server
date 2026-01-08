# Copyright (c) 2025 Beijing Volcano Engine Technology Co., Ltd. and/or its affiliates
# SPDX-License-Identifier: MIT

"""
Project Detection Module

This module encapsulates project detection logic for veFaaS applications,
ported from vefaas-cli (detector.ts).

Supported frameworks:
- Node.js: Next.js, Nuxt, Vite, VitePress, Rspress, Astro, Express, SvelteKit, Remix, CRA, Angular, Gatsby
- Python: FastAPI, Flask, Streamlit, Django
- Static: HTML sites, Hugo, MkDocs, Zola, Hexo
"""

import os
import json
import re
from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List
import logging

logger = logging.getLogger(__name__)


@dataclass
class DetectionResult:
    """Project detection result"""
    install_command: str = ""      # Install command
    build_command: str = ""        # Build command
    output_path: str = "./"        # Build output directory
    start_command: str = ""        # Start command
    port: int = 8000               # Port
    runtime: str = "native-node20/v1"  # Runtime
    framework: str = ""            # Framework name
    is_static: bool = False        # Is static site


def auto_detect(target_path: str) -> DetectionResult:
    """
    Auto-detect project runtime, framework and related commands based on file system.

    Args:
        target_path: Project root directory path

    Returns:
        DetectionResult: Detection result
    """
    root = os.path.abspath(target_path)
    logger.debug(f"[detect] Starting framework detection for: {root}")

    # Detect build and run scripts
    build_script = _find_script(root, ["build.sh"])
    run_script = _find_script(root, ["run.sh"])
    has_build = build_script is not None
    has_run = run_script is not None
    logger.debug(f"[detect] Found scripts: build={build_script or 'none'}, run={run_script or 'none'}")

    fallback = DetectionResult(
        build_command=build_script or "./build.sh",
        start_command=run_script or "./run.sh",
    )

    # Try detectors in priority order
    detectors = [_detect_node, _detect_python, _detect_static]

    for detector in detectors:
        try:
            result = detector(root)
            if result:
                # Override with custom scripts if present
                if has_build and build_script:
                    result.build_command = build_script
                if has_run and run_script:
                    result.start_command = run_script
                if has_build and has_run:
                    result.port = 8000
                    result.output_path = "./"
                logger.debug(f"[detect] Framework detected: {result.framework or 'none'}")
                return result
        except Exception as e:
            logger.debug(f"[detect] Detector error: {e}")
            continue

    logger.debug("[detect] No framework detected, using fallback")
    return fallback


def _find_script(root: str, names: List[str]) -> Optional[str]:
    """Find script file"""
    for name in names:
        script_path = os.path.join(root, name)
        if os.path.exists(script_path):
            return f"./{name}"
    return None


def _exists(path: str) -> bool:
    """Check if path exists"""
    return os.path.exists(path)


def _read_text(path: str) -> Optional[str]:
    """Read text file"""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    except:
        return None


def _read_json(path: str) -> Dict[str, Any]:
    """Read JSON file"""
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return {}


# ==================== Node.js Detection ====================

def _detect_node(root: str) -> Optional[DetectionResult]:
    """Detect Node.js project"""
    pkg_path = os.path.join(root, "package.json")
    has_pkg = _exists(pkg_path)

    is_node = (
        has_pkg or
        _exists(os.path.join(root, "package-lock.json")) or
        _exists(os.path.join(root, "pnpm-lock.yaml")) or
        _exists(os.path.join(root, "yarn.lock"))
    )

    if not is_node:
        return None

    pkg = _read_json(pkg_path) if has_pkg else {}
    scripts = pkg.get("scripts", {})
    pm = _get_node_package_manager(root, pkg)
    framework = _detect_node_framework(pkg)

    build_cmd = _resolve_node_build_command(pm, scripts, framework)
    output_path = _resolve_node_output_path(framework, scripts, root)
    start_cmd = _resolve_node_start_command(pm, scripts, framework, root, pkg)
    install_cmd = _resolve_node_install_command(pm, root)
    port = _detect_node_port(root, scripts, framework, pkg)
    is_static = _should_use_static_hosting(framework, root, pkg, scripts)

    return DetectionResult(
        install_command=install_cmd,
        build_command=build_cmd,
        output_path=output_path,
        start_command=start_cmd,
        port=port or 8000,
        runtime="native-node20/v1",
        framework=framework,
        is_static=is_static,
    )


def _get_node_package_manager(root: str, pkg: Dict) -> str:
    """Get Node.js package manager"""
    if _exists(os.path.join(root, "pnpm-lock.yaml")):
        return "pnpm"
    if _exists(os.path.join(root, "yarn.lock")):
        return "yarn"
    pm_field = pkg.get("packageManager", "").lower()
    if pm_field.startswith("pnpm"):
        return "pnpm"
    if pm_field.startswith("yarn"):
        return "yarn"
    return "npm"


def _detect_node_framework(pkg: Dict) -> str:
    """Detect Node.js framework"""
    deps = {**pkg.get("dependencies", {}), **pkg.get("devDependencies", {})}

    if "next" in deps:
        return "next"
    if "vitepress" in deps:
        return "vitepress"
    if "rspress" in deps:
        return "rspress"
    if "vite" in deps:
        return "vite"
    if "nuxt" in deps or "nuxi" in deps:
        return "nuxt"
    if "astro" in deps:
        return "astro"
    if "react-scripts" in deps:
        return "cra"
    if "@angular/core" in deps or "@angular/cli" in deps:
        return "angular"
    if "@nestjs/core" in deps:
        return "nest"
    if "express" in deps:
        return "express"
    if "@sveltejs/kit" in deps:
        return "sveltekit"
    if "@remix-run/dev" in deps:
        return "remix"
    if "gatsby" in deps:
        return "gatsby"
    if "@gulux/gulux" in deps or "@gulux/cli" in deps or "gulux" in deps:
        return "gulux"
    return ""


def _pm_run(pm: str, script: str) -> str:
    """Generate package manager run command"""
    if pm == "pnpm":
        return f"pnpm run {script}"
    if pm == "yarn":
        return f"yarn {script}"
    return f"npm run {script}"


def _resolve_node_build_command(pm: str, scripts: Dict, framework: str) -> str:
    """Resolve Node.js build command"""
    if scripts.get("build"):
        base = _pm_run(pm, "build")
        if framework == "nuxt":
            return f"NITRO_PRESET=node-server {base}"
        return base

    framework_builds = {
        "next": "npx next build",
        "vite": "npx vite build",
        "sveltekit": "npx vite build",
        "astro": "npx vite build",
        "vitepress": "npx vitepress build",
        "rspress": "npx rspress build",
        "nuxt": "NITRO_PRESET=node-server npx nuxi build",
        "cra": "npx react-scripts build",
        "angular": "npx ng build --configuration production",
        "gatsby": "npx gatsby build",
    }
    return framework_builds.get(framework, "")


def _resolve_node_output_path(framework: str, scripts: Dict, root: str) -> str:
    """Resolve Node.js output path"""
    output_paths = {
        "next": "./",
        "vite": "dist",
        "sveltekit": "dist",
        "astro": "dist",
        "vitepress": ".vitepress/dist",
        "rspress": "doc_build",
        "nuxt": ".output",
        "cra": "build",
        "angular": "dist",
        "gatsby": "public",
        "gulux": "output",
    }
    return output_paths.get(framework, "./")


def _resolve_node_install_command(pm: str, root: str) -> str:
    """Resolve Node.js install command"""
    if pm == "pnpm":
        return "pnpm install"
    if pm == "yarn":
        return "yarn install"
    # npm: prefer ci
    if _exists(os.path.join(root, "package-lock.json")):
        return "npm ci"
    return "npm install"


def _resolve_node_start_command(pm: str, scripts: Dict, framework: str, root: str, pkg: Dict) -> str:
    """Resolve Node.js start command"""
    # Static sites use Caddy
    if _should_use_static_hosting(framework, root, pkg, scripts):
        return "caddy run --config DefaultCaddyFile --adapter caddyfile"

    if scripts.get("start"):
        return _pm_run(pm, "start")

    framework_starts = {
        "next": "npx next start -p ${PORT:-8080}",
        "nuxt": "HOST=0.0.0.0 node ./server/index.mjs",
        "nest": _pm_run(pm, "start:prod"),
        "express": "node server.js",
    }
    return framework_starts.get(framework, "")


def _detect_node_port(root: str, scripts: Dict, framework: str, pkg: Dict) -> int:
    """Detect Node.js port"""
    if _should_use_static_hosting(framework, root, pkg, scripts):
        return 8000

    # Detect port from scripts
    start_script = scripts.get("start", "")
    port_match = re.search(r"--port[=\s]+(\d+)", start_script)
    if port_match:
        return int(port_match.group(1))

    # Framework default ports
    framework_ports = {
        "next": 3000,
        "nuxt": 3000,
        "nest": 3000,
        "cra": 3000,
        "express": 3000,
        "remix": 3000,
        "gatsby": 3000,
        "vite": 4173,
        "vitepress": 4173,
        "sveltekit": 4173,
        "astro": 4321,
        "angular": 8080,
    }
    return framework_ports.get(framework, 3000)


def _should_use_static_hosting(framework: str, root: str, pkg: Dict, scripts: Dict) -> bool:
    """Determine if static hosting should be used (based on vefaas-cli shouldUseStaticHosting)"""
    deps = {**pkg.get("dependencies", {}), **pkg.get("devDependencies", {})}

    if framework in ["vitepress", "rspress", "cra", "angular", "gatsby"]:
        return True

    if framework == "astro":
        ssr_adapters = ["@astrojs/node", "@astrojs/deno", "@astrojs/netlify", "@astrojs/vercel", "@astrojs/cloudflare"]
        if any(adapter in deps for adapter in ssr_adapters):
            return False
        # Check if astro.config has output: 'server'
        if _is_astro_ssr(root):
            return False
        return True

    if framework == "next":
        # next export or out dir exists means static
        build_script = scripts.get("build", "")
        if "next export" in build_script:
            return True
        if _exists(os.path.join(root, "out")):
            return True
        return False

    if framework == "sveltekit":
        if "@sveltejs/adapter-static" in deps:
            return True
        if "@sveltejs/adapter-node" in deps:
            return False
        return False

    if framework == "nuxt":
        build_script = scripts.get("build", "")
        if "nuxi generate" in build_script:
            return True
        if "NITRO_PRESET=static" in build_script:
            return True
        return False

    if framework == "vite":
        # Vite: if SSR signals present, not static; otherwise default to static (SPA/MPA)
        if _is_vite_ssr(root, pkg, scripts):
            return False
        return True  # Default static

    return False


def _is_vite_ssr(root: str, pkg: Dict, scripts: Dict) -> bool:
    """Detect if Vite is in SSR mode (based on vefaas-cli isViteSSR)"""
    # Check if scripts have ssr related commands
    for key, val in scripts.items():
        val_lower = (val or "").lower()
        if "vite-ssr" in val_lower or "vite build --ssr" in val_lower:
            return True

    # Check SSR dependencies
    deps = {**pkg.get("dependencies", {}), **pkg.get("devDependencies", {})}
    ssr_deps = ["vite-plugin-ssr", "vike", "@vitejs/plugin-react-ssr"]
    if any(dep in deps for dep in ssr_deps):
        return True

    # Check vite.config for ssr config
    vite_config_files = ["vite.config.js", "vite.config.ts", "vite.config.mjs", "vite.config.cjs"]
    for config_file in vite_config_files:
        content = _read_text(os.path.join(root, config_file))
        if content:
            if re.search(r"ssr\s*:\s*\{", content) or re.search(r"ssr\s*:\s*true", content):
                return True

    return False


def _is_astro_ssr(root: str) -> bool:
    """Detect if Astro is in SSR mode"""
    config_files = ["astro.config.js", "astro.config.ts", "astro.config.mjs", "astro.config.cjs", "astro.config.cts"]
    for config_file in config_files:
        content = _read_text(os.path.join(root, config_file))
        if content:
            if re.search(r"output\s*:\s*['\"]server['\"]", content):
                return True
            if re.search(r"adapter\s*:\s*", content):
                return True
    return False


# ==================== Python Detection ====================

def _detect_python(root: str) -> Optional[DetectionResult]:
    """Detect Python project"""
    has_py = (
        _exists(os.path.join(root, "requirements.txt")) or
        _exists(os.path.join(root, "pyproject.toml")) or
        _exists(os.path.join(root, "Pipfile")) or
        any(f.endswith(".py")
            for f in os.listdir(root) if os.path.isfile(os.path.join(root, f)))
    )

    if not has_py:
        return None

    # Read dependency info
    req_content = _read_text(os.path.join(root, "requirements.txt")) or ""
    pyproj_content = _read_text(os.path.join(root, "pyproject.toml")) or ""
    deps_blob = f"{req_content}\n{pyproj_content}".lower()

    is_fastapi = "fastapi" in deps_blob or "uvicorn" in deps_blob
    is_flask = "flask" in deps_blob
    is_django = "django" in deps_blob
    is_streamlit = "streamlit" in deps_blob

    # Detect package manager
    pm = _detect_python_package_manager(root)
    run_prefix = _get_python_run_prefix(pm)
    port = _detect_python_port(root) or 8000

    # Detect entrypoint file
    main_file = _find_python_entrypoint(root)
    default_entry = os.path.basename(main_file) if main_file else "main.py"

    # Generate start command
    has_uvicorn = "uvicorn" in deps_blob
    has_gunicorn = "gunicorn" in deps_blob

    if is_streamlit:
        start_cmd = f"{run_prefix} streamlit run {default_entry} --server.port ${{PORT:-{port}}} --server.address 0.0.0.0".strip()
    elif is_fastapi:
        if has_uvicorn:
            wsgi = _determine_python_wsgi(root, main_file, "fastapi")
            if wsgi:
                start_cmd = f"{run_prefix} uvicorn {wsgi} --host 0.0.0.0 --port ${{PORT:-{port}}}".strip()
            else:
                start_cmd = f"{run_prefix} python {default_entry}".strip()
        else:
            start_cmd = f"{run_prefix} python {default_entry}".strip()
    elif is_flask:
        wsgi = _determine_python_wsgi(root, main_file, "flask")
        if wsgi and has_gunicorn:
            start_cmd = f"{run_prefix} gunicorn {wsgi} --bind :{port}".strip()
        else:
            start_cmd = f"{run_prefix} python {default_entry}".strip()
    elif is_django:
        if has_gunicorn:
            start_cmd = f"{run_prefix} gunicorn project.wsgi:application --bind :{port}".strip()
        else:
            start_cmd = f"{run_prefix} python manage.py runserver 0.0.0.0:{port}".strip(
            )
    else:
        start_cmd = f"{run_prefix} python {default_entry}".strip()

    # Python version detection
    py_version = _detect_python_version(root)
    runtime = f"native-python{_ensure_supported_py_version(py_version)}/v1"

    # Install command
    install_cmd = _resolve_python_install_command(root)

    return DetectionResult(
        install_command=install_cmd,
        build_command="",
        output_path="./",
        start_command=start_cmd,
        port=port,
        runtime=runtime,
        framework="streamlit" if is_streamlit else ("fastapi" if is_fastapi else (
            "flask" if is_flask else ("django" if is_django else ""))),
        is_static=False,
    )


def _detect_python_package_manager(root: str) -> str:
    """Detect Python package manager"""
    if _exists(os.path.join(root, "uv.lock")):
        return "uv"
    pyproj = _read_text(os.path.join(root, "pyproject.toml")) or ""
    if "[tool.poetry]" in pyproj:
        return "poetry"
    if "[tool.pdm]" in pyproj:
        return "pdm"
    if _exists(os.path.join(root, "Pipfile")):
        return "pipenv"
    return "pip"


def _get_python_run_prefix(pm: str) -> str:
    """Get Python run prefix"""
    prefixes = {
        "uv": "UV_PROJECT_ENVIRONMENT=/tmp/.venv uv run",
        "poetry": "POETRY_VIRTUALENVS_PATH=/tmp/.venv poetry run",
        "pipenv": "WORKON_HOME=/tmp/.venv pipenv run",
        "pdm": "PDM_VENV_PATH=/tmp/.venv pdm run",
    }
    return prefixes.get(pm, "")


def _find_python_entrypoint(root: str) -> Optional[str]:
    """Find Python entrypoint file"""
    common_names = ["main.py", "app.py", "run.py",
                    "server.py", "wsgi.py", "asgi.py", "manage.py"]

    for name in common_names:
        path = os.path.join(root, name)
        if _exists(path):
            content = _read_text(path) or ""
            if "FastAPI(" in content or "Flask(" in content:
                return path

    # Fallback to first found common entry
    for name in common_names:
        path = os.path.join(root, name)
        if _exists(path):
            return path

    return None


def _determine_python_wsgi(root: str, entry_file: Optional[str], framework: str) -> Optional[str]:
    """Determine Python WSGI path"""
    if not entry_file:
        return None

    content = _read_text(entry_file)
    if not content:
        return None

    ctor = "FastAPI" if framework == "fastapi" else "Flask"
    match = re.search(rf"(\w+)\s*=\s*{ctor}\(", content)
    if not match:
        return None

    var_name = match.group(1)
    rel = os.path.relpath(entry_file, root)
    module = rel.replace(".py", "").replace(os.sep, ".")

    return f"{module}:{var_name}"


def _detect_python_port(root: str) -> Optional[int]:
    """Detect Python port"""
    # Detect from entry files
    entry_files = ["main.py", "app.py", "run.py", "server.py"]
    for name in entry_files:
        content = _read_text(os.path.join(root, name))
        if content:
            match = re.search(
                r"port[\"']?\s*[=:]\s*(\d{4,5})", content, re.IGNORECASE)
            if match:
                return int(match.group(1))
    return None


def _detect_python_version(root: str) -> str:
    """Detect Python version"""
    # Detect from pyproject.toml
    pyproj = _read_text(os.path.join(root, "pyproject.toml")) or ""
    match = re.search(r'python\s*[>=<~^]*\s*["\']?(\d+\.\d+)', pyproj)
    if match:
        return match.group(1)

    # Detect from .python-version
    pv = _read_text(os.path.join(root, ".python-version"))
    if pv:
        match = re.search(r"(\d+\.\d+)", pv.strip())
        if match:
            return match.group(1)

    return "3.12"  # Default


def _ensure_supported_py_version(version: str) -> str:
    """Ensure supported Python version"""
    supported = ["3.9", "3.10", "3.11", "3.12"]
    if version in supported:
        return version
    # Try to match major version
    for v in reversed(supported):
        if version.startswith(v.split(".")[0]):
            return v
    return "3.12"


def _resolve_python_install_command(root: str) -> str:
    """Resolve Python install command"""
    if _exists(os.path.join(root, "uv.lock")):
        if _exists(os.path.join(root, "requirements.txt")):
            return "uv pip install -r requirements.txt"
        return "uv sync"

    pyproj = _read_text(os.path.join(root, "pyproject.toml")) or ""
    if "[tool.poetry]" in pyproj:
        return "poetry install"
    if "[tool.pdm]" in pyproj:
        return "pdm install"
    if _exists(os.path.join(root, "Pipfile")):
        return "pipenv install"
    if _exists(os.path.join(root, "requirements.txt")):
        return "pip install -r requirements.txt"
    return "pip install ."


# ==================== Static Site Detection ====================

def _detect_static(root: str) -> Optional[DetectionResult]:
    """Detect static site"""
    root_index = os.path.join(root, "index.html")
    has_root_index = _exists(root_index)

    # Hugo detection
    hugo_files = ["hugo.toml", "hugo.json", "hugo.yaml"]
    has_hugo = any(_exists(os.path.join(root, f)) for f in hugo_files)

    # MkDocs detection
    has_mkdocs = _exists(os.path.join(root, "mkdocs.yml"))

    # Build output directory detection
    dist_index = os.path.join(root, "dist", "index.html")
    build_index = os.path.join(root, "build", "index.html")
    public_index = os.path.join(root, "public", "index.html")
    has_built_static = any(_exists(p)
                           for p in [dist_index, build_index, public_index])

    matched = has_root_index or has_hugo or has_mkdocs or has_built_static
    if not matched:
        return None

    # Determine output directory
    if _exists(dist_index):
        output_path = "dist"
    elif _exists(build_index):
        output_path = "build"
    elif _exists(public_index):
        output_path = "public"
    else:
        output_path = "./"

    # Determine framework
    framework = ""
    if has_hugo:
        framework = "hugo"
    elif has_mkdocs:
        framework = "mkdocs"

    return DetectionResult(
        install_command="",
        build_command="",
        output_path=output_path,
        start_command="caddy run --config DefaultCaddyFile --adapter caddyfile",
        port=8000,
        runtime="native-node20/v1",
        framework=framework,
        is_static=True,
    )
