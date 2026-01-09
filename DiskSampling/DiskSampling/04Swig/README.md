# SWIG Development

To use SWIG and cmake we need to build against a python verions. The easiest way to do this is you use an activate a venv 

```
uv run
source .venv/bin/activate
```

We need to specify the swig location

```
cmake -G Ninja -D SWIG_DIR=/public/devel/24-25/swig/share/swig/4.3.0 -DSWIG_EXECUTABLE=/public/devel/24-25/swig/bin/swig  ..
```