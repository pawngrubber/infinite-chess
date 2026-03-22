import os
import sys
import importlib.util
import shutil
from board.board import Board
from board.svg import board_to_svg
from board.testing import get_captured_board, Scenario

def main():
    test_dir = "tests/board"
    
    # 1. Cleanup old documentation in the root to avoid clutter
    print(f"Cleaning up old documentation and root SVGs in {test_dir}...")
    for f in os.listdir(test_dir):
        file_path = os.path.join(test_dir, f)
        # Remove old SVGs in root
        if f.endswith(".svg"):
            os.remove(file_path)
        # Remove old MDs (except README)
        elif f.endswith(".md") and f != "README.md":
            os.remove(file_path)
        # Remove old generic 'visuals' directory if it exists
        elif f == "visuals" and os.path.isdir(file_path):
            shutil.rmtree(file_path)

    test_files = [f for f in os.listdir(test_dir) if f.startswith("test_") and f.endswith(".py")]
    test_files.sort()

    for test_file in test_files:
        module_name = test_file[:-3]
        module_path = os.path.join(test_dir, test_file)
        md_file = os.path.join(test_dir, f"{module_name}.md")
        
        # Folder for this module's SVG clutter
        assets_dir_name = f"{module_name}_assets"
        assets_dir = os.path.join(test_dir, assets_dir_name)
        
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

        # Ensure assets dir exists and is empty for this run
        if os.path.exists(assets_dir):
            shutil.rmtree(assets_dir)
        os.makedirs(assets_dir, exist_ok=True)
        
        # Ensure it's ignored by git
        gitignore_path = ".gitignore"
        ignore_entry = f"{assets_dir}/\n"
        with open(gitignore_path, "a+") as gf:
            gf.seek(0)
            if ignore_entry not in gf.read():
                gf.write(ignore_entry)

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
            svg_path = os.path.join(assets_dir, svg_filename)
            
            with open(svg_path, "w") as f:
                f.write(board_to_svg(board))

            md_content.append(f"## [{s.id}] {s.name}")
            md_content.append(f"**Test**: `{func.__name__}`")
            md_content.append(f"\n**Description**:\n{s.description}")
            md_content.append(f"\n**Pass Condition (Boolean Check)**:\n{s.pass_condition}")
            md_content.append(f"\n<img src='{assets_dir_name}/{svg_filename}' width='600'>\n")
            
        with open(md_file, "w") as f:
            f.write("\n".join(md_content))
        print(f"Generated {md_file} ({len(functions)} scenarios in {assets_dir_name}/)")

if __name__ == "__main__":
    main()
