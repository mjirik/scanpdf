# scanpdf
PDF from scanned files

## Install

1) Install [conda](https://conda.io/miniconda.html)

2) Install requested packages
```commandline
conda create -n scanpdf -c conda-forge -c mcs07 python=3.6 scikit-image ruamel.yaml pyqtgraph pyqt=5 tesseract tesserocr
```


## Run

```commandline
activate scanpdf
python -m scanpdf
```
