# TF-IDF

This folder implements the [tf-idf](https://en.wikipedia.org/wiki/Tf%E2%80%93idf) algorithm for identifying the top keywords in each (text) file within a corpus (folder of files).

## Usage:

````bash
# view full usage/help
./run.py -h

# run on provided examples
./run.py inputs/

# run on custom folder
./run.py ~/example/path

# specify file extensions to look for
./run.py ~/example/path -e "md,txt,rst"
````

## Example Output:
````txt
searching 5 files...

'inputs/tesla.txt' top 3 words:
'energy'	(TF_IDF: 0.03986)
'solar'	(TF_IDF: 0.02741)
'electric'	(TF_IDF: 0.01993)

'inputs/google.txt' top 3 words:
'google'	(TF_IDF: 0.02419)
'properties'	(TF_IDF: 0.01345)
'advertisers'	(TF_IDF: 0.01345)

'inputs/microsoft.txt' top 3 words:
'server'	(TF_IDF: 0.02737)
'office'	(TF_IDF: 0.01825)
'xbox'	(TF_IDF: 0.01642)

'inputs/apple.txt' top 3 words:
'mac'	(TF_IDF: 0.02134)
'ios'	(TF_IDF: 0.01909)
'tv'	(TF_IDF: 0.01685)

'inputs/facebook.txt' top 3 words:
'people'	(TF_IDF: 0.03308)
'marketers'	(TF_IDF: 0.01743)
'messenger'	(TF_IDF: 0.01743)
````
