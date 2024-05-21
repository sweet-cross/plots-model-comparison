# This is the library to plot the results for the CROSS model comparison 


## Files and folders
- distributions/plots.py contains all the functions to upload the data and plot
- cross_comparison.py is the python code that interacts with distributions/plots.py and creates the plots
- results/ is the folder from where the results are uploaded
- plots/ is the folder where the plots are saved


# Dependencies

* See requirements.txt.  


## Usage with python virtual environment without Conda
   
* Create a python virtual environment doing the following:
	* `python -m venv /path_to/cross-comparison ` (This command creates a virtual environment called "cross-comparison")
	* Mac-Os X and Unix based operating systems: `source /path_to/cross-comparison/bin/activate` (This command activates the "cross-comparison" environment.)
	* Windows operating system: `/path_to/cross-comparison/Scripts/activate.bat` (This command activates the "cross-comparison" environment.)
	* `cd` to the folder where you cloned the codes
	* `pip install -r requirements.txt` (This command installs all the required python packages.)
* Run/edit cross_comparison.py.


## Usage with python virtual environment with Conda
   
* Create a [python virtual environment](https://towardsdatascience.com/why-you-should-use-a-virtual-environment-for-every-python-project-c17dab3b0fd0) for this project. For example, if you use [conda](https://docs.conda.io/en/latest/) for python package management, do the following:
	* `conda create -n cross-comparison` (This command creates a virtual environment called "cross-comparison")
	* `conda activate cross-comparison` (This command activates the "cross-comparison" environment.)
	* `cd` to the folder where you cloned the codes
	* `pip install -r requirements.txt` (This command installs all the required python packages.)
* Run/edit cross_comparison.py.






