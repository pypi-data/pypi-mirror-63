# aioimport
Asynchronous module import for asyncio

## Getting Started

### Installing

Install from [PyPI](https://pypi.org/project/aioimport/) using:

```
pip install aioimport
```

### The problem

Some naughty modules have long running operations during import

#### Naive solution

First thing that comes to mind is make import local:

```python
async def my_work() -> None:
    import naughty  # will block event loop
```

It reduces time your program takes to start (or library to import),
but it is still blocking your event loop.

### Usage

```python
import aioimport

async def my_work() -> None:
    await aioimport.import_module("naughty")  # will asynchronously import module
    import naughty  # will be instantaneous since `naughty` is already in `sys.modules`
    await aioimport.reload(naughty)  # and you can asynchronously modules too
```

### How it works

Module import is done in asyncio default executor.

Be aware of the fact that GIL still exists and technically import is done concurrently rather than in parallel with your code.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
