# sschema
sschema is a Python module to facilitate checking YAML schemas in an extensible
way. Although the schemas are represented in YAML, it internally uses jsonschema.

In addition, sschema provides a number of prewritten schemas (e.g. for things
like units and types) that can be included in other projects in order to
facilitate code reuse and standardize on a common schema format for projects
using sschema.
