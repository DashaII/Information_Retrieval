# Information_Retrieval
### PART1
The goal of this project is to get hands-on implementation of the vector space model, text preprocessing, system tuning, and experimentation in Information Retrieval.
 - Develop an experimental retrieval system based on the vector space model.
 - Experiment with methods for text processing, query construction, term and document weighting, similarity measurement, etc.
 - Optimize the system performance on the provided test collections (in English and Czech)

### PART2
The goal of this project is to learn about available frameworks for Information Retrieval and use them to deliver state-of-the-art results on the provided test collections (the same as in PART1).
 - Use the PyTerrier framework to setup/implement an IR system.
 - Optimize the system on the provided test collections (using the training topics)

### PART1 - How to run the script
------------------

1.	Add folders with documents to folder docs, so that structure becomes docs/documents_cs and docs/documents_en

2.	To run the program from command line use:
python main.py --full 0 --run run-0
where:
--full: 0/1 reduced or full list of documents (see note below)
--run: run-0 or run-1
3.	The above script runs both languages for both, train and test, topics and save results to docs/results folder

Notes:
 - I fixed the broken files manually, the list of broken files can be found in the broken_docs.txt. The program will break if run with the full list of topics, you should either use the reduced list of docs (provided in the documents_red _**.lst) or fix the errors in the broken files and run on the full topics list.
 - By default, the script is run with the reduced list of documents.
 - The best results provided for the FULL list of documents which I fixed manually.
 - The list of libraries is in requirements.txt file.
 - To make a clean run and be on the safe side, it makes sense to remove all .json files from docs/clean folder before running the script.

### PART2 - How to run the script
---------------------
1.	Add folders with documents to folder docs, so that structure becomes docs/documents_cs and docs/documents_en

2.	For some reason relative path to index folder for PyTerrier library didn't work for me, so I indicated the full path in configs.py file under xx_INDEX_PATH_RUNx name.
	To run the srcript, you need to change these variables accordingly.

2.	To run the program to get results for run0/run1/run2 run hw2_terrier_run0.py/hw2_terrier_run1.py/hw2_terrier_run2.py accordingly

3.	The above script runs both languages for both, train and test, topics and save results to docs/results folder

Notes:
 - I fixed the broken files manually, the list of broken files can be found in the broken_docs.txt. The program will break if run with the full list of topics, you should either use the reduced list of docs (provided in the documents_red _**.lst) or fix the errors in the broken files and run on the full topics list.
 - By default, the script is run with the reduced list of documents.
 - The best results provided for the FULL list of documents which I fixed manually.
 - The list of libraries is in requirements_hw2.txt file.
 - To make a clean run and be on the safe side, it makes sense to remove all .json files from docs/clean folder before running the script.

