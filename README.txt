- Download fifa.csv, fut.csv, and cards.csv from the zip file. fifa.csv is the downloaded FIFA dataset, fut.csv is the downloaded FUT dataset, and cards.csv is the dataset with player cards.
- Run the Python script to generate 3 files: processed.csv, finalProcessed.csv, and cardProcessed.csv

For Elite Regressions:
	- Import finalProcessed.csv into STATA
	- Open doFile1.do
	- Run doFile1.do

For Non-Elite Regressions:
	- Import cardProcessed.csv into STATA
	- Open doFile2.do
	- Run doFile2.do

-Writing Elite folder shows how we assigned binary values of elite or not elite per player

-Classifiers folder contains the sklearn K-NN and naive bayes classifiers executed in a jupyter notebook (using the binaryelte csv file) that determine if the player was elite or not. Accuracy also calculated using sklearn metrics.    