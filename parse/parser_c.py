import clang.cindex
import json
import os
import sys
sys.path.append("/home/llh/mydataset/util")
from folder_utils import FolderUtils

def node_to_dict(node):
    """
    将 clang 的节点转换为类似 Py150 数据集格式的字典。
    """
    # 创建一个新的节点字典
    node_dict = {"type": node.kind.name}
    
    # 获取节点的值（例如变量、数字、字符串等）
    if node.kind == clang.cindex.CursorKind.FUNCTION_DECL:
        node_dict["value"] = node.spelling
    elif node.kind == clang.cindex.CursorKind.INTEGER_LITERAL:
        tokens = list(node.get_tokens())
        if tokens:
            node_dict["value"] = tokens[0].spelling  # 例如 "7"
    elif node.kind == clang.cindex.CursorKind.STRING_LITERAL:
        node_dict["value"] = node.spelling
    elif node.kind == clang.cindex.CursorKind.DECL_REF_EXPR:
        node_dict["value"] = node.spelling
    elif node.kind == clang.cindex.CursorKind.VAR_DECL:
        node_dict["value"] = node.spelling
    elif node.kind == clang.cindex.CursorKind.FIELD_DECL:
        node_dict["value"] = node.spelling

    # 递归获取子节点，并按 Py150 格式返回
    children = []
    for child in node.get_children():

        children.append(node_to_dict(child))
    
    if children:
        node_dict["children"] = children
    
    return node_dict

def traverse(node):
    """
    将 AST 树转化为 JSON 格式的字典结构。
    """
    # 基础结构
    node_dict = {
        "type": str(node.kind),  # 节点类型
        "value": node.spelling if node.spelling else None,  # 节点值（如果存在）
        "children": []  # 存储子节点
    }

    # 遍历子节点并递归调用 traverse
    for child in node.get_children():
        node_dict["children"].append(traverse(child))
    
    return node_dict



def parse_c_file(file_path):
    """
    解析 C 文件，返回抽象语法树的 JSON 格式
    """

    #删除源文件的头文件引用
    strings = file_path.split(".")

    new_file_path = strings[0]+"without_include.c"


    FolderUtils.remove_includes_from_c_file(file_path,new_file_path)
    #将源文件编译为json类型的AST
    index = clang.cindex.Index.create()
    args = ['-Xclang', '-load', '-Xclang', 'clang-frontend', '-parse-ignore-headers']
    translation_unit = index.parse(new_file_path, args=args)
    root = translation_unit.cursor
    return traverse(root)


def flatten_ast(ast):
    result = []
    def flatten(node):
        # 当前节点的索引
        idx = len(result)
        result.append({
            "type": node["type"],
            "value": node["value"],
            "children": []  
        })
        
        # 遍历子节点，递归填充
        for child in node.get("children", []):
            child_idx = flatten(child)  # 获取子节点的索引
            result[idx]["children"].append(child_idx)  # 将子节点索引添加到当前节点的 children
        return idx
    
    # 从根节点开始
    flatten(ast[0])
    return result
        


if __name__ == "__main__":
    file_path = "/home/llh/mydataset/parse/test_parse_c.c" 
    json_ast = parse_c_file(file_path)
    
    #如果第一个节点是CursorKind.TRANSLATION_UNIT类型，则删除第一个节点
    if(json_ast.get("type") == "CursorKind.TRANSLATION_UNIT"):
        json_ast = json_ast.get("children",[])
    
    formatted_data = json.dumps(json_ast, indent=2, ensure_ascii=False)
    print(formatted_data)
    # 转换AST类型为索引格式
    indexed_ast = flatten_ast(json_ast)

    print(json.dumps(indexed_ast, indent=2))


