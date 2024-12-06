import clang.cindex
import json

# 初始化 libclang
clang.cindex.Config.set_library_path("/path/to/your/clang/lib")  # 配置libclang路径
index = clang.cindex.Index.create()

# 解析 C 文件
translation_unit = index.parse("hello.c")

def node_to_dict(node):
    """
    将 clang 的节点转换为字典结构，符合 Py150 数据集格式
    """
    node_dict = {"type": node.kind.spelling}
    if node.kind == clang.cindex.CursorKind.FunctionDecl:
        node_dict["value"] = node.spelling
    elif node.kind == clang.cindex.CursorKind.INTEGER_LITERAL:
        node_dict["value"] = node.spelling
    elif node.kind == clang.cindex.CursorKind.STRING_LITERAL:
        node_dict["value"] = node.spelling
    elif node.kind == clang.cindex.CursorKind.DECL_REF_EXPR:
        node_dict["value"] = node.spelling

    # 递归获取子节点
    children = []
    for child in node.get_children():
        children.append(node_to_dict(child))
    if children:
        node_dict["children"] = children
    return node_dict

# 从根节点开始
root = translation_unit.cursor
ast_dict = node_to_dict(root)

# 输出 AST
print(json.dumps(ast_dict, indent=2))
