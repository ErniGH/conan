

def cyclonedx_1_4(graph, add_tool_requires=True, add_tests=False, **kwargs):
    """
    (Experimental) Generate cyclone 1.4 sbom with json format
    """
    import uuid
    import time
    from datetime import datetime, timezone

    has_special_root_node = not (getattr(graph.root.ref, "name", False) and getattr(graph.root.ref, "version", False) and getattr(graph.root.ref, "revision", False))
    special_id = str(uuid.uuid4())
    components = [node for node in graph.nodes if
                  (node.test and add_tests and node.context == "build" and add_tool_requires) or
                  (node.test and add_tests and node.context != "build") or
                  (not node.test and node.context == "build" and add_tool_requires) or
                  (not node.test and node.context != "build")]
    if has_special_root_node:
        components = components[1:]

    dependencies = []
    if has_special_root_node:
        deps = {"ref": special_id,
                "dependsOn": [f"pkg:conan/{d.dst.name}@{d.dst.ref.version}?rref={d.dst.ref.revision}"
                              for d in graph.root.dependencies]}
        dependencies.append(deps)
    for c in components:
        deps = {"ref": f"pkg:conan/{c.name}@{c.ref.version}?rref={c.ref.revision}"}
        dep = [d for d in c.dependencies if
               (d.dst.test and add_tests and d.dst.context == "build" and add_tool_requires) or
               (d.dst.test and add_tests and d.dst.context != "build") or
               (not d.dst.test and d.dst.context =="build"  and add_tool_requires) or
               (not d.dst.test and d.dst.context !="build")]
        depends_on = [f"pkg:conan/{d.dst.name}@{d.dst.ref.version}?rref={d.dst.ref.revision}" for d in dep]
        if depends_on:
            deps["dependsOn"] = depends_on
        dependencies.append(deps)

    def _calculate_licenses(component):
        if isinstance(component.conanfile.license, str): # Just one license
            return [{"license": {
                        "id": component.conanfile.license
                    }}]
        return [{"license": {
                    "id": l
                }} for l in c.conanfile.license]

    sbom_cyclonedx_1_4 = {
        **({"components": [{
            "author": "Conan",
            "bom-ref": special_id if has_special_root_node else f"pkg:conan/{c.name}@{c.ref.version}?rref={c.ref.revision}",
            "description": c.conanfile.description,
            **({"externalReferences": [{
                "type": "website",
                "url": c.conanfile.homepage
            }]} if c.conanfile.homepage else {}),
            **({"licenses": _calculate_licenses(c)} if c.conanfile.license else {}),
            "name": c.name,
            "purl": f"pkg:conan/{c.name}@{c.ref.version}",
            "type": "library",
            "version": str(c.ref.version),
        } for c in components]} if components else {}),
        **({"dependencies": dependencies} if dependencies else {}),
        "metadata": {
            "component": {
                "author": "Conan",
                "bom-ref": special_id if has_special_root_node else f"pkg:conan/{c.name}@{c.ref.version}?rref={c.ref.revision}",
                "name": graph.root.conanfile.display_name,
                "type": "library"
            },
            "timestamp": f"{datetime.fromtimestamp(time.time(), tz=timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')}",
            "tools": [{
                "externalReferences": [{
                    "type": "website",
                    "url": "https://github.com/conan-io/conan"
                }],
                "name": "Conan-io"
            }],
        },
        "serialNumber": f"urn:uuid:{uuid.uuid4()}",
        "bomFormat": "CycloneDX",
        "specVersion": "1.4",
        "version": 1,
    }
    return sbom_cyclonedx_1_4
