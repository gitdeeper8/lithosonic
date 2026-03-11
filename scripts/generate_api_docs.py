#!/usr/bin/env python3
"""Generate API documentation from docstrings"""

import os
import inspect
import importlib
from pathlib import Path

def generate_module_docs(module_name, output_dir):
    """Generate documentation for a module"""
    try:
        module = importlib.import_module(module_name)
        
        output_file = output_dir / f"{module_name.replace('.', '_')}.md"
        
        with open(output_file, 'w') as f:
            f.write(f"# {module_name}\n\n")
            
            if module.__doc__:
                f.write(f"{module.__doc__}\n\n")
            
            # Document classes
            for name, obj in inspect.getmembers(module, inspect.isclass):
                if obj.__module__ == module_name:
                    f.write(f"## Class: {name}\n\n")
                    if obj.__doc__:
                        f.write(f"{obj.__doc__}\n\n")
                    
                    # Document methods
                    for method_name, method in inspect.getmembers(obj, inspect.isfunction):
                        if not method_name.startswith('_'):
                            f.write(f"### {method_name}\n\n")
                            if method.__doc__:
                                f.write(f"{method.__doc__}\n\n")
            
            # Document functions
            for name, func in inspect.getmembers(module, inspect.isfunction):
                if func.__module__ == module_name:
                    f.write(f"## Function: {name}\n\n")
                    if func.__doc__:
                        f.write(f"{func.__doc__}\n\n")
        
        print(f"Generated {output_file}")
        
    except Exception as e:
        print(f"Error generating docs for {module_name}: {e}")

def main():
    docs_dir = Path("docs/api")
    docs_dir.mkdir(parents=True, exist_ok=True)
    
    modules = [
        "litho_physics.biot",
        "litho_physics.impedance",
        "litho_physics.fracture_resonance",
        "litho_physics.attenuation",
        "litho_physics.emission",
        "litho_physics.lsi",
        "pipeline.ingest",
        "pipeline.spectral",
        "pipeline.harmonic",
        "pipeline.inversion",
        "instruments.litho_geo_v2",
        "instruments.infrasound_array",
        "instruments.tiltmeter",
        "instruments.calibration",
        "alert.thresholds",
        "alert.neyman_pearson",
        "alert.notifications",
    ]
    
    for module in modules:
        generate_module_docs(module, docs_dir)
    
    print("API documentation generated successfully")

if __name__ == "__main__":
    main()
