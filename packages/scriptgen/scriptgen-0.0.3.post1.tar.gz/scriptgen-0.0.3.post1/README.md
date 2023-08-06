[//]: # (Auto-generated: 2020-03-16T04:57:46.722755)

# scriptgen

[//]: # (badges)
[![Repo](https://img.shields.io/badge/repo-github-brightgreen)](https://github.com/Fopoon/scriptgen)
[![Version](https://img.shields.io/badge/version-0.0.3.post1-brightgreen.svg)](https://github.com/Fopoon/scriptgen/releases)
![PyPI](https://img.shields.io/pypi/v/scriptgen)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/scriptgen)
![PyPI - Status](https://img.shields.io/pypi/status/scriptgen)
![PyPI - License](https://img.shields.io/pypi/l/scriptgen)
![PyPI - Format](https://img.shields.io/pypi/format/scriptgen)
![PyPI - Downloads](https://img.shields.io/pypi/dm/scriptgen)

A collection of script generation helpers and templates.

## Installation

```sh
pip install scriptgen
```

## Usage

```python
from scriptgen import StringBuilder


if __name__ == "__main__":
    # Create a StringBuilder instance.
    sb = StringBuilder()

    sb.wt("Hello ")  # write text "Hello "
    sb.wl("World!")  # write line "World!\n"

    print(str(sb))
```

```
Hello World!

```

<hr/>

```python
from scriptgen import StringBuilder

from scriptgen.templates.csharp import \
    csharp_usings, \
    csharp_namespace, \
    csharp_class, \
    csharp_method


if __name__ == "__main__":
    # Create a StringBuilder instance.
    sb = StringBuilder()

    # Write using statements.
    sb.wb(csharp_usings(
        "System"
    ))

    # Add a new line after the using statements.
    sb.nl()

    # Create a namespace StringBuilder instance.
    ns = csharp_namespace("Sample")

    # Create a class StringBuilder instance.
    c = csharp_class(
        class_name="Program",
        access_modifier="public"
    )

    # Create a method StringBuilder instance.
    m = csharp_method(
        method_name="Main",
        access_modifier="public static",
        return_type="int"
    )

    # Write the following lines inside the method.
    m.wl('Console.WriteLine("Hello World!");')
    m.wl("return 0;")

    c.wb(m)  # Write the method inside the class.
    ns.wb(c)  # Write the class inside the namespace.
    sb.wb(ns)  # Write the namespace.

    print(str(sb))

```

```csharp
using System;

namespace Sample
{
    public class Program
    {
        public static int Main()
        {
            Console.WriteLine("Hello World!");
            return 0;
        }
    }
}

```

<hr/>

```python
from scriptgen import StringBuilder

from scriptgen.templates.csharp import \
    csharp_autogen, \
    csharp_namespace, \
    csharp_class, \
    csharp_region


if __name__ == "__main__":
    # Get version from arguments..
    # i.e. python script.py -major 0 -minor 0 -patch 1
    major: int = 0
    minor: int = 0
    patch: int = 1

    # Create a StringBuilder instance.
    sb = StringBuilder()

    # Write timestamp.
    sb.wb(csharp_autogen())

    # Add a new line after the using statements.
    sb.nl()

    # Create a namespace StringBuilder instance.
    ns = csharp_namespace("Sample")

    # Create a class StringBuilder instance.
    c = csharp_class(
        class_name="BuildInfo",
        access_modifier="public static partial"
    )

    # Create a "Constants" region StringBuilder instance.
    r = csharp_region("Constants")

    # Write the following lines inside the "Constants" region.
    r.wl(f"public const int MAJOR = {major};")
    r.nl()
    r.wl(f"public const int MINOR = {minor};")
    r.nl()
    r.wl(f"public const int PATCH = {patch};")

    c.wb(r)  # Write the region inside the class.
    ns.wb(c)  # Write the class inside the namespace.
    sb.wb(ns)  # Write the namespace.

    print(str(sb))

```

```csharp
// Auto-generated: 2020-03-15T04:20:47.909851

namespace Sample
{
    public static partial class BuildInfo
    {
        #region Constants
        
        public const int MAJOR = 0;
        
        public const int MINOR = 0;
        
        public const int PATCH = 1;
        
        #endregion Constants
    }
}

```

<hr/>

Look at this [script](tools/gen_docs.py) to see its practical use case.

## Contribution

Suggestions and contributions are always welcome.
Make sure to read the [Contribution Guidelines](CONTRIBUTING.md) file for more information before submitting a `pull request`.

## License

`scriptgen` is released under the MIT License. See the [LICENSE](LICENSE.txt) file for details.
