spdx_json_generator = """
import time
import json
from datetime import datetime, timezone
from conan import conan_version
from conan.errors import ConanException

import pathlib

def generate_sbom(graph, **kwargs):
    name = graph.root.name
    version = graph.root.ref.version
    date = datetime.fromtimestamp(time.time(), tz=timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    packages = []
    for dependency in graph.nodes:
        packages.append(
            {
                "name": dependency.ref.name,
                "SPDXID": f"SPDXRef-{dependency.ref}",
                "version": str(dependency.ref.version),
                "license": dependency.conanfile.license or "NOASSERTION",
            })
    files = []
    # https://spdx.github.io/spdx-spec/v2.2.2/package-information/
    data = {
        "SPDXVersion": "SPDX-2.2",
        "DataLicense": "CC0-1.0",
        "SPDXID": "SPDXRef-DOCUMENT",
        "DocumentName": f"{name}-{version}",
        "DocumentNamespace": f"http://spdx.org/spdxdocs/{name}-{version}-{date}", # the date or hash to make it unique
        "Creator": f"Tool: Conan-{conan_version}",
        "Created": date, #YYYY-MM-DDThh:mm:ssZ
        "Packages": [{
            "PackageName": p["name"],
            "SPDXID": p["SPDXID"],
            "PackageVersion": p["version"],
            "PackageDownloadLocation": "NOASSERTION",
            "FilesAnalyzed": False,
            "PackageLicenseConcluded": p["license"],
            "PackageLicenseDeclared": p["license"],
        } for p in packages],
        # "Files": [{
        #     "FileName": f["path"],  # Path to file
        #     "SPDXID": f["SPDXID"],
        #     "FileChecksum": f'{f["checksum_algorithm"]}: {f["checksum_algorithm_value"]}',
        #     "LicenseConcluded": f["licence"],
        #     "LicenseInfoInFile": f["licence"],
        #     "FileCopyrightText": "NOASSERTION"
        # } for f in files],
    }
    try:
        with open(f"../{name}-{version}.spdx.json", 'w') as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        ConanException("error generating spdx file")
"""
