"""Line magics personalizados para notebooks del workshop."""

from __future__ import annotations

import importlib
import os
import sys
from datetime import datetime
from pathlib import Path

from IPython.display import display


def _resolve_var(shell, name: str):
    """Busca una variable en el namespace del kernel."""
    if name in shell.user_ns:
        return shell.user_ns[name]
    raise NameError(f"La variable '{name}' no está definida en el notebook.")


def memory_usage(line: str) -> None:
    """Muestra el uso de RAM del proceso actual (MB)."""
    try:
        import resource

        usage_kb = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
        # macOS reporta bytes; Linux reporta kilobytes
        usage_mb = usage_kb / (1024 * 1024) if sys.platform == "darwin" else usage_kb / 1024
        print(f"RAM máxima usada por este proceso: {usage_mb:.2f} MB")
    except ImportError:
        print("No se pudo leer el uso de memoria en este sistema.")


def env_vars(line: str) -> None:
    """Lista variables de entorno (o muestra una concreta)."""
    name = line.strip()
    if name:
        value = os.environ.get(name)
        if value is None:
            print(f"Variable '{name}' no definida.")
        else:
            print(f"{name}={value}")
        return

    for key in sorted(os.environ):
        print(f"{key}={os.environ[key]}")


def show_pwd(line: str) -> None:
    """Muestra el directorio de trabajo actual."""
    print(Path.cwd())


def check_aws_creds(line: str) -> None:
    """Verifica si hay credenciales AWS configuradas."""
    hints = []
    if os.environ.get("AWS_ACCESS_KEY_ID") and os.environ.get("AWS_SECRET_ACCESS_KEY"):
        hints.append("Variables AWS_ACCESS_KEY_ID / AWS_SECRET_ACCESS_KEY encontradas.")
    if os.environ.get("AWS_PROFILE"):
        hints.append(f"Perfil AWS_PROFILE={os.environ['AWS_PROFILE']}")
    if Path.home().joinpath(".aws", "credentials").exists():
        hints.append("Archivo ~/.aws/credentials encontrado.")

    if hints:
        print("AWS: credenciales detectadas.")
        for hint in hints:
            print(f"  - {hint}")
    else:
        print("AWS: no se detectaron credenciales comunes.")


def check_gcp_creds(line: str) -> None:
    """Verifica si hay credenciales GCP configuradas."""
    hints = []
    adc = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    if adc and Path(adc).exists():
        hints.append(f"GOOGLE_APPLICATION_CREDENTIALS apunta a {adc}")
    if Path.home().joinpath(".config", "gcloud", "application_default_credentials.json").exists():
        hints.append("ADC de gcloud encontrado en ~/.config/gcloud/")
    if os.environ.get("CLOUDSDK_CORE_PROJECT"):
        hints.append(f"Proyecto: {os.environ['CLOUDSDK_CORE_PROJECT']}")

    if hints:
        print("GCP: credenciales detectadas.")
        for hint in hints:
            print(f"  - {hint}")
    else:
        print("GCP: no se detectaron credenciales comunes.")


def check_azure_creds(line: str) -> None:
    """Verifica si hay credenciales Azure configuradas."""
    hints = []
    for key in ("AZURE_CLIENT_ID", "AZURE_TENANT_ID", "AZURE_CLIENT_SECRET"):
        if os.environ.get(key):
            hints.append(f"{key} definida.")
    if Path.home().joinpath(".azure").exists():
        hints.append("Directorio ~/.azure encontrado (Azure CLI).")

    if hints:
        print("Azure: credenciales detectadas.")
        for hint in hints:
            print(f"  - {hint}")
    else:
        print("Azure: no se detectaron credenciales comunes.")


def df_info(line: str) -> None:
    """Muestra información de un DataFrame (requiere pandas)."""
    import pandas as pd

    name = line.strip()
    if not name:
        print("Uso: %df_info nombre_variable")
        return

    shell = get_ipython()
    obj = _resolve_var(shell, name)
    if not isinstance(obj, pd.DataFrame):
        print(f"'{name}' no es un pandas.DataFrame (es {type(obj).__name__}).")
        return

    obj.info()


def df_preview(line: str) -> None:
    """Muestra las primeras filas de un DataFrame."""
    import pandas as pd

    name = line.strip()
    if not name:
        print("Uso: %df_preview nombre_variable")
        return

    shell = get_ipython()
    obj = _resolve_var(shell, name)
    if not isinstance(obj, pd.DataFrame):
        print(f"'{name}' no es un pandas.DataFrame (es {type(obj).__name__}).")
        return

    display(obj.head())


def clear_cache(line: str) -> None:
    """Recarga módulos importados en el kernel (útil tras editar .py)."""
    reloaded = []
    for name, module in list(sys.modules.items()):
        if module is None or not hasattr(module, "__file__") or module.__file__ is None:
            continue
        if "site-packages" in module.__file__ or "dist-packages" in module.__file__:
            continue
        try:
            importlib.reload(module)
            reloaded.append(name)
        except Exception:
            pass

    if reloaded:
        print(f"Módulos recargados ({len(reloaded)}): {', '.join(sorted(reloaded)[:10])}")
        if len(reloaded) > 10:
            print(f"  ... y {len(reloaded) - 10} más")
    else:
        print("No había módulos del proyecto para recargar.")


def timestamp(line: str) -> None:
    """Muestra la fecha y hora actual."""
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


def trace_var(line: str) -> None:
    """Inspecciona tipo, valor y tamaño de una variable."""
    name = line.strip()
    if not name:
        print("Uso: %trace_var nombre_variable")
        return

    shell = get_ipython()
    obj = _resolve_var(shell, name)
    print(f"Variable: {name}")
    print(f"  Tipo:   {type(obj).__name__}")
    print(f"  Valor:  {obj!r}")
    try:
        print(f"  Tamaño: {len(obj)}")
    except TypeError:
        pass


def list_vars(line: str) -> None:
    """Lista variables definidas por el usuario en el notebook."""
    shell = get_ipython()
    ignore = {"In", "Out", "get_ipython", "exit", "quit", "open"}
    user_vars = {
        name: type(value).__name__
        for name, value in shell.user_ns.items()
        if not name.startswith("_") and name not in ignore and not name.isupper()
    }

    if not user_vars:
        print("No hay variables de usuario definidas todavía.")
        return

    print(f"{'Variable':<20} {'Tipo'}")
    print("-" * 32)
    for name in sorted(user_vars):
        print(f"{name:<20} {user_vars[name]}")


_MAGICS = {
    "memory_usage": memory_usage,
    "env_vars": env_vars,
    "show_pwd": show_pwd,
    "check_aws_creds": check_aws_creds,
    "check_gcp_creds": check_gcp_creds,
    "check_azure_creds": check_azure_creds,
    "df_info": df_info,
    "df_preview": df_preview,
    "clear_cache": clear_cache,
    "timestamp": timestamp,
    "trace_var": trace_var,
    "list_vars": list_vars,
}


def load_ipython_extension(ipython) -> None:
    """Registra todos los line magics en el kernel activo."""
    for name, func in _MAGICS.items():
        ipython.register_magic_function(func, "line", name)


def unload_ipython_extension(ipython) -> None:
    """Elimina los magics del kernel."""
    for name in _MAGICS:
        ipython.magics_manager.magics["line"].pop(name, None)
