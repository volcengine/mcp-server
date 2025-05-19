import re
from copy import deepcopy
from typing import Any, Dict, List, Set, Optional

from fastmcp.utilities.logging import configure_logging, get_logger
from mcp.types import Tool
from pydantic import ValidationError

# 定义logger
logger = get_logger(__name__)
configure_logging("INFO")


# $ref 解析逻辑
def resolve_refs(swagger_dict: Dict[str, Any]) -> Dict[str, Any]:
    """
    递归解析Swagger字典中的所有内部 $ref 引用 (#/...)

    Args:
        swagger_dict: 原始 Swagger 文档字典

    Returns:
        展开所有 $ref 引用后的 Swagger 文档字典 (一个新的字典对象)
        如果解析失败则可能抛出 ValueError。

    注意：此函数返回一个新的字典，原始字典不会被修改。
    """
    # 用于缓存已解析的引用，避免重复解析和循环引用问题
    cache = {}
    # 用于检测循环引用，存储正在解析的 $ref 路径
    resolving_stack = set()

    def _resolve_node(node: Any) -> Any:
        """递归解析节点中的$ref"""
        if isinstance(node, list):
            # 递归处理列表中的每个元素
            # 使用列表推导式创建新列表，避免修改原列表
            return [_resolve_node(item) for item in node]

        if not isinstance(node, dict):
            # 基本类型或非字典对象，直接返回
            return node

        if "$ref" in node:
            ref_path = node["$ref"]
            if not isinstance(ref_path, str):
                logger.error(f"警告：发现非字符串类型的 $ref 值：{ref_path}，将忽略此 $ref。")
                # 处理字典中 $ref 之外的其他键
                result = {}
                for k, v in node.items():
                    if k != "$ref":
                        result[k] = _resolve_node(v)
                return result

            # 检查是否是内部引用
            if ref_path.startswith('#/'):
                cache_key = ref_path

                # 检查缓存
                if cache_key in cache:
                    # 从缓存返回深拷贝，防止后续修改影响缓存
                    return deepcopy(cache[cache_key])

                # 检查循环引用
                if ref_path in resolving_stack:
                    logger.error(f"警告：检测到循环引用: {ref_path}，将返回 null 或空对象以中断循环。")
                    # 可以返回 None, {}, 或者一个特定的错误标记对象
                    # 返回空字典可能比 None 更安全，避免后续处理 .get() 等方法出错
                    return {"$ref_cycle_detected": ref_path}

                # 将当前引用添加到解析栈
                resolving_stack.add(ref_path)

                #  查找引用目标
                parts = ref_path[2:].split('/')
                target = swagger_dict  # 从根开始查找
                try:
                    for part in parts:
                        # RFC 6901 JSON Pointer 反转义
                        part_unescaped = part.replace('~1', '/').replace('~0', '~')
                        if isinstance(target, list):
                            target = target[int(part_unescaped)]
                        elif isinstance(target, dict):
                            # 尝试数字键（用于 responses 等）和字符串键
                            if part_unescaped.isdigit() and int(part_unescaped) in target:
                                target = target[int(part_unescaped)]
                            elif part_unescaped in target:
                                target = target[part_unescaped]
                            else:
                                raise KeyError(f"路径部分 '{part_unescaped}' 在字典中未找到")
                        else:
                            raise TypeError(f"路径部分 '{part_unescaped}' 无法在非字典/列表类型中查找")
                except (KeyError, IndexError, ValueError, TypeError) as e:
                    # 查找失败，从解析栈中移除并抛出错误
                    resolving_stack.remove(ref_path)
                    raise ValueError(f"无法解析引用: {ref_path}, 错误: {e}") from e

                # 递归解析找到的目标
                resolved_target = _resolve_node(deepcopy(target))

                # 处理 $ref 同级的其他属性
                result = deepcopy(resolved_target)
                # 如果基础不是字典（例如 $ref 指向一个字符串或数字），则无法合并
                if isinstance(result, dict):
                    for k, v in node.items():
                        if k != "$ref":
                            # 对同级属性的值也进行递归解析
                            result[k] = _resolve_node(v)
                elif len(node) > 1:  # 如果 $ref 指向非对象，但同级还有其他属性
                    logger.error(f"警告：$ref '{ref_path}' 指向非对象类型，但同级存在其他属性，这些属性将被忽略。")

                # 缓存并返回结果
                cache[cache_key] = result
                # 从解析栈中移除
                resolving_stack.remove(ref_path)

                return result

            else:
                # 不支持外部引用或其他格式的 $ref，保留原样，但递归处理其子节点（如果它是对象）
                logger.error(f"警告：跳过不支持的外部或非标准 $ref: {ref_path}")
                result = {}
                for k, v in node.items():
                    # 保留 $ref 键本身，但递归处理其他值
                    if k == "$ref":
                        result[k] = v
                    else:
                        result[k] = _resolve_node(v)
                return result

        # 处理普通对象（没有 $ref 键）
        result = {}
        for k, v in node.items():
            result[k] = _resolve_node(v)
        return result

    # 从根节点开始解析，传入原始字典的深拷贝以确保原始字典不变
    return _resolve_node(deepcopy(swagger_dict))


