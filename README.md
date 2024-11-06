# TestMigrationsInPy

🖖 Welcome to **TestMigrationsInPy**!

This repository provides a curated dataset focused on supporting research related to migrating Python test suites from the **unittest** framework to **pytest**. It draws upon a selection of 100 top Python projects, carefully chosen to exclude non-software projects like tutorials, examples, and samples.

## Repository Structure: How to Navigate

To facilitate your exploration of the dataset, here is an overview of the repository structure and how to navigate through it:

### `projects/` Directory

Within the `projects` directory, you will find the repositories of some of the top 100 Python projects on GitHub that include migrations from the _unittest_ to _pytest_. Each project is contained in its own folder named after the repository.

### Project Folder Contents

Within each project folder, you will encounter folders numbered sequentially. These folders correspond to specific commits of the project that involve migration activities.

### Commit Folder Structure

Inside each commit folder, you will find:

- **`metadata` file**: This file contains detailed information about the commit and the associated migration.
- **`diff/` directory**: This directory includes the migration files, structured as follows:
  - `migN-before/after-namedoftestfilewithmigration.py`: These files represent the state of the test file before and after the migration.
  
Each migration is individual and pertains to a specific point of migration, making it easy to track and analyze the changes.

By following this structure, you can efficiently navigate through the dataset and access the information you need for your research on Python test suite migrations.
