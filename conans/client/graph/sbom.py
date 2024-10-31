import os

from conan.internal.cache.home_paths import HomePaths

def migrate_sbom_file(cache_folder):
    from conans.client.migrations import update_file
    with open("spdx.py", "r") as file:
        default_spdx_json = file.read()
        sbom_path = HomePaths(cache_folder).sbom_manifest_plugin_path
        update_file(sbom_path, default_spdx_json)
