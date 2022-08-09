# Copyright (C) 2022  Max Wiklund
#
# Licensed under the Apache License, Version 2.0 (the “License”);
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an “AS IS” BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import tempfile
import os

import textwrap
import subprocess
import shutil


def create_and_run_shell(config_name: str):
    """Configure jam shell.

    Args:
        config_name: Jam config name.

    """
    old_home = os.getenv("HOME")

    # Create temp directory for bash files.
    temp_home_dir = tempfile.mkdtemp(prefix="jam_")

    bashrc_path = os.path.join(temp_home_dir, ".bashrc")
    bash_content = textwrap.dedent(
        f"""
    #!/usr/bin/bash
    export HOME="{old_home}"
    export JAM_ENV={config_name}
    . "{old_home}/.bashrc"
    export JAM_STORED_PROMPT_SH="$PS1"
    export PS1="($JAM_ENV) $JAM_STORED_PROMPT_SH"
    echo "You are now editing $JAM_ENV Jam config."
    echo ""
    """
    )
    with open(bashrc_path, "w") as f:
        f.write(bash_content)

    jam_shell_path = os.path.join(temp_home_dir, "jam-shell")

    jam_shell_content = textwrap.dedent(
        f"""
    #!/usr/bin/bash
    export HOME="{temp_home_dir}"
    /usr/bin/bash
    exit $?
    """
    )
    with open(jam_shell_path, "w") as f:
        f.write(jam_shell_content)
    os.chmod(jam_shell_path, mode=0o775)

    subprocess.run(jam_shell_path, shell=True)
    shutil.rmtree(temp_home_dir)  # Clean up.
