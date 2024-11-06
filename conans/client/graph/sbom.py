from conans.client.graph.spdx import spdx_json_generator
from conan.internal.cache.home_paths import HomePaths

def migrate_sbom_file(cache_folder):
    from conans.client.migrations import update_file
    sbom_path = HomePaths(cache_folder).sbom_manifest_plugin_path
    update_file(sbom_path, spdx_json_generator)
