import textwrap

import pytest

from conan.test.assets.genconanfile import GenConanfile
from conan.test.utils.tools import TestClient
from conans.util.files import save
import os

sbom_hook = """

import json
import os
from conan.errors import ConanException
from conan.api.output import ConanOutput
from conan.tools.sbom.cycloneDX import cyclonedx_1_4

def _generate_cyclonedx_1_4_file(conanfile):
    try:
        sbom_cyclonedx_1_4 = cyclonedx_1_4(conanfile.subgraph)
        metadata_folder = conanfile.package_metadata_folder
        file_name = "cyclonedx_1_4.json"
        with open(os.path.join(metadata_folder, file_name), 'w') as f:
            json.dump(sbom_cyclonedx_1_4, f, indent=4)
        ConanOutput().success(f"CYCLONEDX CREATED - {conanfile.package_metadata_folder}")
    except Exception as e:
        ConanException("error generating CYCLONEDX file")

def post_package(conanfile):
    _generate_cyclonedx_1_4_file(conanfile)

def post_generate(conanfile):
    _generate_cyclonedx_1_4_file(conanfile)
"""

@pytest.fixture()
def hook_setup():
    tc = TestClient()
    hook_path = os.path.join(tc.paths.hooks_path, "hook_sbom.py")
    save(hook_path, sbom_hook)
    return tc

def test_sbom_generation_create(hook_setup):
    tc = hook_setup
    tc.run("new cmake_lib -d name=dep -d version=1.0")
    tc.run("export .")
    tc.run("new cmake_lib -d name=foo -d version=1.0 -d requires=dep/1.0 -f")
    tc.run("export .")
    tc.run("new cmake_lib -d name=bar -d version=1.0 -d requires=foo/1.0 -f")
    # bar -> foo -> dep
    tc.run("create . --build=missing")
    bar_layout = tc.created_layout()
    assert os.path.exists(os.path.join(bar_layout.build(),"..", "d", "metadata", "cyclonedx_1_4.json"))

def test_sbom_generation_install_requires(hook_setup):
    tc = hook_setup
    tc.save({"dep/conanfile.py": GenConanfile("dep", "1.0"),
             "conanfile.py": GenConanfile("foo", "1.0").with_requires("dep/1.0")})
    tc.run("export dep")
    tc.run("create . --build=missing")

    #cli -> foo -> dep
    tc.run("install --requires=foo/1.0")
    assert os.path.exists(os.path.join(tc.current_folder, "cyclonedx_1_4.json"))

def test_sbom_generation_install_path(hook_setup):
    tc = hook_setup
    tc.save({"dep/conanfile.py": GenConanfile("dep", "1.0"),
             "conanfile.py": GenConanfile("foo", "1.0").with_requires("dep/1.0")})
    tc.run("create dep")

    #foo -> dep
    tc.run("install .")
    assert os.path.exists(os.path.join(tc.current_folder, "cyclonedx_1_4.json"))

def test_sbom_generation_install_path_consumer(hook_setup):
    tc = hook_setup
    tc.save({"dep/conanfile.py": GenConanfile("dep", "1.0"),
             "conanfile.py": GenConanfile().with_requires("dep/1.0")})
    tc.run("create dep")

    #conanfile.py -> dep
    tc.run("install .")
    assert os.path.exists(os.path.join(tc.current_folder, "cyclonedx_1_4.json"))

def test_sbom_generation_install_path_txt(hook_setup):
    tc = hook_setup
    tc.save({"dep/conanfile.py": GenConanfile("dep", "1.0"),
             "conanfile.txt": textwrap.dedent(
                 """
                 [requires]
                 dep/1.0
                 """
             )})
    tc.run("create dep")

    #foo -> dep
    tc.run("install .")
    assert os.path.exists(os.path.join(tc.current_folder, "cyclonedx_1_4.json"))

def test_sbom_generation_skipped_dependencies(hook_setup):
    tc = hook_setup
    tc.save({"dep/conanfile.py": GenConanfile("dep", "1.0"),
             "app/conanfile.py": GenConanfile("app", "1.0")
                                .with_package_type("application")
                                .with_requires("dep/1.0"),
             "conanfile.py": GenConanfile("foo", "1.0").with_tool_requires("app/1.0")})
    tc.run("create dep")
    tc.run("create app")
    tc.run("create .")
    create_layout = tc.created_layout()

    cyclone_path = os.path.join(create_layout.build(), "..", "d", "metadata", "cyclonedx_1_4.json")
    content = tc.load(cyclone_path)
    # A skipped dependency also shows up in the sbom
    assert "pkg:conan/dep@1.0?rref=6a99f55e933fb6feeb96df134c33af44" in content
