# Parsing wheel-task arguments

When running Python wheel tasks in Databricks jobs, we set parameters as part of the config on a task. Use `parse_args` to quickly define and parse them.

## Signature

`parse_args(description, arguments)`

Parameters:

- `description` (str): Description shown in the help output.
- `arguments` (list[str]): List of argument names to parse. Each name becomes a
  required `--name` CLI flag.

Returns an `argparse.Namespace` with each argument accessible as an attribute.

## Example (wheel task entry point)

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
