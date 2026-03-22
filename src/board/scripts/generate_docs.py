import os
import sys
import importlib.util
import shutil
from board.board import Board
from board.svg import board_to_svg
from board.testing import get_captured_board, Scenario

def main():
    test_dir = "tests/board"
    # Root folder for all SVG clutter in this test category
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

    # Re-initialize the consolidated assets root
    if os.path.exists(assets_root):
        shutil.rmtree(assets_root)
    os.makedirs(assets_root, exist_ok=True)
    
    # Ensure the root assets folder is ignored by git
    gitignore_path = ".gitignore"
    ignore_entry = f"{test_dir}/{assets_root_name}/\n"
    with open(gitignore_path, "a+") as gf:
        gf.seek(0)
        content = gf.read()
        if ignore_entry not in content:
            gf.write(ignore_entry)

    test_files = [f for f in os.listdir(test_dir) if f.startswith("test_") and f.endswith(".py")]
    test_files.sort()

    for test_file in test_files:
        module_name = test_file[:-3]
        module_path = os.path.join(test_dir, test_file)
        md_file = os.path.join(test_dir, f"{module_name}.md")
        
        # Subdirectory for this specific module's SVGs (only created if needed)
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

        # Now we know we have scenarios, so create the assets subdir
        os.makedirs(module_assets_dir, exist_ok=True)

        md_content = [f"# {module_name.replace('_', ' ').title()}\n"]
        
        # Sort by Scenario ID
        functions.sort(key=lambda f: f._scenario.id)

        for func in functions:
            s: Scenario = func._scenario
            
            # Run the test to capture the board
            try:
                func()
            except Exception as e:
                print(f"Warning: Test {s.id} ({func.__name__}) failed during doc generation: {e}")
            
            board = get_captured_board() or Board()
            
            svg_filename = f"{func.__name__}.svg"
            svg_path = os.path.join(module_assets_dir, svg_filename)
            
            with open(svg_path, "w") as f:
                f.write(board_to_svg(board))

            md_content.append(f"## [{s.id}] {s.name}")
            md_content.append(f"**Test**: `{func.__name__}`")
            md_content.append(f"\n**Description**:\n{s.description}")
            md_content.append(f"\n**Pass Condition (Boolean Check)**:\n{s.pass_condition}")
            md_content.append(f"\n<img src='{assets_root_name}/{module_name}/{svg_filename}' width='600'>\n")
            
        with open(md_file, "w") as f:
            f.write("\n".join(md_content))
        print(f"Generated {md_file} ({len(functions)} scenarios in {assets_root_name}/{module_name}/)")

if __name__ == "__main__":
    main()
