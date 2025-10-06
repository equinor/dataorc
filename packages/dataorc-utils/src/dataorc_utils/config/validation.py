"""
Parameter validation logic.
"""

from .models import CorePipelineConfig


def print_config(
    config: CorePipelineConfig, title: str = "Pipeline Configuration"
) -> None:
    """Print configuration for debugging."""
    print(f"📦 {title}:")
    # Handle both string and enum types
    env_value = config.env.value if hasattr(config.env, "value") else str(config.env)
    load_type_value = (
        config.load_type.value
        if hasattr(config.load_type, "value")
        else str(config.load_type)
    )

    print(f"   Environment: {env_value}")
    print(f"   Data Lake: {config.datalake_name}")
    print(f"   Container: {config.datalake_container_name}")
    print(f"   Load Type: {load_type_value}")

    print("   🏗️ Data Lake Structure:")
    print(f"     Domain: {config.domain}")
    print(f"     Product: {config.product}")
    print(f"     Bronze Version: {config.bronze_version}")
    print(f"     Silver Version: {config.silver_version}")
    print(f"     Gold Version: {config.gold_version}")

    print("   ⚙️ Processing Methods:")
    print(f"     Bronze: {config.bronze_processing_method}")
    print(f"     Silver: {config.silver_processing_method}")
    print(f"     Gold: {config.gold_processing_method}")

    # Only show generated lake paths if structure is complete
    if all([config.domain, config.product]):
        print("   📁 Generated Paths:")
        print(f"     Bronze Lake Path: {config.get_lake_path('bronze')}")
        print(f"     Silver Lake Path: {config.get_lake_path('silver')}")
        print(f"     Gold Lake Path: {config.get_lake_path('gold')}")
    else:
        print("   ⚠️  Data Lake Structure incomplete - paths not generated")
    # Azure infrastructure
    if hasattr(config, "apim_base_url") and config.apim_base_url:
        print(f"   APIM URL: {config.apim_base_url}")
    if hasattr(config, "az_keyvault_scope") and config.az_keyvault_scope:
        print(f"   KeyVault Scope: {config.az_keyvault_scope}")
