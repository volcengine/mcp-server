.EXPORT_ALL_VARIABLES:

OUTPUT_DIR := output
ZIP_NAME := $(OUTPUT_DIR)/mcp-server-flink.zip
ZIP_DIRS := src tests
ZIP_FILES := pyproject.toml poetry.lock poetry.toml requirements.txt README.md run.sh pytest.ini

# 默认目标
package-function: zip

mcp-run-debug:
	npx @modelcontextprotocol/inspector poetry run mcp-server-flink

# 打包 ZIP 文件
zip:
	@echo "===> Building zip package to $(ZIP_NAME)"
	@mkdir -p $(OUTPUT_DIR)
	@rm -f $(ZIP_NAME)
	zip -r $(ZIP_NAME) $(ZIP_DIRS) $(ZIP_FILES)

clean:
	@echo "===> Cleaning output directory"
	rm -rf $(OUTPUT_DIR)

build:
	poetry update
	uv sync
	uv pip compile pyproject.toml -o requirements.txt