# Materials Science Data Science Notebooks

## Summary

A bunch of jupyter notebooks that I have been using during the year of 2019 in Professor Ohuchi and Professor Huang's research group.

## Requirements

### Python dependencies

To be able to run these notebooks, make sure you install the required python packages by running `pip install -r requirements.txt`. You will also need a specific package internal to our research group.

### Data dependencies

You will need to place a data file named `Updated_PCM.csv` in `data/`, to be able to run most of these. It is a particular file internal to our research group.

## Individual Descriptions

### ML_Playground.ipynb

Used for training neural networks to predict specific properties when other properties are known. Also contains various graphing tools for these ends.

### Sompy_experientation.ipynb

Lets one generate and train a Self-organizing-map. One cell allows one to press a button in order to train a SOM. When that is complete, you can then press the "save" button, and it will generate a `som_codemat_nprops_{date}.h5` file. This can then be used in the subsequent `SOM_Visualization.ipynb` file to see the results.

### SOM_Visualization.ipynb

Visualizes a Self-Organizing Map with various systems. To select a SOM, first train one with the `Sompy_experimentation.ipynb` file, and then copy the filename of the created file into the `CODEBOOK_FILE` variable in around cell 7 or so.

### Scaling\ Demonstration.ipynb

Notebook for experimenting with various scaling functions for visualizing the data in the SOM heatmaps

### Parse_SOM.py

Code from Everet Wang that parses our dataset into a form that can be fed into a pandas dataframe.

## Credits

Thank you to Everet Wang, for both collecting the data that these scripts use (although this data is not included in this distribution), and for writing the script to parse all the collected data from the file.

Thank you to Professor Ohuchi and Professor Huang, for supporting this research initiative and providing guidance in various ways.

Thank you to all the other members of the research group I am in for their various insights they have provided over the course of development.

Thank you to the collaborators over at Tohoku University who provided the ground work for this project (Gota Kikugawa, Yuta Nishimura).

Thank you to the developers of [SOMPY](https://github.com/sevamoo/SOMPY), Vahid Moosavi, Sebastian Packmann, and Ivan Valles.
