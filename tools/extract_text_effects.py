"""
从 data.ts 文件提取所有花字效果并生成 Python 映射表
"""
import re
import json


def extract_text_effects_from_data_ts(file_path: str) -> dict:
    """
    从 data.ts 文件中提取所有花字效果
    
    Args:
        file_path: data.ts 文件路径
    
    Returns:
        花字效果映射字典 {title: {"effect_id": ..., "resource_id": ..., "is_vip": ...}}
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 使用正则表达式匹配所有花字对象
    # 匹配 common_attr 块
    pattern = r'common_attr:\s*\{([^}]+(?:\{[^}]*\}[^}]*)*)\}'
    
    text_effects = {}
    
    for match in re.finditer(pattern, content, re.DOTALL):
        block = match.group(1)
        
        # 提取 effect_id
        effect_id_match = re.search(r'effect_id:\s*["\'](\d+)["\']', block)
        if not effect_id_match:
            continue
        effect_id = effect_id_match.group(1)
        
        # 提取 title
        title_match = re.search(r'title:\s*["\']([^"\']+)["\']', block)
        if not title_match:
            continue
        title = title_match.group(1)
        
        # 提取 is_vip 信息 (从 business_info.json_str 中)
        is_vip = False
        json_str_match = re.search(r'json_str:\s*["\']({[^}]+})["\']', block)
        if json_str_match:
            try:
                business_info = json.loads(json_str_match.group(1).replace('\\"', '"'))
                is_vip = business_info.get('is_vip', False)
            except:
                pass
        
        # 添加到字典
        text_effects[title] = {
            "resource_id": effect_id,
            "effect_id": effect_id,
            "name": title,
            "is_vip": is_vip
        }
    
    return text_effects


def generate_python_mapping(text_effects: dict) -> str:
    """
    生成 Python 格式的映射表代码
    
    Args:
        text_effects: 花字效果字典
    
    Returns:
        Python 代码字符串
    """
    code_lines = [
        "# 从 data.ts 自动生成的花字效果映射表",
        "# 格式：{effect_name: {\"resource_id\": \"...\", \"effect_id\": \"...\", \"name\": \"...\", \"is_vip\": ...}}",
        "TEXT_EFFECT_MAP = {",
    ]
    
    # 按名称排序
    sorted_effects = sorted(text_effects.items(), key=lambda x: x[0])
    
    for i, (name, data) in enumerate(sorted_effects):
        is_last = i == len(sorted_effects) - 1
        comma = "," if not is_last else ""
        
        code_lines.append(f'    "{name}": {{')
        code_lines.append(f'        "resource_id": "{data["resource_id"]}",')
        code_lines.append(f'        "effect_id": "{data["effect_id"]}",')
        code_lines.append(f'        "name": "{data["name"]}",')
        code_lines.append(f'        "is_vip": {data["is_vip"]}')  # Use Python boolean directly
        code_lines.append(f"    }}{comma}")
    
    code_lines.append("}")
    
    return "\n".join(code_lines)


def main():
    # 读取 data.ts 文件
    data_file = "d:\\code\\GitHub\\capcut-mate\\data.ts"
    
    print("=" * 60)
    print("开始从 data.ts 提取花字效果...")
    print("=" * 60)
    
    # 提取花字效果
    text_effects = extract_text_effects_from_data_ts(data_file)
    
    print(f"\n成功提取 {len(text_effects)} 个花字效果")
    
    # 显示前 20 个效果
    print("\n前 20 个花字效果:")
    for i, (name, data) in enumerate(list(text_effects.items())[:20]):
        vip_tag = " [VIP]" if data["is_vip"] else ""
        print(f"  {i+1}. {name}{vip_tag} (ID: {data['effect_id']})")
    
    # 统计 VIP 和免费数量
    vip_count = sum(1 for data in text_effects.values() if data["is_vip"])
    free_count = len(text_effects) - vip_count
    
    print(f"\nVIP 效果数量：{vip_count}")
    print(f"免费效果数量：{free_count}")
    
    # 生成 Python 映射代码
    print("\n生成 Python 映射代码...")
    python_code = generate_python_mapping(text_effects)
    
    # 保存到文件
    output_file = "d:\\code\\GitHub\\capcut-mate\\text_effect_map_generated.py"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(python_code)
    
    print(f"\n映射表已保存到：{output_file}")
    print("=" * 60)
    
    return text_effects


if __name__ == "__main__":
    main()
