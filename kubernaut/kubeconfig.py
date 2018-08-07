import os

from kubernaut.util import strip_margin
from pathlib import Path


def write_kubeconfig(kubeconfig_data: str, path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(kubeconfig_data)


def kubeconfig_message(path: Path) -> str:
    shell_type = os.getenv("SHELL", "sh")

    env_var_export_cmd = "export KUBECONFIG="
    if "csh" in shell_type:
        env_var_export_cmd = "setenv KUBECONFIG "
    elif "fish" in shell_type:
        env_var_export_cmd = "set -x KUBECONFIG "

    msg = strip_margin("""
    | Your clusters kubeconfig has been written to the below path:
    | 
    | {0}
    | 
    | Usage Instructions:
    |
    | There are several ways you can use this kubeconfig file:
    |
    | 1. Pass --kubeconfig to the `kubectl` command:
    |
    |    kubectl --kubeconfig={0} ...
    |
    | 2. Set the KUBECONFIG environment variable:
    |
    |    {1}{0}
    """.format(str(path), env_var_export_cmd))

    return msg
