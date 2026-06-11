# quickstart-structures-logic

Workshop hands-on de **estructuras de datos y lógica en Python**, usando el mástil de guitarra en afinación **EADGBE** como ejemplo práctico.

## Requisitos

- [uv](https://docs.astral.sh/uv/) instalado
- Python ≥ 3.12

## Configuración

```bash
# Clonar e instalar dependencias (incluye JupyterLab)
git clone https://github.com/hugramirez/quickstart-structures-logic.git
cd quickstart-structures-logic
uv sync
```

## Usar el notebook

### Opción 1 — JupyterLab (recomendado)

```bash
uv run jupyter lab
```

Abre `quickstart_structures_logic.ipynb` en el navegador y ejecuta las celdas.

### Opción 2 — Cursor / VS Code

1. Ejecuta `uv sync` para crear el entorno `.venv`.
2. Selecciona el intérprete `.venv/bin/python` como kernel del notebook.
3. Abre `quickstart_structures_logic.ipynb` y ejecuta las celdas.

### Opción 3 — Google Colab

Sube el `.ipynb` y la carpeta `src/` a [Google Colab](https://colab.research.google.com/). Colab ya incluye matplotlib; no necesitas uv.

## Comandos útiles

```bash
# Regenerar la imagen del mástil
uv run python src/generate_fretboard.py

# Añadir una dependencia nueva
uv add nombre-paquete

# Añadir dependencia de desarrollo
uv add --dev nombre-paquete

# Ejecutar cualquier script con el entorno del proyecto
uv run python tu_script.py
```

## Estructura

```
├── quickstart_structures_logic.ipynb   # Notebook principal
├── src/
│   ├── generate_fretboard.py           # Generador del diagrama EADGBE
│   └── image.png                       # Imagen de referencia del mástil
├── pyproject.toml                      # Dependencias (uv)
└── uv.lock                             # Lockfile reproducible
```
