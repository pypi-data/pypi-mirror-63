# colourmap

[![Python](https://img.shields.io/pypi/pyversions/colourmap)](https://img.shields.io/pypi/pyversions/colourmap)
[![PyPI Version](https://img.shields.io/pypi/v/colourmap)](https://pypi.org/project/colourmap/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](https://github.com/erdogant/colourmap/blob/master/LICENSE)
[![Downloads](https://pepy.tech/badge/colourmap/week)](https://pepy.tech/project/colourmap/week)
[![Donate](https://img.shields.io/badge/donate-grey.svg)](https://erdogant.github.io/donate/?currency=USD&amount=5)

* Python package colourmap generates an N unique colors from the specified input colormap.

## Contents
- [Installation](#-installation)
- [Requirements](#-Requirements)
- [Quick Start](#-quick-start)
- [Contribute](#-contribute)
- [Citation](#-citation)
- [Maintainers](#-maintainers)
- [License](#-copyright)

## Installation
* Install colourmap from PyPI (recommended). colourmap is compatible with Python 3.6+ and runs on Linux, MacOS X and Windows. 
* It is distributed under the MIT license.

## Requirements
```python
# This can be done manually but is also done automatically when pip installing colourmap.
pip install -r requirements
```

## Quick Start
```
pip install colourmap
```

* Alternatively, install colourmap from the GitHub source:
```bash
git clone https://github.com/erdogant/colourmap.git
cd colourmap
python setup.py install
```  

### Import colourmap package
```python
import colourmap as colourmap
```

### Example:
```python
N=10
# Create N colors
getcolors=colourmap.generate(N)

# With different cmap
getcolors=colourmap.generate(N, cmap='Set2')

# Create color for label
y=[1,1,2,2,3,1,2,3]
label_colors, colordict=colourmap.fromlist(y)
# With different cmap
label_colors, colordict=colourmap.fromlist(y, cmap='Set2')
# With different method
label_colors, colordict=colourmap.fromlist(y, cmap='Set2', method='seaborn')

# String as input labels
y=['1','1','2','2','3','1','2','3']
label_colors, colordict=colourmap.fromlist(y)
# With different cmap
label_colors, colordict=colourmap.fromlist(y, cmap='Set2')
# With different method
label_colors, colordict=colourmap.fromlist(y, cmap='Set2', method='seaborn')

```

### Citation
Please cite colourmap in your publications if this is useful for your research. Here is an example BibTeX entry:
```BibTeX
@misc{erdogant2019colourmap,
  title={colourmap},
  author={Erdogan Taskesen},
  year={2019},
  howpublished={\url{https://github.com/erdogant/colourmap}},
}
```

### Maintainers
* Erdogan Taskesen, github: [erdogant](https://github.com/erdogant)

### Contribute
* Contributions are welcome.

### Licence
See [LICENSE](LICENSE) for details.

### Donation
* This package is created and maintained in my free time. If this package is usefull, you can show your <a href="https://erdogant.github.io/donate/?currency=USD&amount=5">gratitude</a> :) Thanks!
