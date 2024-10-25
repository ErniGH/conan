from conan.test.assets.genconanfile import GenConanfile
from conan.test.utils.tools import TestClient
import os


def test_sbom_generation():
    tc = TestClient(light=True)
    tc.save({"dep/conanfile.py": GenConanfile("dep", "1.0"),
             "conanfile.py": GenConanfile("foo", "1.0").with_requires("dep/1.0")})
    tc.run("export dep")
    tc.run("create . --build=missing")
    assert os.path.exists(os.path.join(tc.current_folder, "spdx", "dep-1.0-SPDX.json"))
    assert os.path.exists(os.path.join(tc.current_folder, "spdx", "foo-1.0-SPDX.json"))
