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

def test_sbom_generation_install():
    tc = TestClient()
    tc.save({"dep/conanfile.py": GenConanfile("dep", "1.0"),
             "conanfile.py": GenConanfile("foo", "1.0").with_requires("dep/1.0")})
    tc.run("export dep")
    tc.run("create . --build=missing")

    #cli -> foo -> dep
    tc.run("install --requires=foo/1.0")
    assert os.path.exists(os.path.join(tc.current_folder, "CLI-cyclonedx.json"))
