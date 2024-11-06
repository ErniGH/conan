from conan.test.assets.genconanfile import GenConanfile
from conan.test.utils.tools import TestClient
import os


def test_sbom_generation_create():
    tc = TestClient()
    tc.save({"dep/conanfile.py": GenConanfile("dep", "1.0"),
             "conanfile.py": GenConanfile("foo", "1.0").with_requires("dep/1.0")})
    tc.run("export dep")
    tc.run("create . --build=missing")
    foo_layout = tc.created_layout()

    assert os.path.exists(os.path.join(foo_layout.build(), "foo-1.0.spdx.json"))

def test_sbom_generation_install():
    tc = TestClient()
    tc.save({"dep/conanfile.py": GenConanfile("dep", "1.0"),
             "conanfile.py": GenConanfile("foo", "1.0").with_requires("dep/1.0")})
    tc.run("export dep")
    tc.run("create . --build=missing")

    tc.run("install --requires=foo/1.0")
    assert os.path.exists(os.path.join(tc.current_folder,  "foo-1.0.spdx.json")) #TODO FIX this test
