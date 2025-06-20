# veFaaS Browser MCP Server

veFaaS Browser MCP server 为用户提供各种浏览器原子化操作，满足用户对浏览器、网页元素、键盘、表单、标签页、截图、PDF 生成等的细粒度管理和操作需求。

| | |
|------|------|
| 版本 | 0.0.26 |
| 描述 | veFaaS Browser MCP server 为用户提供各种浏览器原子化操作 |
| 分类 | 开发者工具 |
| 标签 | veFaaS，函数服务，Browser，浏览器 |

## Tools

本 MCP Server 产品提供以下 Tools (工具/能力):

### Tool 1: create_browser_task

#### 类型

互动类工具

#### 详细描述

发起浏览器操作任务

### Tool 2: browser_snapshot

#### 类型

互动类工具

#### 详细描述

捕获页面结构以进行自动化。

* **参数**: 无

### Tool 3: browser_click

#### 类型

互动类工具

#### 详细描述

点击网页元素。

* **参数**:
  * `element`: 元素描述
  * `ref`: 元素引用

### Tool 4: browser_drag

#### 类型

互动类工具

#### 详细描述

执行拖放操作。

* **参数**:
  * `startElement`: 源元素描述
  * `startRef`: 源元素引用
  * `endElement`: 目标元素描述
  * `endRef`: 目标元素引用

### Tool 5: browser_hover

#### 类型

互动类工具

#### 详细描述

将鼠标悬停在元素上。

* **参数**:
  * `element`: 元素描述
  * `ref`: 元素引用

### Tool 6: browser_type

#### 类型

互动类工具

#### 详细描述

在字段中输入文本。

* **参数**:
  * `element`: 元素描述
  * `ref`: 元素引用
  * `text`: 要输入的文本
  * `submit`: 输入后提交
  * `slowly`: 逐字符输入

### Tool 7: browser_select_option

#### 类型

互动类工具

#### 详细描述

选择下拉菜单选项。

* **参数**:
  * `element`: 元素描述
  * `ref`: 元素引用
  * `values`: 要选择的选项

### Tool 8: browser_press_key

#### 类型

互动类工具

#### 详细描述

触发键盘按键。

* **参数**:
  * `key`: 按键名称或字符

### Tool 9: browser_wait_for

#### 类型

互动类工具

#### 详细描述

等待条件满足。

* **参数**:
  * `time`: 等待秒数
  * `text`: 等待出现的文本
  * `textGone`: 等待消失的文本

### Tool 10: browser_file_upload

#### 类型

互动类工具

#### 详细描述

上传文件。

* **参数**:
  * `paths`: 要上传的文件路径

### Tool 11: browser_handle_dialog

#### 类型

互动类工具

#### 详细描述

管理浏览器对话框。

* **参数**:
  * `accept`: 接受对话框
  * `promptText`: 提示文本

### Tool 12: browser_navigate

#### 类型

导航类工具

#### 详细描述

打开指定 URL。

* **参数**:
  * `url`: 目标 URL

### Tool 13: browser_navigate_back

#### 类型

导航类工具

#### 详细描述

返回上一页。

* **参数**: 无

### Tool 14: browser_navigate_forward

#### 类型

导航类工具

#### 详细描述

前进到下一页。

* **参数**: 无

### Tool 15: browser_take_screenshot

#### 类型

资源类工具

#### 详细描述

捕获页面图像。

* **参数**:
  * `raw`: 无压缩图像
  * `filename`: 保存位置
  * `element`: 要捕获的元素
  * `ref`: 元素引用

### Tool 16: browser_pdf_save

#### 类型

资源类工具

#### 详细描述

将页面导出为 PDF。

* **参数**:
  * `filename`: 保存位置

### Tool 17: browser_network_requests

#### 类型

资源类工具

#### 详细描述

列出网络活动。

* **参数**: 无

### Tool 18: browser_console_messages

#### 类型

资源类工具

#### 详细描述

显示控制台输出。

* **参数**: 无

### Tool 19: browser_install

#### 类型

工具类工具

#### 详细描述

设置浏览器环境。

* **参数**: 无

### Tool 20: browser_close

#### 类型

工具类工具

#### 详细描述

退出当前页面。

* **参数**: 无

### Tool 21: browser_resize

#### 类型

工具类工具

#### 详细描述

更改窗口尺寸。

* **参数**:
  * `width`: 窗口宽度
  * `height`: 窗口高度

### Tool 22: browser_tab_list

#### 类型

标签页类工具

#### 详细描述

显示打开的标签页。

* **参数**: 无

### Tool 23: browser_tab_new

#### 类型

标签页类工具

#### 详细描述

创建新标签页。

* **参数**:
  * `url`: 初始 URL

### Tool 24: browser_tab_select

#### 类型

标签页类工具

#### 详细描述

切换活动标签页。

* **参数**:
  * `index`: 标签页位置

### Tool 25: browser_tab_close

#### 类型

标签页类工具

#### 详细描述

删除标签页。

* **参数**:
  * `index`: 要关闭的标签页

### Tool 26: browser_generate_playwright_test

#### 类型

测试类工具

#### 详细描述

创建自动化测试。

* **参数**:
  * `name`: 测试标识符
  * `description`: 测试目的
  * `steps`: 测试步骤

### Tool 27: browser_screen_capture

#### 类型

视觉模式工具

#### 详细描述

获取视觉快照。

* **参数**: 无

### Tool 28: browser_screen_move_mouse

#### 类型

视觉模式工具

#### 详细描述

定位光标。

* **参数**:
  * `element`: 元素描述
  * `x`: 水平位置
  * `y`: 垂直位置

### Tool 29: browser_screen_click

#### 类型

视觉模式工具

#### 详细描述

在坐标处点击。

* **参数**:
  * `element`: 元素描述
  * `x`: 水平位置
  * `y`: 垂直位置

### Tool 30: browser_screen_drag

#### 类型

视觉模式工具

#### 详细描述

在点之间拖动。

* **参数**:
  * `element`: 元素描述
  * `startX` / `startY`: 起始位置
  * `endX` / `endY`: 结束位置

### Tool 31: browser_screen_type

#### 类型

视觉模式工具

#### 详细描述

在光标处输入文本。

* **参数**:
  * `text`: 要输入的文本
  * `submit`: 输入后按回车

## 可适配平台  

Python, Cursor, Claude macOS App, Trae

## 使用方式

### 调用本地默认浏览器

```json
{
  "mcpServers": {
    "vefaas-browser": {
      "command": "npx",
      "args": [
        "@faas-mcp/browser@latest"
      ]
    }
  }
}
```

### 调用其他浏览器（如 veFaaS 浏览器 session 池管理提供的）

```json
{
  "mcpServers": {
    "vefaas-browser": {
      "command": "npx",
      "args": [
        "@faas-mcp/browser@latest",
        "--cdp-endpoint",
        "ws://xxxxxxxx.apigateway-cn-beijing.volceapi.com/v0.1/browsers/yyyyyyyyzzzzzfaked"
      ]
    }
  }
}
```

如果使用 veFaaS，需要[开通产品](https://console.volcengine.com/vefaas)。

## License

volcengine/mcp-server is licensed under the [MIT](../..//LICENSE).
