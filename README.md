# Generated Web Application

## Description
You are given two attachments: execute.py and data.xlsx.

- Commit execute.py after fixing the non-trivial error in it.
- Ensure it runs on Python 3.11+ with Pandas 2.3.
- Convert data.xlsx to data.csv and commit it.
- Add a GitHub Actions push workflow at .github/workflows/ci.yml that:
  - Runs ruff and shows its results in the CI log
  - Runs: python execute.py > result.json
  - Publishes result.json via GitHub Pages
- Do not commit result.json; it must be generated in CI.

## Requirements
- execute.py, data.csv, and .github/workflows/ci.yml exist\n- result.json is NOT committed\n- execute.py does not contain the typo "revenew"\n- data.csv content equals data.xlsx (attachment)\n- CI YAML has steps for ruff, executing execute.py, and Pages deploy\n- GitHub Actions ran for this commit and logs show ruff + execute.py\n- result.json is published on GitHub Pages

## Setup
1. Clone this repository
2. Open `index.html` in a web browser

## Usage
This application was generated based on the provided brief and requirements.

## License
MIT License - see LICENSE file for details
