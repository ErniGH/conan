import os

from conan.internal.cache.home_paths import HomePaths

_default_spdx_json = """
import time
import json
import os
from datetime import datetime, timezone
from conan import conan_version
from conan.errors import ConanException

# https://spdx.org/licenses/
spdx_licences = {'0BSD', '3D-Slicer-1.0', 'AAL', 'Abstyles', 'AdaCore-doc', 'Adobe-2006', 'Adobe-Display-PostScript', 'Adobe-Glyph', 'Adobe-Utopia', 'ADSL', 'AFL-1.1', 'AFL-1.2', 'AFL-2.0', 'AFL-2.1', 'AFL-3.0', 'Afmparse', 'AGPL-1.0-only', 'AGPL-1.0-or-later', 'AGPL-3.0-only', 'AGPL-3.0-or-later', 'Aladdin', 'AMD-newlib', 'AMDPLPA', 'AML', 'AML-glslang', 'AMPAS', 'ANTLR-PD', 'ANTLR-PD-fallback', 'any-OSI', 'Apache-1.0', 'Apache-1.1', 'Apache-2.0', 'APAFML', 'APL-1.0', 'App-s2p', 'APSL-1.0', 'APSL-1.1', 'APSL-1.2', 'APSL-2.0', 'Arphic-1999', 'Artistic-1.0', 'Artistic-1.0-cl8', 'Artistic-1.0-Perl', 'Artistic-2.0', 'ASWF-Digital-Assets-1.0', 'ASWF-Digital-Assets-1.1', 'Baekmuk', 'Bahyph', 'Barr', 'bcrypt-Solar-Designer', 'Beerware', 'Bitstream-Charter', 'Bitstream-Vera', 'BitTorrent-1.0', 'BitTorrent-1.1', 'blessing', 'BlueOak-1.0.0', 'Boehm-GC', 'Borceux', 'Brian-Gladman-2-Clause', 'Brian-Gladman-3-Clause', 'BSD-1-Clause', 'BSD-2-Clause', 'BSD-2-Clause-Darwin', 'BSD-2-Clause-first-lines', 'BSD-2-Clause-Patent', 'BSD-2-Clause-Views', 'BSD-3-Clause', 'BSD-3-Clause-acpica', 'BSD-3-Clause-Attribution', 'BSD-3-Clause-Clear', 'BSD-3-Clause-flex', 'BSD-3-Clause-HP', 'BSD-3-Clause-LBNL', 'BSD-3-Clause-Modification', 'BSD-3-Clause-No-Military-License', 'BSD-3-Clause-No-Nuclear-License', 'BSD-3-Clause-No-Nuclear-License-2014', 'BSD-3-Clause-No-Nuclear-Warranty', 'BSD-3-Clause-Open-MPI', 'BSD-3-Clause-Sun', 'BSD-4-Clause', 'BSD-4-Clause-Shortened', 'BSD-4-Clause-UC', 'BSD-4.3RENO', 'BSD-4.3TAHOE', 'BSD-Advertising-Acknowledgement', 'BSD-Attribution-HPND-disclaimer', 'BSD-Inferno-Nettverk', 'BSD-Protection', 'BSD-Source-beginning-file', 'BSD-Source-Code', 'BSD-Systemics', 'BSD-Systemics-W3Works', 'BSL-1.0', 'BUSL-1.1', 'bzip2-1.0.6', 'C-UDA-1.0', 'CAL-1.0', 'CAL-1.0-Combined-Work-Exception', 'Caldera', 'Caldera-no-preamble', 'Catharon', 'CATOSL-1.1', 'CC-BY-1.0', 'CC-BY-2.0', 'CC-BY-2.5', 'CC-BY-2.5-AU', 'CC-BY-3.0', 'CC-BY-3.0-AT', 'CC-BY-3.0-AU', 'CC-BY-3.0-DE', 'CC-BY-3.0-IGO', 'CC-BY-3.0-NL', 'CC-BY-3.0-US', 'CC-BY-4.0', 'CC-BY-NC-1.0', 'CC-BY-NC-2.0', 'CC-BY-NC-2.5', 'CC-BY-NC-3.0', 'CC-BY-NC-3.0-DE', 'CC-BY-NC-4.0', 'CC-BY-NC-ND-1.0', 'CC-BY-NC-ND-2.0', 'CC-BY-NC-ND-2.5', 'CC-BY-NC-ND-3.0', 'CC-BY-NC-ND-3.0-DE', 'CC-BY-NC-ND-3.0-IGO', 'CC-BY-NC-ND-4.0', 'CC-BY-NC-SA-1.0', 'CC-BY-NC-SA-2.0', 'CC-BY-NC-SA-2.0-DE', 'CC-BY-NC-SA-2.0-FR', 'CC-BY-NC-SA-2.0-UK', 'CC-BY-NC-SA-2.5', 'CC-BY-NC-SA-3.0', 'CC-BY-NC-SA-3.0-DE', 'CC-BY-NC-SA-3.0-IGO', 'CC-BY-NC-SA-4.0', 'CC-BY-ND-1.0', 'CC-BY-ND-2.0', 'CC-BY-ND-2.5', 'CC-BY-ND-3.0', 'CC-BY-ND-3.0-DE', 'CC-BY-ND-4.0', 'CC-BY-SA-1.0', 'CC-BY-SA-2.0', 'CC-BY-SA-2.0-UK', 'CC-BY-SA-2.1-JP', 'CC-BY-SA-2.5', 'CC-BY-SA-3.0', 'CC-BY-SA-3.0-AT', 'CC-BY-SA-3.0-DE', 'CC-BY-SA-3.0-IGO', 'CC-BY-SA-4.0', 'CC-PDDC', 'CC0-1.0', 'CDDL-1.0', 'CDDL-1.1', 'CDL-1.0', 'CDLA-Permissive-1.0', 'CDLA-Permissive-2.0', 'CDLA-Sharing-1.0', 'CECILL-1.0', 'CECILL-1.1', 'CECILL-2.0', 'CECILL-2.1', 'CECILL-B', 'CECILL-C', 'CERN-OHL-1.1', 'CERN-OHL-1.2', 'CERN-OHL-P-2.0', 'CERN-OHL-S-2.0', 'CERN-OHL-W-2.0', 'CFITSIO', 'check-cvs', 'checkmk', 'ClArtistic', 'Clips', 'CMU-Mach', 'CMU-Mach-nodoc', 'CNRI-Jython', 'CNRI-Python', 'CNRI-Python-GPL-Compatible', 'COIL-1.0', 'Community-Spec-1.0', 'Condor-1.1', 'copyleft-next-0.3.0', 'copyleft-next-0.3.1', 'Cornell-Lossless-JPEG', 'CPAL-1.0', 'CPL-1.0', 'CPOL-1.02', 'Cronyx', 'Crossword', 'CrystalStacker', 'CUA-OPL-1.0', 'Cube', 'curl', 'cve-tou', 'D-FSL-1.0', 'DEC-3-Clause', 'diffmark', 'DL-DE-BY-2.0', 'DL-DE-ZERO-2.0', 'DOC', 'DocBook-Schema', 'DocBook-XML', 'Dotseqn', 'DRL-1.0', 'DRL-1.1', 'DSDP', 'dtoa', 'dvipdfm', 'ECL-1.0', 'ECL-2.0', 'EFL-1.0', 'EFL-2.0', 'eGenix', 'Elastic-2.0', 'Entessa', 'EPICS', 'EPL-1.0', 'EPL-2.0', 'ErlPL-1.1', 'etalab-2.0', 'EUDatagrid', 'EUPL-1.0', 'EUPL-1.1', 'EUPL-1.2', 'Eurosym', 'Fair', 'FBM', 'FDK-AAC', 'Ferguson-Twofish', 'Frameworx-1.0', 'FreeBSD-DOC', 'FreeImage', 'FSFAP', 'FSFAP-no-warranty-disclaimer', 'FSFUL', 'FSFULLR', 'FSFULLRWD', 'FTL', 'Furuseth', 'fwlw', 'GCR-docs', 'GD', 'GFDL-1.1-invariants-only', 'GFDL-1.1-invariants-or-later', 'GFDL-1.1-no-invariants-only', 'GFDL-1.1-no-invariants-or-later', 'GFDL-1.1-only', 'GFDL-1.1-or-later', 'GFDL-1.2-invariants-only', 'GFDL-1.2-invariants-or-later', 'GFDL-1.2-no-invariants-only', 'GFDL-1.2-no-invariants-or-later', 'GFDL-1.2-only', 'GFDL-1.2-or-later', 'GFDL-1.3-invariants-only', 'GFDL-1.3-invariants-or-later', 'GFDL-1.3-no-invariants-only', 'GFDL-1.3-no-invariants-or-later', 'GFDL-1.3-only', 'GFDL-1.3-or-later', 'Giftware', 'GL2PS', 'Glide', 'Glulxe', 'GLWTPL', 'gnuplot', 'GPL-1.0-only', 'GPL-1.0-or-later', 'GPL-2.0-only', 'GPL-2.0-or-later', 'GPL-3.0-only', 'GPL-3.0-or-later', 'Graphics-Gems', 'gSOAP-1.3b', 'gtkbook', 'Gutmann', 'HaskellReport', 'hdparm', 'HIDAPI', 'Hippocratic-2.1', 'HP-1986', 'HP-1989', 'HPND', 'HPND-DEC', 'HPND-doc', 'HPND-doc-sell', 'HPND-export-US', 'HPND-export-US-acknowledgement', 'HPND-export-US-modify', 'HPND-export2-US', 'HPND-Fenneberg-Livingston', 'HPND-INRIA-IMAG', 'HPND-Intel', 'HPND-Kevlin-Henney', 'HPND-Markus-Kuhn', 'HPND-merchantability-variant', 'HPND-MIT-disclaimer', 'HPND-Netrek', 'HPND-Pbmplus', 'HPND-sell-MIT-disclaimer-xserver', 'HPND-sell-regexpr', 'HPND-sell-variant', 'HPND-sell-variant-MIT-disclaimer', 'HPND-sell-variant-MIT-disclaimer-rev', 'HPND-UC', 'HPND-UC-export-US', 'HTMLTIDY', 'IBM-pibs', 'ICU', 'IEC-Code-Components-EULA', 'IJG', 'IJG-short', 'ImageMagick', 'iMatix', 'Imlib2', 'Info-ZIP', 'Inner-Net-2.0', 'Intel', 'Intel-ACPI', 'Interbase-1.0', 'IPA', 'IPL-1.0', 'ISC', 'ISC-Veillard', 'Jam', 'JasPer-2.0', 'JPL-image', 'JPNIC', 'JSON', 'Kastrup', 'Kazlib', 'Knuth-CTAN', 'LAL-1.2', 'LAL-1.3', 'Latex2e', 'Latex2e-translated-notice', 'Leptonica', 'LGPL-2.0-only', 'LGPL-2.0-or-later', 'LGPL-2.1-only', 'LGPL-2.1-or-later', 'LGPL-3.0-only', 'LGPL-3.0-or-later', 'LGPLLR', 'Libpng', 'libpng-2.0', 'libselinux-1.0', 'libtiff', 'libutil-David-Nugent', 'LiLiQ-P-1.1', 'LiLiQ-R-1.1', 'LiLiQ-Rplus-1.1', 'Linux-man-pages-1-para', 'Linux-man-pages-copyleft', 'Linux-man-pages-copyleft-2-para', 'Linux-man-pages-copyleft-var', 'Linux-OpenIB', 'LOOP', 'LPD-document', 'LPL-1.0', 'LPL-1.02', 'LPPL-1.0', 'LPPL-1.1', 'LPPL-1.2', 'LPPL-1.3a', 'LPPL-1.3c', 'lsof', 'Lucida-Bitmap-Fonts', 'LZMA-SDK-9.11-to-9.20', 'LZMA-SDK-9.22', 'Mackerras-3-Clause', 'Mackerras-3-Clause-acknowledgment', 'magaz', 'mailprio', 'MakeIndex', 'Martin-Birgmeier', 'McPhee-slideshow', 'metamail', 'Minpack', 'MirOS', 'MIT', 'MIT-0', 'MIT-advertising', 'MIT-CMU', 'MIT-enna', 'MIT-feh', 'MIT-Festival', 'MIT-Khronos-old', 'MIT-Modern-Variant', 'MIT-open-group', 'MIT-testregex', 'MIT-Wu', 'MITNFA', 'MMIXware', 'Motosoto', 'MPEG-SSG', 'mpi-permissive', 'mpich2', 'MPL-1.0', 'MPL-1.1', 'MPL-2.0', 'MPL-2.0-no-copyleft-exception', 'mplus', 'MS-LPL', 'MS-PL', 'MS-RL', 'MTLL', 'MulanPSL-1.0', 'MulanPSL-2.0', 'Multics', 'Mup', 'NAIST-2003', 'NASA-1.3', 'Naumen', 'NBPL-1.0', 'NCBI-PD', 'NCGL-UK-2.0', 'NCL', 'NCSA', 'NetCDF', 'Newsletr', 'NGPL', 'NICTA-1.0', 'NIST-PD', 'NIST-PD-fallback', 'NIST-Software', 'NLOD-1.0', 'NLOD-2.0', 'NLPL', 'Nokia', 'NOSL', 'Noweb', 'NPL-1.0', 'NPL-1.1', 'NPOSL-3.0', 'NRL', 'NTP', 'NTP-0', 'O-UDA-1.0', 'OAR', 'OCCT-PL', 'OCLC-2.0', 'ODbL-1.0', 'ODC-By-1.0', 'OFFIS', 'OFL-1.0', 'OFL-1.0-no-RFN', 'OFL-1.0-RFN', 'OFL-1.1', 'OFL-1.1-no-RFN', 'OFL-1.1-RFN', 'OGC-1.0', 'OGDL-Taiwan-1.0', 'OGL-Canada-2.0', 'OGL-UK-1.0', 'OGL-UK-2.0', 'OGL-UK-3.0', 'OGTSL', 'OLDAP-1.1', 'OLDAP-1.2', 'OLDAP-1.3', 'OLDAP-1.4', 'OLDAP-2.0', 'OLDAP-2.0.1', 'OLDAP-2.1', 'OLDAP-2.2', 'OLDAP-2.2.1', 'OLDAP-2.2.2', 'OLDAP-2.3', 'OLDAP-2.4', 'OLDAP-2.5', 'OLDAP-2.6', 'OLDAP-2.7', 'OLDAP-2.8', 'OLFL-1.3', 'OML', 'OpenPBS-2.3', 'OpenSSL', 'OpenSSL-standalone', 'OpenVision', 'OPL-1.0', 'OPL-UK-3.0', 'OPUBL-1.0', 'OSET-PL-2.1', 'OSL-1.0', 'OSL-1.1', 'OSL-2.0', 'OSL-2.1', 'OSL-3.0', 'PADL', 'Parity-6.0.0', 'Parity-7.0.0', 'PDDL-1.0', 'PHP-3.0', 'PHP-3.01', 'Pixar', 'pkgconf', 'Plexus', 'pnmstitch', 'PolyForm-Noncommercial-1.0.0', 'PolyForm-Small-Business-1.0.0', 'PostgreSQL', 'PPL', 'PSF-2.0', 'psfrag', 'psutils', 'Python-2.0', 'Python-2.0.1', 'python-ldap', 'Qhull', 'QPL-1.0', 'QPL-1.0-INRIA-2004', 'radvd', 'Rdisc', 'RHeCos-1.1', 'RPL-1.1', 'RPL-1.5', 'RPSL-1.0', 'RSA-MD', 'RSCPL', 'Ruby', 'Ruby-pty', 'SAX-PD', 'SAX-PD-2.0', 'Saxpath', 'SCEA', 'SchemeReport', 'Sendmail', 'Sendmail-8.23', 'SGI-B-1.0', 'SGI-B-1.1', 'SGI-B-2.0', 'SGI-OpenGL', 'SGP4', 'SHL-0.5', 'SHL-0.51', 'SimPL-2.0', 'SISSL', 'SISSL-1.2', 'SL', 'Sleepycat', 'SMLNJ', 'SMPPL', 'SNIA', 'snprintf', 'softSurfer', 'Soundex', 'Spencer-86', 'Spencer-94', 'Spencer-99', 'SPL-1.0', 'ssh-keyscan', 'SSH-OpenSSH', 'SSH-short', 'SSLeay-standalone', 'SSPL-1.0', 'SugarCRM-1.1.3', 'Sun-PPP', 'Sun-PPP-2000', 'SunPro', 'SWL', 'swrule', 'Symlinks', 'TAPR-OHL-1.0', 'TCL', 'TCP-wrappers', 'TermReadKey', 'TGPPL-1.0', 'threeparttable', 'TMate', 'TORQUE-1.1', 'TOSL', 'TPDL', 'TPL-1.0', 'TTWL', 'TTYP0', 'TU-Berlin-1.0', 'TU-Berlin-2.0', 'Ubuntu-font-1.0', 'UCAR', 'UCL-1.0', 'ulem', 'UMich-Merit', 'Unicode-3.0', 'Unicode-DFS-2015', 'Unicode-DFS-2016', 'Unicode-TOU', 'UnixCrypt', 'Unlicense', 'UPL-1.0', 'URT-RLE', 'Vim', 'VOSTROM', 'VSL-1.0', 'W3C', 'W3C-19980720', 'W3C-20150513', 'w3m', 'Watcom-1.0', 'Widget-Workshop', 'Wsuipa', 'WTFPL', 'X11', 'X11-distribute-modifications-variant', 'X11-swapped', 'Xdebug-1.03', 'Xerox', 'Xfig', 'XFree86-1.1', 'xinetd', 'xkeyboard-config-Zinoviev', 'xlock', 'Xnet', 'xpp', 'XSkat', 'xzoom', 'YPL-1.0', 'YPL-1.1', 'Zed', 'Zeeff', 'Zend-2.0', 'Zimbra-1.3', 'Zimbra-1.4', 'Zlib', 'zlib-acknowledgement', 'ZPL-1.1', 'ZPL-2.0', 'ZPL-2.1'}

def generate_sbom(conanfile, out_file, **kwargs):
    name = conanfile.ref.name
    version = conanfile.ref.version
    date = datetime.fromtimestamp(time.time(), tz=timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')
    packages = []

    for dependency in [conanfile] + conanfile.dependencies.values():
        packages.append(
            {
                "name": dependency.ref.name,
                "SPDXID": f"SPDXRef-{dependency.ref}",
                "version": str(dependency.ref.version),
                "license": dependency.license if dependency.license in spdx_licences else "NOASSERTION",
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
        with open(out_path, 'w') as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        ConanException("error generating spdx file")

"""


def migrate_sbom_file(cache_folder):
    from conans.client.migrations import update_file
    sbom_path = HomePaths(cache_folder).sbom_manifest_plugin_path
    update_file(sbom_path, _default_spdx_json)
