# TODO RENAME THIS FILE

spdx_json_generator = """

def generate_sbom(graph, **kwargs):
    cyclonedx_1_4(graph, **kwargs)
    #spdx_sbom(graph, **kwargs)

def cyclonedx_1_4(graph, **kwargs):
    import json
    import os
    import uuid
    import time
    from datetime import datetime, timezone
    from conan import conan_version
    from conan.errors import ConanException
    from conan.api.subapi.graph import CONTEXT_BUILD
    from conan.api.output import ConanOutput

    if graph.root.conanfile.tested_reference_str: # Is a test package
        return

    components = [node for node in graph.nodes if node.recipe != "Cli"]
    IS_CLI = graph.root.recipe == "Cli"
    CLI_ID = str(uuid.uuid4())

    dependencies = []
    if IS_CLI:
        deps = {"ref": CLI_ID}
        deps["dependsOn"] = [f"pkg:conan/{d.dst.name}@{d.dst.ref.version}?rref={d.dst.ref.revision}" for d in graph.root.dependencies]
        dependencies.append(deps)
    for c in components:
        deps = {"ref": f"pkg:conan/{c.name}@{c.ref.version}?rref={c.ref.revision}"}
        dependsOn = [f"pkg:conan/{d.dst.name}@{d.dst.ref.version}?rref={d.dst.ref.revision}" for d in c.dependencies]
        if dependsOn:
            deps["dependsOn"] = dependsOn
        dependencies.append(deps)

    def _calculate_licenses(component):
        if isinstance(component.conanfile.license, str): # Just one license
            return [{"license": {
                        "id": component.conanfile.license
                    }}]
        return [{"license": {
                    "id": license
                }} for license in c.conanfile.license]

    sbom_cyclonedx_1_4 = {
        **({"components": [{
            "author": "Conan",
            "bom-ref": CLI_ID if IS_CLI else f"pkg:conan/{c.name}@{c.ref.version}?rref={c.ref.revision}",
            "description": c.conanfile.description,
            **({"externalReferences": [{
                "type": "website",
                "url": c.conanfile.homepage
            }]} if c.conanfile.homepage else {}),
            **({"licenses": _calculate_licenses(c)} if c.conanfile.license else {}),
            "name": c.name,
            "fpurl": f"pkg:conan/{c.name}@{c.ref.version}?rref={c.ref.revision}",
            "type": "library",
            "version": str(c.ref.version),
        } for c in components]} if components else {}),
        **({"dependencies": dependencies} if dependencies else {}),
        "metadata": {
            "component": {
                "author": "Conan",
                "bom-ref": f"pkg:conan/{graph.root.name}@{graph.root.ref.version}?rref={graph.root.ref.revision}",
                "name": graph.root.name,
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
    try:
        metadata_folder = graph.root.conanfile.package_metadata_folder
        file_name = "CLI-cyclonedx.json" if IS_CLI else f"{graph.root.name}-{graph.root.ref.version}-cyclonedx.json"
        with open(os.path.join(metadata_folder, file_name), 'w') as f:
            json.dump(sbom_cyclonedx_1_4, f, indent=4)
        ConanOutput().success(f"CYCLONEDX CREATED - {graph.root.conanfile.package_metadata_folder}")
    except Exception as e:
        ConanException("error generating CYCLONEDX file")

def spdx_sbom(graph, **kwargs):
    import os
    import time
    import json
    import pathlib
    from glob import glob
    from datetime import datetime, timezone
    from conan import conan_version
    from conan.errors import ConanException
    from conan.api.output import ConanOutput

    name = graph.root.name if graph.root.name else "CLI"
    version = "SPDX-2.2"
    date = datetime.fromtimestamp(time.time(), tz=timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    packages = []
    files = []
    relationships = []

    # --- Root node ---
    if graph.root.recipe != "Cli":
        conan_data = graph.root.conanfile.conan_data
        url_location = conan_data.get("sources", {}).get(graph.root.conanfile.version, {}).get("url", {}) if conan_data else None
        checksum = conan_data.get("sources", {}).get(graph.root.conanfile.version, {}).get("sha256", {}) if conan_data else None
        packages.extend([
            {
                "name": graph.root.ref.name,
                "SPDXID": f"SPDXRef-{graph.root.ref}",
                "version": str(graph.root.ref.version),
                "downloadLocation": graph.root.conanfile.url or "NOASSERTION",
                "homePage": graph.root.conanfile.homepage or "NOASSERTION",
                "licenseConcluded": graph.root.conanfile.license or "NOASSERTION",
                "licenseDeclared": "NOASSERTION",
                "copyrightText": "NOASSERTION",
                "description": graph.root.conanfile.description or "NOASSERTION",
                "comment":  f"This is the {graph.root.ref.name} package in the remote" # TODO It could be a local package

            },
            {
                "name": f"{graph.root.pref} binary",
                "SPDXID": f"SPDXRef-binary-{graph.root.ref}",
                "downloadLocation": graph.root.remote.url if graph.root.remote else "NONE",
                "licenseConcluded": graph.root.conanfile.license or "NOASSERTION",
                "licenseDeclared": "NOASSERTION",
                "copyrightText": "NOASSERTION",
                "comment": f"This is the {graph.root.ref} binary generated by conan"
            },
            {
                "name": f"{graph.root.ref.name} upstream",
                "SPDXID": f"SPDXRef-resource-{graph.root.ref}",
                "downloadLocation": url_location or "NONE",
                **({"checksum": {
                        "algorithm": "SHA256",
                        "checksumValue": checksum
                    }} if checksum else {}),
                "licenseConcluded": graph.root.conanfile.license or "NOASSERTION",
                "licenseDeclared": "NOASSERTION",
                "copyrightText": "NOASSERTION",
                "comment": f"This is the {graph.root.ref.name} release file"
            }])

        relationships.extend([{
            "spdxElementId": f"SPDXRef-binary-{graph.root.ref}",
            "relationshipType": "DEPENDS_ON",
            "relatedSpdxElement": f"SPDXRef-binary-{d.dst.ref}",
        }for d in graph.root.dependencies])

        relationships.append({
            "spdxElementId": f"SPDXRef-{graph.root.ref}",
            "relationshipType": "GENERATES",
            "relatedSpdxElement": f"SPDXRef-binary-{graph.root.ref}",
        })

        exported_path = graph.root.conanfile.recipe_folder # /e folder
        external_files = [f for f in glob(os.path.join(exported_path, "**", "*"), recursive=True) if not f.endswith('/')] if exported_path else []

        try:
            with open(os.path.join(graph.root.conanfile.recipe_folder, "conanmanifest.txt")) as conanmanifest:
                external_files.extend([os.path.join(exported_path[:-1], *line.split(" ")[0][:-1].split("/")) for line in conanmanifest.readlines()[2:]])
        except Exception:
            pass

        for i, file_name in enumerate(external_files):
            checksum = None
            files.append(
                {
                    "fileName": file_name,
                    "SPDXID": f"SPDXRef-file-{graph.root.ref}-{i}",
                    **({"checksums":{
                            "algorithm": "SHA256",
                            "checksumValues": checksum,
                        }} if checksum else {}),
                    "licenseConcluded": "NOASSERTION",
                    "copyrightText": "NOASSERTION"
                }
            )
            relationships.append({
                "spdxElementId": f"SPDXRef-{graph.root.ref}",
                "relationshipType": "CONTAINS",
                "relatedSpdxElement": f"SPDXRef-file-{graph.root.ref}-{i}",
            })

    # --- Just the binaries for dependencies ---
    for node in graph.nodes[1:]:
        conan_data = node.conanfile.conan_data
        url_location = conan_data.get("sources", {}).get(node.conanfile.version, {}).get("url", {}) if conan_data else None
        checksum = conan_data.get("sources", {}).get(node.conanfile.version, {}).get("sha256", {}) if conan_data else None
        packages.extend([
            {
                "name": f"{node.pref} binary",
                "SPDXID": f"SPDXRef-binary-{node.ref}",
                "downloadLocation": node.remote.url if node.remote else "NONE",
                "licenseConcluded": node.conanfile.license or "NOASSERTION",
                "licenseDeclared": "NOASSERTION",
                "copyrightText": "NOASSERTION",
                "comment": f"This is the {node.ref} binary generated by conan"
            }])

        relationships.extend([{
            "spdxElementId": f"SPDXRef-binary-{node.ref}",
            "relationshipType": "DEPENDS_ON",
            "relatedSpdxElement": f"SPDXRef-binary-{d.dst.ref}",
        }for d in node.dependencies])


    # https://spdx.github.io/spdx-spec/v2.2.2/package-information/
    data = {
        "SPDXVersion": "SPDX-2.2",
        "dataLicense": "CC0-1.0",
        "SPDXID": "SPDXRef-DOCUMENT",
        "documentName": f"{name}-{version}",
        "documentNamespace": f"http://spdx.org/spdxdocs/{name}-{version}-{date}", # the date or hash to make it unique
        "creator": f"Tool: Conan-{conan_version}",
        "created": date, #YYYY-MM-DDThh:mm:ssZ
        "packages": packages,
        **({"files": files} if files else {}),
        **({"relationships": relationships} if relationships else {}),
    }
    try:
        metadata_folder = graph.root.conanfile.package_metadata_folder
        with open(os.path.join(metadata_folder, f"{name}-{graph.root.ref.version if graph.root.ref else 'local'}.spdx.json"), 'w') as f:
            json.dump(data, f, indent=4)
        ConanOutput().success(f"SPDX CREATED - {graph.root.conanfile.package_metadata_folder}")
    except Exception as e:
        ConanException("error generating spdx file")
"""
