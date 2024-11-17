# dRR

[NDSS 2024] dRR: A Decentralized, Scalable, and Auditable Architecture for RPKI Repository
dRR is an architecture that enhances the security, robustness, and scalability of the RPKI Repository. dRR introduces two new entities: Certificate Servers (CSs) and Monitors, forms a decentralized federation of CSs, which enables the RPKI Repository to proactively defend against malicious behavior from authorities and to tolerate PPs’failures.

For more details, please refer to [our paper](https://www.ndss-symposium.org/ndss-paper/drr-a-decentralized-scalable-and-auditable-architecture-for-rpki-repository/) from NDSS'24.


# CSfederation

This module is used to simulate the CS federation which contains several CS nodes. In our paper, we use Alibaba Cloud servers and the distribution of the nodes is as follow: `Australia (7), India(7), China(7), Hongkong,China(7), Singapore(7), Japan(7), Germany(7), Britain(7), Silicon Valley,USA(7), Virginia,USA(7), Indonesia(6), Malaysia(6), Dubai,UAE(6), Philippines(6), and Thailand(6).` You can refer to [hotstuff](https://github.com/relab/hotstuff) to config hotstuff and choose the `Chained Hotstuff`. And you should use `config.yaml` to config your CS nodes.

## prerequisites

Ubuntu 18.04 server with 4 cores and 8GB RAM

go 1.17.6

python 3.x

protocol buffers 3.16

peak-bandwidth 200Mbps

## run the command:
`sudo ./hotstuff run --config /root/config.yaml  --duration 60s --view-timeout 5s --client-timeout 10s --batch-size 50 --rate-limit 100 --max-concurrent 400`

# Email

This module is used to send questionnaires to the ROA deployers.

## prerequisites
python 3.10

# Measurement

This module is used to measure the data update of the RPKI Repository and measure the latency of the RPKI Repository to each country.

## prerequisites

Ubuntu 22.04

python 3.10

## code 

1) get_repository.py: process the repository.json to get the URI information.

2) count_xml.py: request each URI, determine if each URI updates the file, and get the latest data.

3) create_measurement.py: obtain RIPE Atlas probes distributed in different countries and to use the probes for ping tests.


# Monitor

This module is used to simulate the delay of CS nodes -> monitors -> RPs.

## prerequisites

Ubuntu 22.04

python 3.10

peak-bandwidth 100Mbps

## code

1) cluster_A.py: simulate CS nodes and a script for cluster_A.py should be run on each CS node.

2) cluster_B.py: simulate monitor nodes and a script for cluster_B.py should be run on each monitor node. Receive data from upper CS nodes and send the data to the RP nodes.

3) cluster_C.py: simulate RP nodes and a script for cluster_C.py should be run on each RP node. Receive files from the monitor.