#  ToolName 辅助函数
def sanitize_name(name: str) -> str:
    """
    清理名称，使其符合 mcp.types.Tool 对 name 字段的要求 (^[a-zA-Z0-9_]+$) 和长度限制 (1-64)。
    """
    # 移除开头/结尾的非允许字符
    name = re.sub(r'^[^a-zA-Z0-9_]+|[^a-zA-Z0-9_]+$', '', name)
    # 将中间的非允许字符序列替换为单个下划线
    name = re.sub(r'[^a-zA-Z0-9_]+', '_', name)

    # 确保名称不为空
    if not name:
        name = "unnamed_tool"

    # 检查长度限制
    if len(name) > 64:
        logger.error(f"警告：清理后的工具名称 '{name}' 超过 64 个字符，将被截断。")
        name = name[:64]
        # 确保截断后不会以下划线结尾
        while name.endswith('_') and len(name) > 1:
            name = name[:-1]
        # 如果截断后为空或只剩下下划线，则重置为默认值
        if not name or name == '_':
            name = "unnamed_tool"
        # 再次检查截断后的首字符是否有效（理论上不太可能，除非原名极特殊）
        if not re.match(r'^[a-zA-Z0-9_]', name):
            name = "unnamed_tool"

    # 最终检查，确保至少有一个有效字符
    if not re.match(r'^[a-zA-Z0-9_]+$', name):
        logger.error(f"警告：清理后的名称 '{name}' 仍然无效，将使用 'unnamed_tool'。")
        name = "unnamed_tool"

    return name


