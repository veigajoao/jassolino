import os
from pathlib import Path

from .agent import graph

# Determine the project root
# This assumes your script is in a known location relative to the project root
# Adjust the number of parent directories as needed
PROJECT_ROOT = Path(__file__).resolve().parents[1]  # Adjust the number (1) as needed

try:
    png_data = graph.get_graph().draw_mermaid_png()
    
    # Create the output filename using an absolute path
    output_file = PROJECT_ROOT / 'graph.png'
    
    # Write the PNG data to the file
    with open(output_file, 'wb') as f:
        f.write(png_data)
    
    print(f"Image saved to: {output_file}")
except Exception as e:
    print(f"An error occurred: {e}")

