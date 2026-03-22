import os
import sys
import importlib.util
import shutil
from board.board import Board
from board.svg import board_to_svg
from board.testing import get_captured_board, Scenario

def main():
    test_dir = "tests/board"
    assets_root_name = "assets"
    assets_root = os.path.join(test_dir, assets_root_name)
    
    # 1. Cleanup old documentation and assets in the root
    print(f"Cleaning up old documentation and root assets in {test_dir}...")
    for f in os.listdir(test_dir):
        file_path = os.path.join(test_dir, f)
        if f.endswith(".svg"):
            os.remove(file_path)
        elif f.endswith(".md") and f != "README.md":
            os.remove(file_path)
        elif f.endswith("_assets") and os.path.isdir(file_path):
            shutil.rmtree(file_path)
        elif f == "visuals" and os.path.isdir(file_path):
            shutil.rmtree(file_path)

    if os.path.exists(assets_root):
        shutil.rmtree(assets_root)
    os.makedirs(assets_root, exist_ok=True)
    
    test_files = [f for f in os.listdir(test_dir) if f.startswith("test_") and f.endswith(".py")]
    test_files.sort()

    global_id_counter = 1

    for test_file in test_files:
        module_name = test_file[:-3]
        module_path = os.path.join(test_dir, test_file)
        md_file = os.path.join(test_dir, f"{module_name}.md")
        
        module_assets_dir = os.path.join(assets_root, module_name)
        
        spec = importlib.util.spec_from_file_location(module_name, module_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        functions = []
        for name in dir(module):
            attr = getattr(module, name)
            if hasattr(attr, "_scenario"):
                functions.append(attr)
        
        if not functions:
            print(f"Skipping {test_file} (no @scenario decorators found)")
            continue

        os.makedirs(module_assets_dir, exist_ok=True)
        md_content = [f"# {module_name.replace('_', ' ').title()}\n"]
        
        # Sort functions by their name to have stable discovery order
        functions.sort(key=lambda f: f.__name__)

        for func in functions:
            s: Scenario = func._scenario
            
            # Autogenerate ID if not provided
            test_id = s.id if s.id else f"IC-{global_id_counter:03d}"
            global_id_counter += 1
            
            try:
                func()
            except Exception as e:
                print(f"Warning: Test {test_id} ({func.__name__}) failed during doc generation: {e}")
            
            board = get_captured_board() or Board()
            
            svg_filename = f"{func.__name__}.svg"
            svg_path = os.path.join(module_assets_dir, svg_filename)
            
            with open(svg_path, "w") as f:
                f.write(board_to_svg(board))

            md_content.append(f"## [{test_id}] {s.name}")
            md_content.append(f"**Test**: `{func.__name__}`")
            md_content.append(f"\n**Description**:\n{s.description}")
            md_content.append(f"\n**Pass Condition (Boolean Check)**:\n{s.pass_condition}")
            md_content.append(f"\n<img src='{assets_root_name}/{module_name}/{svg_filename}' width='600'>\n")
            
        with open(md_file, "w") as f:
            f.write("\n".join(md_content))
        print(f"Generated {md_file} ({len(functions)} scenarios)")

if __name__ == "__main__":
    main()
