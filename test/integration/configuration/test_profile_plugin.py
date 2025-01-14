import os
import textwrap

from conan.internal.cache.home_paths import HomePaths
from conan.test.utils.tools import TestClient


class TestErrorsProfilePlugin:
    """ when the plugin fails, we want a clear message and a helpful trace
    """
    def test_error_profile_plugin(self):
        c = TestClient()
        profile_plugin = textwrap.dedent("""\
            def profile_plugin(profile):
                settings = profile.kk
            """)
        c.save_home({"extensions/plugins/profile.py": profile_plugin})

        c.run("install --requires=zlib/1.2.3", assert_error=True)
        assert "Error while processing 'profile.py' plugin, line 2" in c.out
        assert "settings = profile.kk" in c.out

    def test_remove_plugin_file(self):
        c = TestClient()
        c.run("version")  # to trigger the creation
        os.remove(HomePaths(c.cache_folder).profile_plugin_path)
        c.run("profile show", assert_error=True)
        assert "ERROR: The 'profile.py' plugin file doesn't exist" in c.out

    def test_regresion_29(self):
        # https://github.com/conan-io/conan/issues/17247
        c = TestClient()
        c.save({"conanfile.txt": ""})
        c.run("install . -s compiler=clang -s compiler.version=19 -s compiler.cppstd=26")
        # doesn't fail anymore
        c.run("install . -s compiler=apple-clang -s compiler.version=16 -s compiler.cppstd=26")
        # doesn't fail anymore
        c.run("install . -s compiler=gcc -s compiler.version=14 -s compiler.cppstd=26")
        # doesn't fail anymore


def test_android_ndk_version():
    c = TestClient()
    c.run("profile show -s os=Android")
    assert "os.ndk_version" not in c.out
    c.run("profile show -s os=Android -s os.ndk_version=r26")
    assert "os.ndk_version=r26" in c.out
    c.run("profile show -s os=Android -s os.ndk_version=r26a")
    assert "os.ndk_version=r26a" in c.out
