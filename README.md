# TestMigrationsInPy

🖖 Welcome to **TestMigrationsInPy**!

This repository provides a curated dataset focused on supporting research related to migrating Python test suites from the **unittest** to **pytest** frameworks. It draws upon a selection of 100 top Python projects, carefully chosen to exclude non-software projects like tutorials, examples, and samples. 

## How to Navigate

To facilitate your exploration of the dataset, here is an overview of the repository structure and how to navigate through:
```plaintext
projects/
└── projectName/
    ├── diff/
    │   ├── migN-before-testFileName.py
    │   └── migN-after-testFileName.py
    └── output.info
```

### 📁 `projects/`

Within the `projects` directory, you will find repositories from some of the top 100 Python projects on GitHub that include migrations from `unittest` to `pytest`. Each project is organized into its own folder, named after the repository. Examples of projects available in this dataset include `airflow`, `pandas`, `requests`, and `redis`.

### 📂 `projectName/` - Project Folder Contents

Inside each project folder, you will find a well-structured organization that facilitates easy navigation and understanding of the migration process. The contents are as follows:

* **Sequentially Numbered Folders:** These folders are numbered sequentially and correspond to specific commits in the project's history that involve migration activities. Each of these folders contains:
  * `output.info`: This file provides detailed information about the commit and the associated migration, offering valuable context for researchers analyzing the dataset.
  * `diff/`: This subdirectory contains the migration files, which are split into before-and-after versions to clearly illustrate the changes made during the migration.
    * **migN-before-fileName.py:** Represents the state of the test file using the unittest framework before the migration to pytest.
    * **migN-after-fileName.py:** Represents the state of the test file after it has been migrated to pytest.

**NOTE:** It is important to notice that a migration commit may have one or more migrations. We focused on detecting isolated migrations, that is, migrations that simply replace unittest with pytest, and no other unrelated changes are involved.

Happy navigating and researching! 🚀
