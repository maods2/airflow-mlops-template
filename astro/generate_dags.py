#!/usr/bin/env python3
"""
DAG Generation Script

This script generates Airflow DAGs from YAML configuration files
using the DAG builder module.
"""

import sys
import os
from pathlib import Path

# Add current directory to Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

from dag_builder.builder import DAGBuilder


def main():
    """Main function to generate DAGs"""
    print("🚀 Starting DAG generation process...")
    
    try:
        # Initialize DAG builder
        builder = DAGBuilder(
            config_dir="config",
            templates_dir="templates", 
            dags_dir="dags"
        )
        
        print("📁 Configuration directories:")
        print(f"  - Config: {builder.config_dir}")
        print(f"  - Templates: {builder.templates_dir}")
        print(f"  - DAGs: {builder.dags_dir}")
        
        # Clean up old DAGs (keep exampledag.py and __init__.py)
        print("\n🧹 Cleaning up old DAGs...")
        builder.cleanup_old_dags(["__init__.py", "exampledag.py"])
        
        # Generate all DAGs from config files
        print("\n⚙️  Generating DAGs from configuration files...")
        generated_dags = builder.build_all_dags()
        
        if generated_dags:
            print(f"\n✅ Successfully generated {len(generated_dags)} DAGs:")
            for dag_path in generated_dags:
                print(f"  - {dag_path}")
        else:
            print("\n⚠️  No DAGs were generated. Check your configuration files.")
        
        print("\n🎉 DAG generation completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Error during DAG generation: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
