# Project README

## Project Overview

This project is designed to facilitate the development, testing, and evaluation of text analytics models using a consistent and reproducible approach. The project structure includes directories for data storage (`data`), model development (`models`), generic scripts (`scripts`), and testing (`tests`).

## Project Structure

```
project-root/
│
├── data/
│   ├── doccano_export/
│   ├── predictions/
│   ├── processed/
│   └── raw/
│
├── models/
│   └── template.py
│
├── scripts/
│
└── tests/
```

### `data/`

The `data` directory is organized into subdirectories for managing different stages of data processing:

- `doccano_export/`: Storage for the original exported doccano data.
- `predictions/`: Location for saving model predictions.
- `processed/`: Training, dev, and testing files.
- `raw/`: Combined doccano data for each project that is slightly processed.

### `models/`

The `models` directory contains a `template.py` file meant to be edited and expanded upon to create text analytics models. You can use this template as a starting point for building custom models.

### `scripts/`

The `scripts` directory contains generic functions that can be reused across the project. These functions are designed to help with data organization, preprocessing, and model evaluation.

### `tests/`

The `tests` directory is reserved for unit tests and test data. Writing tests for the project ensures that modifications and additions do not break existing functionality.

## Getting Started

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/edalatma/sdg_text_analytics.git
   cd your-project
   ```

2. **Install Tox:**
   ```bash
   pip install tox
   ```

3. **Run Tox:**
   
   Execute the following command to run tests and setup directories using Tox:
   ```bash
   tox
   ```

   This command will create virtual environments, install dependencies, and execute tests for the specified Python versions.

