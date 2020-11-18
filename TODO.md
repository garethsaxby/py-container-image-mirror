# Possible Improvements

- Allow env vars for input, especially for authetication details.
- Create class for inputs to avoid passing all of it through to the functions and clean up the mess.
- Look to possibly move away from Click, or simplify the quantity of decorators involved; it's hard to read currently.
- Log output formatting - Should be selectable and be more human readable for CLI exectuion.
- Testing - Linting in Actions instead of just the Makefile, Unit tests, possibly integration tests.
- Allow for remote Docker usage.
- Batch mode.
- Discovery of images to push, instead of having to execute multiple times.
