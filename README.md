# RedAffair
Text based adventure/detective game written in python

## Android build with ksproject

RedAffair uses `ksproject` for Android builds. Install Python 3.13 and `uv`,
then run:

```bash
uv sync
uv run ksproject android build debug --clean
uv run ksproject android devices
uv run ksproject android run --uuid DEVICE_SERIAL
```

The Android configuration is in `pyproject.toml`. It targets Android API 36,
uses the Kivy bootstrap from the `master` branch of `ksp-bootstraps`, and
supports `arm64-v8a` and `x86_64` debug builds.

`buildozer.spec` is retained as a legacy fallback. It is not required for the
normal ksproject workflow.