#  核心转换逻辑
def openapi_to_mcp_tools(openapi_spec: Optional[Dict[str, Any]]) -> List[Tool]:
    """
    从 OpenAPI v3 JSON 文件加载规范，解析 $ref，并将其转换为 MCP Tool 对象列表。

    Args:
        openapi_spec  swagger dict

    Returns:
        一个 mcp.types.Tool 对象列表。
    """
    tools: List[Tool] = []
    resolved_spec: Optional[Dict[str, Any]] = None
    # 1. 解析 $ref 引用
    try:
        resolved_spec = resolve_refs(openapi_spec)
    except Exception as e:
        raise e

    # 2. 将 OpenAPI 操作转换为 MCP Tools...
    paths = resolved_spec.get('paths', {})
    if not isinstance(paths, dict):
        logger.error("警告：解析后的规范中缺少 'paths' 键或其值不是字典。")
        return []

    valid_methods = {"get", "put", "post", "delete", "options", "head", "patch", "trace"}
    for path, path_item in paths.items():
        if not isinstance(path_item, dict):
            continue

        # 获取路径级别的参数
        path_level_params = path_item.get('parameters', [])
        if not isinstance(path_level_params, list):  # 添加检查
            logger.error(f"警告：路径 '{path}' 的 parameters 不是列表，已忽略。")
            path_level_params = []

        for method, operation in path_item.items():
            if method not in valid_methods or not isinstance(operation, dict):
                continue

            #  a. 确定工具名称
            raw_name = ""
            operation_id = operation.get('operationId')
            if operation_id and isinstance(operation_id, str):
                raw_name = operation_id
            else:
                # 回退名称生成
                sanitized_path = path.replace('/', '_').replace('{', '_').replace('}', '')
                # 移除路径开头的下划线（如果存在）
                if sanitized_path.startswith('_'):
                    sanitized_path = sanitized_path[1:]
                raw_name = f"{method}_{sanitized_path}"  # 使用下划线分隔

            tool_name = sanitize_name(raw_name)

            #  b. 确定工具描述
            description = operation.get('description', '') or operation.get('summary', '')
            if not description:  # 如果两者都为空或不存在
                description = f"API 调用: {method.upper()} {path}"
            if not isinstance(description, str):
                logger.error(f"警告：操作 {method.upper()} {path} 的描述不是字符串，将使用默认描述。")
                description = f"API 调用: {method.upper()} {path}"

            #  c/d/e. 构建参数模式
            tool_parameters_dict: Dict[str, Any] = {"type": "object", "properties": {}, "required": []}
            required_params_set: Set[str] = set()
            param_properties: Dict[str, Any] = {}

            # 合并路径级和操作级的参数
            operation_params = operation.get('parameters', [])
            if not isinstance(operation_params, list):  # 添加检查
                logger.error(f"警告：操作 {method.upper()} {path} 的 parameters 不是列表，已忽略。")
                operation_params = []

            # 确保参数列表中的每个元素都是字典
            all_params = [p for p in (path_level_params + operation_params) if isinstance(p, dict)]

            processed_param_names: Set[str] = set()

            # 反向迭代，优先处理操作级参数
            for param_def in reversed(all_params):
                # $ref 已被解析，直接使用字段
                param_name = param_def.get('name')
                param_in = param_def.get('in')

                # 跳过无效的、重复的或非 query/path 参数
                if not param_name or not isinstance(param_name, str) or \
                        not param_in or not isinstance(param_in, str) or \
                        param_name in processed_param_names or \
                        param_in not in ['path', 'query']:
                    continue

                param_schema = param_def.get('schema')
                if isinstance(param_schema, dict):
                    # 检查是否是循环引用占位符
                    if "$ref_cycle_detected" in param_schema:
                        logger.error(f"警告：参数 '{param_name}' 的 schema 指向一个循环引用，已跳过。")
                        continue

                    # 如果模式中没有描述，则从参数本身获取描述
                    if 'description' not in param_schema and param_def.get('description'):
                        param_schema['description'] = param_def.get('description')

                    param_properties[param_name] = param_schema
                    if param_def.get('required', False) or param_in == 'path':
                        required_params_set.add(param_name)
                    processed_param_names.add(param_name)
                else:
                    logger.error(f"警告：参数 '{param_name}' 缺少有效的 schema 定义（非字典），已跳过。")

            # 处理请求体 (仅 application/json)
            request_body = operation.get('requestBody')
            if isinstance(request_body, dict):
                # 检查是否是循环引用占位符
                if "$ref_cycle_detected" in request_body:
                    logger.error(f"警告：操作 {method.upper()} {path} 的 requestBody 指向一个循环引用，已跳过。")
                else:
                    content = request_body.get('content')
                    if isinstance(content, dict):
                        media_type = content.get('application/json')
                        if media_type is None:
                            media_type = content.get('application/x-www-form-urlencoded')
                        if isinstance(media_type, dict):
                            body_schema = media_type.get('schema')
                            if isinstance(body_schema, dict):
                                # 检查 schema 是否是循环引用占位符
                                if "$ref_cycle_detected" in body_schema:
                                    logger.error(
                                        f"警告：操作 {method.upper()} {path} 的 requestBody schema 指向一个循环引用，已跳过请求体合并。")
                                # 如果请求体模式是对象类型，则合并其属性
                                elif (body_schema.get('type') == 'object' and
                                      isinstance(body_schema.get('properties'), dict)):
                                    for prop_name, prop_schema in body_schema['properties'].items():
                                        if not isinstance(prop_name, str) or not isinstance(prop_schema, dict):
                                            logger.error(f"警告：请求体属性 '{prop_name}' 名称或 schema 无效，已跳过。")
                                            continue
                                        # 检查属性 schema 是否是循环引用占位符
                                        if "$ref_cycle_detected" in prop_schema:
                                            logger.error(
                                                f"警告：请求体属性 '{prop_name}' 的 schema 指向一个循环引用，已跳过。")
                                            continue
                                        if prop_name in param_properties:
                                            logger.error(
                                                f"警告：工具 '{tool_name}' 中存在名称冲突 '{prop_name}'。请求体属性将覆盖现有参数。")
                                        param_properties[prop_name] = prop_schema

                                    # 合并请求体模式中的必需字段
                                    body_required = body_schema.get('required', [])
                                    if isinstance(body_required, list):
                                        required_params_set.update(req for req in body_required if isinstance(req, str))

            #  完成参数模式
            if param_properties:
                tool_parameters_dict['properties'] = param_properties
            # 确保 required 列表中的项都在 properties 中
            valid_required = [req for req in sorted(list(required_params_set)) if req in param_properties]
            if valid_required:
                tool_parameters_dict['required'] = valid_required
            else:
                tool_parameters_dict.pop('required', None)  # 移除空的 required 列表

            #  f. 创建 Tool 实例
            try:
                tool_instance = Tool(
                    name=tool_name,
                    description=description,
                    inputSchema=tool_parameters_dict
                )
                tools.append(tool_instance)
            except ValidationError as e:
                logger.error(
                    f"\n警告：无法为 {method.upper()} {path} (尝试命名为 '{tool_name}') 创建 Tool 实例，因为参数验证失败:{e}")
            except Exception as e:
                logger.error(
                    f"\n警告：为 {method.upper()} {path} (尝试命名为 '{tool_name}') 创建 Tool 实例时发生意外错误: {e}")
    return tools
