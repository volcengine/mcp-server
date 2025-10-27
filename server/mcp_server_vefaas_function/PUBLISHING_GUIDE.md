# PyPI 发布指南

本指南详细说明如何将 mcp-server-vefaas-function 包发布到 PyPI。

## 前置条件

在发布前，请确保您已完成以下准备工作：

1. 安装必要的工具：
   ```bash
   pip install build twine
   ```

2. 在 [PyPI](https://pypi.org/) 上注册账号

3. 确保项目文件完整：
   - `pyproject.toml`（已配置）
   - `README.md`（已存在）
   - `LICENSE`（已添加）
   - `setup.py`（已添加，用于兼容性）

## 发布步骤

### 1. 清理构建目录（如存在）

```bash
rm -rf dist build *.egg-info
```

### 2. 构建分发包

```bash
python -m build
```

这将创建两个文件在 `dist` 目录中：
- 一个源码分发包（.tar.gz）
- 一个二进制分发包（.whl）

### 3. 验证分发包

```bash
python -m twine check dist/*
```

确保没有任何警告或错误。

### 4. 上传到 PyPI

```bash
python -m twine upload dist/*
```

系统将提示您输入 PyPI 的用户名和密码。

### 5. 验证发布

发布成功后，可以通过以下方式验证：

1. 访问 `https://pypi.org/project/mcp-server-vefaas-function/` 查看包信息
2. 尝试安装包：
   ```bash
   pip install mcp-server-vefaas-function
   ```

## 更新版本号

当您需要发布新版本时，请按照以下步骤更新版本号：

1. 修改 `pyproject.toml` 文件中的 `version` 字段
2. 重复上述发布步骤

## 发布到测试环境

如果您想先在测试环境中验证，可以使用 TestPyPI：

```bash
python -m twine upload --repository testpypi dist/*
```

然后从 TestPyPI 安装测试：

```bash
pip install --index-url https://test.pypi.org/simple/ mcp-server-vefaas-function
```

## 注意事项

1. 确保版本号符合语义化版本规范（SemVer）
2. 更新 `README.md` 中的文档，反映新版本的变化
3. 检查依赖项的版本约束，确保兼容性
4. 确保代码质量，最好在发布前运行测试
5. 保护好您的 PyPI 账号凭证

祝您发布顺利！