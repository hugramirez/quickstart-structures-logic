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

## Usar los notebooks

### Empezar aquí (Módulo 1 — ~45 min)

Si conoces poco Python, abre primero **`quickstart_structures_logic.ipynb`**: listas y diccionarios explicados paso a paso con acordes.

Luego continúa con **`workshop_hands_on.ipynb`** (iteraciones, funciones y hands-on del mástil).

**Opcional (~15 min):** [`functions_and_design.ipynb`](functions_and_design.ipynb) — repaso de funciones y principio SRP/OCP con el código del taller.

### Opción 1 — JupyterLab (recomendado)

```bash
uv run jupyter lab
```

Abre los notebooks en el navegador y ejecuta las celdas en orden.

### Opción 2 — Cursor / VS Code

1. Ejecuta `uv sync` para crear el entorno `.venv`.
2. Selecciona el intérprete `.venv/bin/python` como kernel del notebook.
3. Abre `quickstart_structures_logic.ipynb` o `workshop_hands_on.ipynb` y ejecuta las celdas.

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
├── quickstart_structures_logic.ipynb   # Módulo 1: listas y diccionarios
├── workshop_hands_on.ipynb             # Módulos 2–4: mástil, bucles, funciones
├── functions_and_design.ipynb          # Opcional: funciones y SRP/OCP
├── src/
│   ├── generate_fretboard.py           # Generador del diagrama EADGBE
│   └── image.png                       # Imagen de referencia del mástil
├── pyproject.toml                      # Dependencias (uv)
└── uv.lock                             # Lockfile reproducible
```
