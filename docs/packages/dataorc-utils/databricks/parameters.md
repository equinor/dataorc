# Parsing wheel-task arguments

When running Python wheel tasks in Databricks jobs, we set parameters as part of the config on a task. Use `parse_args` to quickly define and parse them.

## Signature

`parse_args(description, arguments)`

Parameters:

- `description` (str): Description shown in the help output.
- `arguments` (list[str] | dict[str, bool]): Either a list of argument names (all required), 
  or a dict mapping argument names to boolean `required` flags. Each name becomes a `--name` CLI flag.

Returns an `argparse.Namespace` with each argument accessible as an attribute.

## Example 1: All required arguments (list)

```python
from dataorc_utils.databricks import parse_args

def main():
    args = parse_args("ETL Job", ["database", "schema", "table"])
    print(f"Running on {args.database}.{args.schema}.{args.table}")

if __name__ == "__main__":
    main()
```

When the Databricks job is configured with parameters
`["--database", "analytics", "--schema", "public", "--table", "events"]`,
the script will print:

```text
Running on analytics.public.events
```

## Example 2: Mixed required and optional arguments (dict)

```python
from dataorc_utils.databricks import parse_args

def main():
    args = parse_args("ETL Job", {
        "database": True,   # required
        "schema": False,    # optional
        "mode": False       # optional
    })
    
if __name__ == "__main__":
    main()
```
