**This module is used to measure the data update of the RPKI Repository.**



#### get_repository.py

This file is used to process the *repository.json* file obtained by Routinator and extract the information in it. This file implements:

**a. Process the repository.json to get the URI information.**



#### **count_xml.py**

This file is used to request each URI, determine if each URI updates the file, and get the latest data. This file implements:

**a. Based on the result of get_repository.py, the data of each URI is requested to determine if there is any data update.**

**b. Get the latest URI data, extract the updated data amount and the updated file name.**

