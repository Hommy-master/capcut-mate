import os
import shutil
import sys

# 添加父目录到系统路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 从example.py中导入必要的函数
from example import add_video_impl, add_effect, save_draft_impl

def example_capcut_effect():
    """Test service for adding effects"""
    # draft_folder = "/Users/sunguannan/Movies/JianyingPro/User Data/Projects/com.lveditor.draft"
    draft_folder = "/Users/sunguannan/Movies/CapCut/User Data/Projects/com.lveditor.draft"
    
    print("\nTest: Adding effects")
    # First add video track
    image_result = add_video_impl(
        video_url="https://pan.superbed.cn/share/1nbrg1fl/jimeng_daweidai.mp4",
        start=0,
        end=3.0,
        target_start=0,
        width=1080,
        height=1920
    )
    print(f"Video added successfully! {image_result['output']['draft_id']}")
    image_result = add_video_impl(
        video_url="https://pan.superbed.cn/share/1nbrg1fl/jimeng_daweidai.mp4",
        draft_id=image_result['output']['draft_id'],
        start=0,
        end=3.0,
        target_start=3,
    )
    print(f"Video added successfully! {image_result['output']['draft_id']}")
    
    # Then add effect
    effect_result = add_effect(
        effect_type="Like",
        effect_category="character",  # Explicitly specify as character effect
        start=3,
        end=6,
        draft_id=image_result['output']['draft_id'],
        track_name="effect_01"
    )
    print(f"Effect adding result: {effect_result}")
    print(save_draft_impl(effect_result['output']['draft_id'], draft_folder))
    
    source_folder = os.path.join(os.getcwd(), effect_result['output']['draft_id'])
    destination_folder = os.path.join(draft_folder, effect_result['output']['draft_id'])
    
    if os.path.exists(source_folder):
        print(f"Moving {effect_result['output']['draft_id']} to {draft_folder}")
        shutil.move(source_folder, destination_folder)
        print("Folder moved successfully!")
    else:
        print(f"Source folder {source_folder} does not exist")
    
    # Add log to prompt user to find the draft in CapCut
    print(f"\n===== IMPORTANT =====\nPlease open CapCut and find the draft named '{effect_result['output']['draft_id']}'\n=======================")
    
    # Return the first test result for subsequent operations (if any)
    return effect_result


if __name__ == "__main__":
    example_capcut_effect()