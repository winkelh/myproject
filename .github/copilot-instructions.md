# Copilot Instructions for myproject

## Project Overview
This is a Python **learning and sandbox repository** for experimenting with Python concepts and algorithms. It contains individual learning scripts rather than a unified application.

## Running Python Files
- **Run a single script**: `python <filename>.py` (e.g., `python HelloWorld.py`)
- **Interactive mode**: `python -i <filename>.py` to load a script and stay in the Python REPL
- **Python version**: Project requires Python 3.14+

## Dependency Management
- **Package manager**: Poetry
- **View dependencies**: `poetry show`
- **Add a package**: `poetry add <package-name>`
- **Install dependencies**: `poetry install`

## Project Structure

### Core Learning Modules
- **`person.py` / `student.py`**: Class inheritance examples. `Student` extends `Person` with additional attributes and methods.
- **`PersonClassUser.py`**: Demonstrates instantiation and method calls on the inheritance hierarchy.

### Algorithm Implementations
- **`DijkstrasAlgoritm.py`**: Graph class with incomplete Dijkstra's algorithm implementation. Uses adjacency list representation (`nodes` dict with neighbours).
- **`dict.py`**: Graph representations and basic data structure exploration (sets, lists, dictionaries).
- **`dc_Dijkstra.py`**: Related algorithm exploration (check for alternative implementation patterns).

### Basic Learning Scripts
- **`HelloWorld.py`**: Arithmetic operators, basic conditionals
- **`math_flshcards.py`**, **`image_display.py`**: General Python feature exploration
- **`ClassMultiInheritance.py`**: Multi-level inheritance patterns

### Resources
- **`resources/`**: Image assets (grass tiles, water, RPG tileset) and text files (database notes)

## Key Conventions

### Class Design
- Classes follow simple object-oriented patterns with `__init__` and method definitions
- Inheritance is used for specialization (e.g., `Student(Person)`)
- No type hints are used (bare parameters and return types)

### Graph/Algorithm Implementation
- **Graph representation**: Dictionary of nodes with visited status and neighbours
- **Node structure**: `{name: {"visited": bool, "neighbours": {node_name: weight}}}`
- Note: Some implementations are incomplete or exploratory; they may be refactored as learning progresses

### Naming Quirks
- `DijkstrasAlgoritm.py` has a typo in the filename (Algoritm vs Algorithm)
- Variable names like `ed` for graph instances are short and informal (typical of sandbox code)

## No Automated Testing or Linting
This is a learning repository without CI/CD, automated tests, or linting. When adding code:
- Keep scripts self-contained or import from existing modules as shown in `PersonClassUser.py`
- Test interactively by running scripts directly
