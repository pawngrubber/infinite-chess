import os
import sys
import importlib.util
from board.board import Board
from board.svg import board_to_svg
from board.testing import get_captured_board, Scenario

def main():
    test_dir = "tests/board"
    visuals_dir = os.path.join(test_dir, "visuals")
    
    # 1. Cleanup old documentation to avoid clutter
    print(f"Cleaning up old documentation in {test_dir}...")
    for f in os.listdir(test_dir):
        if f.endswith(".md") and f != "README.md":
            os.remove(os.path.join(test_dir, f))
    
    if os.path.exists(visuals_dir):
        for f in os.listdir(visuals_dir):
            if f.endswith(".svg"):
                os.remove(os.path.join(visuals_dir, f))
    
    os.makedirs(visuals_dir, exist_ok=True)

    test_files = [f for f in os.listdir(test_dir) if f.startswith("test_") and f.endswith(".py")]
    test_files.sort()

    for test_file in test_files:
        module_name = test_file[:-3]
        module_path = os.path.join(test_dir, test_file)
        md_file = os.path.join(test_dir, f"{module_name}.md")
        
        spec = importlib.util.spec_from_file_location(module_name, module_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        md_content = [f"# {module_name.replace('_', ' ').title()}\n"]
        
        functions = []
        for name in dir(module):
            attr = getattr(module, name)
            if hasattr(attr, "_scenario"):
                functions.append(attr)
        
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
            svg_path = os.path.join(visuals_dir, svg_filename)
            
            with open(svg_path, "w") as f:
                f.write(board_to_svg(board))

            md_content.append(f"## [{s.id}] {s.name}")
            md_content.append(f"**Test**: `{func.__name__}`")
            md_content.append(f"\n**Description**:\n{s.description}")
            md_content.append(f"\n**Pass Condition (Boolean Check)**:\n{s.pass_condition}")
            md_content.append(f"\n<img src='visuals/{svg_filename}' width='600'>\n")
            
        if functions:
            with open(md_file, "w") as f:
                f.write("\n".join(md_content))
            print(f"Generated {md_file} ({len(functions)} scenarios)")
        else:
            # Handle old-style tests or inform the user
            print(f"Skipping {test_file} (no @scenario decorators found)")

if __name__ == "__main__":
    main()
