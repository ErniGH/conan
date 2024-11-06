import json
import os
import textwrap

from conan.test.assets.genconanfile import GenConanfile
from conan.test.utils.tools import TestClient
from conans.util.files import load


def test_subgraph_reports():
    c = TestClient()
    subgraph_hook = textwrap.dedent("""\
        import os, json
        from conan.tools.files import save
        from conans.model.graph_lock import Lockfile
        def post_package(conanfile):
            subgraph = conanfile.subgraph
            save(conanfile, os.path.join(conanfile.package_folder, "..", "..", f"{conanfile.name}-conangraph.json"),
                 json.dumps(subgraph.serialize(), indent=2))
            save(conanfile, os.path.join(conanfile.package_folder, "..", "..", f"{conanfile.name}-conan.lock"),
                 Lockfile(subgraph).dumps())
        """)

    c.save_home({"extensions/hooks/subgraph_hook/hook_subgraph.py": subgraph_hook})
    c.save({"dep/conanfile.py": GenConanfile("dep", "0.1"),
            "pkg/conanfile.py": GenConanfile("pkg", "0.1").with_requirement("dep/0.1"),
            "app/conanfile.py": GenConanfile("app", "0.1").with_requirement("pkg/0.1")})
    c.run("export dep")
    c.run("export pkg")
    # app -> pkg -> dep
    c.run("create app --build=missing --format=json")

    app_graph = json.loads(load(os.path.join(c.cache.builds_folder, "app-conangraph.json")))
    pkg_graph = json.loads(load(os.path.join(c.cache.builds_folder, "pkg-conangraph.json")))
    dep_graph = json.loads(load(os.path.join(c.cache.builds_folder, "dep-conangraph.json")))

    app_lock = json.loads(load(os.path.join(c.cache.builds_folder, "app-conan.lock")))
    pkg_lock = json.loads(load(os.path.join(c.cache.builds_folder, "pkg-conan.lock")))
    dep_lock = json.loads(load(os.path.join(c.cache.builds_folder, "dep-conan.lock")))

    assert len(app_graph["nodes"]) == len(app_lock["requires"])
    assert len(pkg_graph["nodes"]) == len(pkg_lock["requires"])
    assert len(dep_graph["nodes"]) == len(dep_lock["requires"])

