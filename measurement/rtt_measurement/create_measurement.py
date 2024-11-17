"""
This python file is used to create traceroute measurement
"""

import time
from ripe.atlas.cousteau import (
  Traceroute,
  Ping,
  AtlasSource,
  AtlasCreateRequest,
  AtlasResultsRequest,
  ProbeRequest,
  Probe
)
from ripe.atlas.sagan import TracerouteResult


ATLAS_API_KEY = "Your ATLAS_API_KEY"


def create_measurement(domain_name, probe_value, probe_num):
    time.sleep(1)
    ping = Ping(
        af=4,
        target=domain_name,
        description=f"Your description",
        resolve_on_probe='true'
    )

    source = AtlasSource(
        type="probes",
        value=probe_value,
        requested=probe_num,
    )

    atlas_request = AtlasCreateRequest(
        # start_time=datetime.datetime.utcnow() + datetime.timedelta(minutes=1),
        key=ATLAS_API_KEY,
        measurements=[ping],
        sources=[source],
        is_oneoff=True
    )

    (is_success, response) = atlas_request.create()

    print(response['measurements'][0])
    if is_success:
        my_id = response['measurements'][0]
        f.write(f'{my_id}\n')
        f.flush()
    else:
        print(response)
        print('fail')


def get_probe_list():

    probe_list = open('data/probe_info.txt', 'w')

    filters = {"status": 1, "is_public": 'true'}
    probes = ProbeRequest(**filters)

    country_dict = dict()
    for probe in probes:
        probe_id = probe['id']
        probe_asn = probe['asn_v4']
        probe_country = probe['country_code']

        if probe_country is not None and probe_asn is not None:
            if probe_country not in country_dict.keys():
                country_dict[probe_country] = dict()
            if len(country_dict[probe_country]) < 1:
                if probe_asn not in country_dict[probe_country].keys():
                    country_dict[probe_country][probe_asn] = probe_id
                    probe_list.write(f'{probe_id} {probe_asn} {probe_country}\n')

    probe_list.close()


if __name__ == '__main__':

    domain_list = ['0.sb', 'ca.nat.moe', 'ca.rg.net', 'chloe.sobornost.net', 'cloudie.rpki.app', 'dev.tw',
                   'krill.accuristechnologies.ca', 'krill.stonham.uk', 'magellan.ipxo.com', 'repo-rpki.idnic.net',
                   'repo.kagl.me', 'repo.rpki.space', 'rov-measurements.nlnetlabs.net', 'rpki-01.pdxnet.uk',
                   'rpki-publication.haruue.net', 'rpki-repo.registro.br', 'rpki-repository.nic.ad.jp',
                   'rpki-rrdp.mnihyc.com', 'rpki-rrdp.us-east-2.amazonaws.com', 'rpki-rrdp.us-east-2.amazonaws.com-1',
                   'rpki-rrdp.us-east-2.amazonaws.com-10', 'rpki-rrdp.us-east-2.amazonaws.com-11',
                   'rpki-rrdp.us-east-2.amazonaws.com-12', 'rpki-rrdp.us-east-2.amazonaws.com-13',
                   'rpki-rrdp.us-east-2.amazonaws.com-14', 'rpki-rrdp.us-east-2.amazonaws.com-15',
                   'rpki-rrdp.us-east-2.amazonaws.com-2', 'rpki-rrdp.us-east-2.amazonaws.com-3',
                   'rpki-rrdp.us-east-2.amazonaws.com-4', 'rpki-rrdp.us-east-2.amazonaws.com-5',
                   'rpki-rrdp.us-east-2.amazonaws.com-6', 'rpki-rrdp.us-east-2.amazonaws.com-7',
                   'rpki-rrdp.us-east-2.amazonaws.com-8', 'rpki-rrdp.us-east-2.amazonaws.com-9',
                   'rpki.admin.freerangecloud.com', 'rpki.apernet.io', 'rpki.as207960.net', 'rpki.cc',
                   'rpki.cernet.edu.cn', 'rpki.cnnic.cn', 'rpki.folf.systems', 'rpki.luys.cloud', 'rpki.miralium.net',
                   'rpki.multacom.com', 'rpki.owl.net', 'rpki.pudu.be', 'rpki.qs.nu', 'rpki.rand.apnic.net',
                   'rpki.roa.net', 'rpki.sailx.co', 'rpki.sn-p.io', 'rpki.tools.westconnect.ca', 'rpki.uz',
                   'rpki.xindi.eu', 'rpki.zappiehost.com', 'rpkica.mckay.com', 'rrdp-rps.arin.net', 'rrdp.afrinic.net',
                   'rrdp.apnic.net', 'rrdp.arin.net', 'rrdp.krill.nlnetlabs.nl', 'rrdp.lacnic.net',
                   'rrdp.paas.rpki.ripe.net', 'rrdp.ripe.net', 'rrdp.rp.ki', 'rrdp.sub.apnic.net',
                   'sakuya.nat.moe', 'x-8011.p.u9sv.com']

    domain_list = ["pub.krill.ausra.cloud", "rrdp.rpki.co", "rrdp.rpki.tianhai.link", "rrdp.twnic.tw",]

    get_probe_list()
    probe_list = list()
    with open('data/probe_info.txt', 'r') as f:
        line = f.readline()
        while line:
            if line != '\n':
                probe_list.append(line.strip('\n').split(' ')[0])
            line = f.readline()
    probe_info = ', '.join(probe_list)

    with open('data/msm_id.txt', 'w') as f:
        for domain in domain_list:
            try:
                create_measurement(domain, probe_info, len(probe_list))
            except:
                print(f'Domain Fail : {domain}')



