# Find 资源 - 搜索功能

Find 资源提供搜索功能，包括文本搜索、文件搜索和符号搜索。

## 📋 方法列表

1. [text](#1-text) - 在文件中搜索文本
2. [files](#2-files) - 搜索文件名
3. [symbols](#3-symbols) - 搜索工作区符号

---

## 📖 详细文档

### 1. text

在文件中搜索文本。

**参数:**
- `query` (str) - 搜索查询字符串
- `path` (Optional[str]) - 可选的搜索路径（限制搜索范围）
- `case_sensitive` (bool) - 是否区分大小写
- `whole_word` (bool) - 是否匹配整个单词
- `regex` (bool) - 是否使用正则表达式
- `max_results` (Optional[int]) - 最大结果数量

**返回值:**
- `List[Dict[str, Any]]` - 搜索结果列表，每个结果包含文件路径、行号、匹配内容等

**示例:**
```python
# 搜索文本
results = client.find.text("TODO")
for result in results:
    print(f"{result['path']}:{result['line']}: {result['text']}")

# 使用正则表达式搜索
results = client.find.text(r"function\s+\w+", regex=True)

# 区分大小写搜索
results = client.find.text("TODO", case_sensitive=True)

# 限制搜索范围
results = client.find.text("TODO", path="/src")
```

---

### 2. files

搜索文件名。

**参数:**
- `query` (str) - 文件名搜索查询（支持模糊匹配）
- `path` (Optional[str]) - 可选的搜索路径
- `max_results` (Optional[int]) - 最大结果数量

**返回值:**
- `List[Dict[str, Any]]` - 匹配的文件列表

**示例:**
```python
# 搜索文件
files = client.find.files("*.py")
for file in files:
    print(file['path'])

# 模糊搜索
files = client.find.files("readme")

# 限制搜索范围
files = client.find.files("*.py", path="/src")
```

---

### 3. symbols

搜索工作区符号。

搜索代码中的符号（函数、类、变量等）。

**参数:**
- `query` (str) - 符号名称搜索查询
- `max_results` (Optional[int]) - 最大结果数量

**返回值:**
- `List[Dict[str, Any]]` - 符号列表，每个符号包含名称、类型、位置等信息

**示例:**
```python
# 搜索函数
symbols = client.find.symbols("main")
for symbol in symbols:
    print(f"{symbol['name']} ({symbol['kind']}) in {symbol['path']}")

# 搜索类
symbols = client.find.symbols("MyClass")
```

---

## 💡 使用建议

1. **文本搜索** - 使用 `text()` 在代码中搜索特定文本
2. **文件搜索** - 使用 `files()` 查找特定文件
3. **符号搜索** - 使用 `symbols()` 查找函数、类等定义

## 🔗 相关资源

- [File 资源](file.md) - 文件操作
- [LSP 资源](lsp.md) - 语言服务器协议
