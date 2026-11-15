# gitstat

Analyze git repositories from your terminal. Stats, contributors, hotspots, branches, tags. Zero dependencies, pure Python stdlib.

## Install

```bash
pip install gitstat
```

Or run directly:

```bash
python gitstat.py --help
```

## Usage

```bash
# Repository stats
gitstat stats

# Contributors
gitstat contributors

# Most changed files
gitstat hotspots -n 10

# Branches
gitstat branches

# Tags
gitstat tags

# Recent commits
gitstat recent -n 5
```

## License

MIT