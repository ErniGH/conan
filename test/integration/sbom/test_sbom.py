import textwrap

from conan.test.assets.genconanfile import GenConanfile
from conan.test.utils.tools import TestClient
import os


def test_sbom_generation_create():
    tc = TestClient()
    tc.run("new cmake_lib -d name=dep -d version=1.0")
    tc.run("export .")
    tc.run("new cmake_lib -d name=foo -d version=1.0 -d requires=dep/1.0 -f")
    tc.run("export .")
    tc.run("new cmake_lib -d name=bar -d version=1.0 -d requires=foo/1.0 -f")
    # bar -> foo -> dep
    tc.run("create . --build=missing")
    bar_layout = tc.created_layout()
    assert os.path.exists(os.path.join(bar_layout.build(),"..", "d", "metadata", "bar-1.0-cyclonedx.json"))

def test_sbom_generation_install_requires():
    tc = TestClient()
    tc.save({"dep/conanfile.py": GenConanfile("dep", "1.0"),
             "conanfile.py": GenConanfile("foo", "1.0").with_requires("dep/1.0")})
    tc.run("export dep")
    tc.run("create . --build=missing")

    #cli -> foo -> dep
    tc.run("install --requires=foo/1.0")
    assert os.path.exists(os.path.join(tc.current_folder, "CLI-cyclonedx.json"))

def test_sbom_generation_install_path():
    tc = TestClient()
    tc.save({"dep/conanfile.py": GenConanfile("dep", "1.0"),
             "conanfile.py": GenConanfile("foo", "1.0").with_requires("dep/1.0")})
    tc.run("create dep")

    #foo -> dep
    tc.run("install .")
    assert os.path.exists(os.path.join(tc.current_folder, "foo-1.0-cyclonedx.json"))

def test_sbom_generation_install_path_consumer():
    # There is not .../d/metadata/...
    tc = TestClient()
    tc.save({"dep/conanfile.py": GenConanfile("dep", "1.0"),
             "conanfile.py": GenConanfile().with_requires("dep/1.0")})
    tc.run("create dep")

    #conanfile.py -> dep
    tc.run("install .")
    assert os.path.exists(os.path.join(tc.current_folder, "CONANFILE-PY-cyclonedx.json"))

def test_sbom_generation_install_path_txt():
    # There is not .../d/metadata/...
    tc = TestClient()
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
    assert os.path.exists(os.path.join(tc.current_folder, "CONANFILE-TXT-cyclonedx.json"))

def test_sbom_generation_skipped_dependencies():
    tc = TestClient()
    tc.save({"dep/conanfile.py": GenConanfile("dep", "1.0"),
             "app/conanfile.py": GenConanfile("app", "1.0")
                                .with_package_type("application")
                                .with_requires("dep/1.0"),
             "conanfile.py": GenConanfile("foo", "1.0").with_tool_requires("app/1.0")})
    tc.run("create dep")
    tc.run("create app")
    tc.run("create .")
    create_layout = tc.created_layout()

    cyclone_path = os.path.join(create_layout.build(), "..", "d", "metadata", "foo-1.0-cyclonedx.json")
    content = tc.load(cyclone_path)
    # A skipped dependency also shows up in the sbom
    assert "pkg:conan/dep@1.0?rref=6a99f55e933fb6feeb96df134c33af44" in content
