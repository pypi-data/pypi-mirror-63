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

### Naive solution

First thing that comes to mind is to postpone import by moving it into the function that need that module:

```python
async def my_work(self) -> None:
    import this  # will block until imported
```

It reduces your startup time, but it is still blocking your event loop.

### Usage

The preferred way to use `aioimport` is:
```python
import aioimport

async def my_work(self) -> None:
    await aioimport.import_module("this")  # will asynchronously import module
    import this  # will be instantaneous since `this` is already in `sys.modules`
    # and you can asynchronously reload it too:
    await aioimport.reload(this)
```

### How it works

Module import is done in new thread worker.

Be aware of the fact that GIL still exists and technically import is done concurrently rather than in parallel with your code.

## Future work

Currently after your first use of `aioimport` it's workers threads run forever waiting for new imports.

The plan is to have some form of automatic shutdown after some time passes since last import.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
