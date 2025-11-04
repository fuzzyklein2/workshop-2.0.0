# Module `hw.__main__`

*Generated on 2025-10-16T08:06:23*

❌ **Failed to import module `hw.__main__`**

```
Import attempt using importlib.import_module failed:

Traceback (most recent call last):
  File "/home/fuzzy/projects/pygnition-1.0.1/pygnition/generate_docs_pipeline.py", line 71, in safe_import_module
    mod = importlib.import_module(module_name)
  File "/home/fuzzy/python-3.13.2/lib/python3.13/importlib/__init__.py", line 88, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1331, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 935, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 1026, in exec_module
  File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
  File "/home/fuzzy/projects/pygnition-1.0.1/docs/examples/hw-1.0.1/hw/__main__.py", line 83, in <module>
    from .hw import HW
  File "/home/fuzzy/projects/pygnition-1.0.1/docs/examples/hw-1.0.1/hw/hw.py", line 15, in <module>
    from pygnition.program import Program
  File "/home/fuzzy/projects/pygnition-1.0.1/pygnition/program.py", line 42, in <module>
    from pygnition.settings import Settings
  File "/home/fuzzy/projects/pygnition-1.0.1/pygnition/settings.py", line 53, in <module>
    from pygnition.configure import configure
  File "/home/fuzzy/projects/pygnition-1.0.1/pygnition/configure.py", line 49, in <module>
    from pygnition.constants import NEWLINE
  File "/home/fuzzy/projects/pygnition-1.0.1/pygnition/constants.py", line 76, in <module>
    VERSION = remove_tag(grep(VERSION_TAG, DOCSTR)[0])
                         ~~~~~~~~~~~~~~~~~~~~~~~~~^^^
IndexError: list index out of range


Fallback attempt using runpy.run_module failed:

Traceback (most recent call last):
  File "/home/fuzzy/projects/pygnition-1.0.1/pygnition/generate_docs_pipeline.py", line 80, in safe_import_module
    module_globals = runpy.run_module(module_name, run_name=module_name, alter_sys=True)
                     ^^^^^
NameError: name 'runpy' is not defined. Did you forget to import 'runpy'?

```
