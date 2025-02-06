from conan.test.utils.tools import TestClient, GenConanfile


def test_create_consume_module():

    # main ->   mod   -> dep/1.0
    #      -> dep/2.0
    tc = TestClient()
    tc.save({"conanfile.py": GenConanfile("dep", "1.0").with_generator("CMakeDeps").with_settings("build_type")})
    tc.run('create -c tools.cmake.cmakedeps:new="will_break_next" .')
    tc.save({"conanfile.py": GenConanfile("dep", "2.0").with_generator("CMakeDeps").with_settings("build_type")})
    tc.run('create -c tools.cmake.cmakedeps:new="will_break_next" .')
    tc.save({"conanfile.py": GenConanfile("mod", "1.0").with_requirement("dep/1.0", visible=False).with_package_type("module").with_generator("CMakeDeps").with_settings("build_type")})
    tc.run('create -c tools.cmake.cmakedeps:new="will_break_next" .')
    tc.save({"conanfile.py": GenConanfile("main", "1.0").with_requires("dep/2.0", "mod/1.0").with_generator("CMakeDeps").with_settings("build_type")})
    tc.run('create -c tools.cmake.cmakedeps:new="will_break_next" .')
    assert True
