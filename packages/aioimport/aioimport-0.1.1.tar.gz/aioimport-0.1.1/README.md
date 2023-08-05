# aioimport
Asynchronous module import for asyncio

## Getting Started

### Installing

Install from [PyPI](https://pypi.org/project/aioimport/) using:

```
pip install aioimport
```

### The problem

Some nasty modules have long running operations during import

### The naive solution

First thing that comes to mind is to postpone import by moving it into the function that need that module:

```python
async def my_work(self) -> None:
    import this  # will block until imported
```

It reduces your startup time, but it is still blocking your event loop.

That's where `aioimport` comes in.

### Usage

The preferred way to use `aioimport` is:
```python
import aioimport

async def my_work(self) -> None:
    await aioimport.cache_module("this")  # will asynchronously import module
    import this  # will be instantaneous since `this` is already in import cache 
```

Also `aioimport` can be also used the following way:
```python
import aioimport

async def my_work(self) -> None:
    this = await aioimport.import_module("this")  # will asynchronously import module
    # now `this` has exactly the same module as you would have gotten be doing `import this`
```
But your types will be all messed up.

### How it works

Module import is done in thread executor.

Be aware of the fact that GIL still exists and technically import is done concurrently rather than in parallel with your code.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
