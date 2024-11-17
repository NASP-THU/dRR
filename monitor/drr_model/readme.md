**This module is mainly used to simulate the delay of our model.**

#### **cluster_A.py**

This file is mainly used to simulate CS nodes, and a script for cluster_A.py should be run on each CS node. This file implements:

**a. Generate several RPKI files randomly every 10 seconds.**

**b. Notify other CS nodes of the updated filename of the machine.**

**c. Notify each CS node of the update of data to the monitor node responsible for the CS node of this machine.**



#### cluster_B.py

This file is mainly used to simulate monitor nodes, and a script for cluster_B.py should be run on each monitor node. This file implements:

**a. Receive data synchronization information from upper CS nodes and request the latest data from all CS nodes.**

**b. Save the latest received RPKI data and send the data to the RP node.**



#### cluster_C.py

This file is mainly used to simulate RP nodes, and a script for cluster_C.py should be run on each RP node. This file implements:

**a. Receive files from the monitor machine.**

