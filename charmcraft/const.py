# Copyright 2023 Canonical Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# For further info, check https://github.com/canonical/charmcraft

"""Constants used in charmcraft."""

# region Environment variables
ALTERNATE_AUTH_ENV_VAR = "CHARMCRAFT_AUTH"
DEVELOPER_MODE_ENV_VAR = "CHARMCRAFT_DEVELOPER"
EXPERIMENTAL_EXTENSIONS_ENV_VAR = "CHARMCRAFT_ENABLE_EXPERIMENTAL_EXTENSIONS"
IMAGE_INFO_ENV_VAR = "CHARMCRAFT_IMAGE_INFO"
PROVIDER_ENV_VAR = "CHARMCRAFT_PROVIDER"
SHARED_CACHE_ENV_VAR = "CRAFT_SHARED_CACHE"

# These are only for use within the managed environment
MANAGED_MODE_ENV_VAR = "CHARMCRAFT_MANAGED_MODE"
SNAP_CHANNEL_ENV_VAR = "CHARMCRAFT_INSTALL_SNAP_CHANNEL"
# endregion
# region Project files and directories
CHARMCRAFT_FILENAME = "charmcraft.yaml"
BUNDLE_FILENAME = "bundle.yaml"
MANIFEST_FILENAME = "manifest.yaml"
METADATA_FILENAME = "metadata.yaml"
JUJU_ACTIONS_FILENAME = "actions.yaml"
JUJU_CONFIG_FILENAME = "config.yaml"
WORK_DIRNAME = "work_dir"
BUILD_DIRNAME = "build"
VENV_DIRNAME = "venv"
STAGING_VENV_DIRNAME = "staging-venv"
# endregion
# region Output files and directories
# Dispatch script filename
DISPATCH_FILENAME = "dispatch"
# Hooks directory name
HOOKS_DIRNAME = "hooks"
# The minimum set of hooks to be provided for compatibility with old Juju
MANDATORY_HOOK_NAMES = frozenset(("install", "start", "upgrade-charm"))

# The minimum set of files for a charm to be considered valid
CHARM_MANDATORY_FILES = frozenset(
    (
        DISPATCH_FILENAME,
        HOOKS_DIRNAME,
    )
)
# Optional files that can be present in a charm
CHARM_OPTIONAL_FILES = frozenset(
    (
        METADATA_FILENAME,
        JUJU_ACTIONS_FILENAME,
        JUJU_CONFIG_FILENAME,
        "metrics.yaml",
        "lxd-profile.yaml",
        "templates",
        "version",
        "lib",
        "mod",
        "LICENSE",
        "icon.svg",
        "README.md",
        "actions",
    )
)
# endregion

DEPENDENCIES_HASH_FILENAME = "charmcraft-dependencies-hash.txt"

# If Juju doesn't support the dispatch mechanism, it will execute the
# hook, and we'd need sys.argv[0] to be the name of the hook but it's
# getting lost by calling this dispatch, so we fake JUJU_DISPATCH_PATH
# to be the value it would've otherwise been.
DISPATCH_CONTENT = """#!/bin/sh

JUJU_DISPATCH_PATH="${{JUJU_DISPATCH_PATH:-$0}}" PYTHONPATH=lib:venv \\
  exec ./{entrypoint_relative_path}
"""

UBUNTU_LTS_STABLE = frozenset(
    (
        "18.04",
        "20.04",
        "22.04",
    )
)

# Metadata keys that are defined in the metadata.yaml file, for backwards compatible
CHARM_METADATA_LEGACY_KEYS = frozenset(
    (
        "assumes",
        "containers",
        "description",
        "devices",
        "display-name",
        "docs",
        "extra-bindings",
        "issues",
        "maintainers",
        "name",
        "peers",
        "provides",
        "requires",
        "resources",
        "series",
        "storage",
        "subordinate",
        "summary",
        "terms",
        "website",
    )
)

CHARM_METADATA_LEGARY_KEYS_ALIAS = frozenset(
    (
        "display_name",
        "extra_bindings",
    )
)

# Metadata keys that are allowed in the charmcraft.yaml file
CHARM_METADATA_KEYS = frozenset(
    (
        "assumes",
        "containers",
        "description",
        "devices",
        "title",
        "documentation",
        "extra-bindings",
        "links",
        "name",
        "peers",
        "provides",
        "requires",
        "resources",
        "storage",
        "subordinate",
        "summary",
        "terms",
    )
)

CHARM_METADATA_KEYS_ALIAS = frozenset(("extra_bindings",))
