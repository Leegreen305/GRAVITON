# Contributing to GRAVITON

Thank you for your interest in contributing to GRAVITON. This project aims to maintain the highest standards of scientific accuracy.

## Ground Rules

1. **Every equation must have a citation.** If you add new physics, include a reference to a peer-reviewed paper, textbook, or arXiv preprint.

2. **No speculative physics without citations.** GRAVITON simulates what the equations of GR and QFT actually predict, not what we wish they predicted.

3. **Tests are mandatory.** Every new physics module must include pytest tests that verify:
   - Correct signs (e.g., negative energy density for exotic matter)
   - Correct scaling laws (e.g., 1/r^2 for gravity)
   - Limiting cases (e.g., Kerr reduces to Schwarzschild at a=0)
   - Comparison with known analytical or experimental results where possible

4. **SI units everywhere.** All physical quantities must be in SI units with clear documentation.

## Development Setup

```bash
git clone https://github.com/YOUR_USERNAME/GRAVITON.git
cd GRAVITON
pip install -r requirements.txt
python -m pytest tests/ -v
```

## Pull Request Process

1. Fork the repository and create a feature branch.
2. Implement your changes with appropriate docstrings and citations.
3. Write tests for all new functionality.
4. Ensure all tests pass: `python -m pytest tests/ -v`
5. Submit a pull request with a clear description of the physics being added.

## Module Structure

Each physics module should follow this pattern:

```
module_name/
├── __init__.py        # Exports
├── physics.py         # Core physics computation
├── visualizer.py      # Visualization (Matplotlib/Plotly)
└── README.md          # Module-specific documentation with citations
```

## Code Style

- Python 3.10+ type hints
- NumPy-style docstrings
- Physical constants imported from `graviton.constants`
- Clear variable names that match the physics notation (e.g., `r_s` for Schwarzschild radius)

## Reporting Issues

If you find a physics error, please open an issue with:
- The specific equation or computation that is incorrect
- The correct equation with a citation
- A test case demonstrating the discrepancy
