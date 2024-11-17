import json


def read_routinator_repo():
    repo_set = list()
    with open(f'data/repositories-rrdp.json', 'r', encoding='utf-8') as file:
        data = json.load(file)
        for rp in data['repositories']:
            if "rpkiNotify" in rp.keys():
                repo_set.append(rp["rpkiNotify"])
    return repo_set


if __name__ == '__main__':
    s2 = read_routinator_repo()
    for i in s2:
        print(i)



