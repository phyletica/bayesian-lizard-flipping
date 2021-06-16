[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/phyletica/bayesian-lizard-flipping/main?filepath=bayesian-stats.ipynb)

A simple example of Bayesian probability using lizard flipping.
The lizard flipping was inspired by Luke Harmon's book on phylogenetic
comparative methods: <https://lukejharmon.github.io/pcm>

# Setting up the Python environment

To setup a local Python virtual environment that allows you to open the iPython
notebooks using JupyterLab, run the `setup-python-env.sh` Bash script:

```bash
bash setup-python-env.sh
```

After that script finishes, there will be a `pyenv` directory that contains
the local Python environment with all of the requirements needed to run
the iPython notebooks with JupyterLab.
To do so, first activate the Python environment:

```bash
source pyenv/bin/activate
```

and then fire up JupyterLab:

```bash
jupyter-lab
```

# License

<a rel="license" href="http://creativecommons.org/licenses/by/4.0/deed.en_US"><img alt="Creative Commons License" style="border-width:0" src="http://i.creativecommons.org/l/by/4.0/88x31.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by/4.0/deed.en_US">Creative Commons Attribution 4.0 International License</a>.
