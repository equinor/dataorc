"""
Parameter validation logic.
"""

from .models import CorePipelineConfig


def print_config(
    config: CorePipelineConfig, title: str = "Pipeline Configuration"
) -> None:
    """Print configuration for debugging."""
    print(f"📦 {title}:")
    # `env` is a plain string in the current design
    print(f"   Environment: {config.env}")

    print("   🏗️ Data Lake Structure:")
    print(f"     Domain: {config.domain}")
    print(f"     Product: {config.product}")
    print(f"     Table: {config.table_name}")
    print(f"     Bronze Version: {config.bronze_version}")
    print(f"     Silver Version: {config.silver_version}")
    print(f"     Gold Version: {config.gold_version}")

    print("   ⚙️ Processing Methods:")
    print(f"     Bronze: {config.bronze_processing_method}")
    print(f"     Silver: {config.silver_processing_method}")
    print(f"     Gold: {config.gold_processing_method}")

    # Only show generated lake paths if structure is complete
    container = config.env_vars.get("datalake_container_name", "")
    if not container:
        print("   📦 Layer-as-container mode (no datalake_container_name)")
    if all([config.domain, config.product, config.table_name]):
        print("   📁 Generated Paths:")
        print(f"     Bronze Lake Path: {config.get_lake_path('bronze')}")
        print(f"     Silver Lake Path: {config.get_lake_path('silver')}")
        print(f"     Gold Lake Path: {config.get_lake_path('gold')}")
        print("   📁 Work paths:")
        print(f"     Bronze: {config.get_work_path('bronze')}")
        print(f"     Silver: {config.get_work_path('silver')}")
        print(f"     Gold: {config.get_work_path('gold')}")
    else:
        print("   ⚠️  Data Lake Structure incomplete - paths not generated")

    # Infrastructure variables
    if config.env_vars:
        print("   🔧 Infrastructure Variables:")
        for key, value in sorted(config.env_vars.items()):
            display_value = value if value else "(empty)"
            print(f"     {key}: {display_value}")
