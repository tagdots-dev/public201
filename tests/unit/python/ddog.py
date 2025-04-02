#!/usr/bin/env python

import json

import requests
from click import argument, command
from datadog import initialize, statsd


def get_db_group_rows(environment):
    headers = {'Host': 'app-query.ingress.consul'}
    url = f"http://ingress-{environment}.{environment}.test.io:8080/groups"

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        curl_data = response.json()
        json_data = json.dumps(curl_data)
        data_dump = json.loads(json_data)
        data_leng = len(data_dump)
        return (data_leng)
    except requests.exceptions.HTTPError as errh:
        raise SystemExit(errh)
    except requests.exceptions.ConnectionError as errc:
        raise SystemExit(errc)
    except requests.exceptions.Timeout as errt:
        raise SystemExit(errt)
    except requests.exceptions.RequestException as err:
        raise SystemExit(err)


def put_db_group_rows(env, data):
    cluster_name = f"cluster_name:eks-service-{env}"
    environment = f"environment:{env}"
    options = {
        'statsd_host': 'datadog-agent',
        'statsd_port': 8125
    }

    try:
        initialize(**options)
        statsd.gauge('app.db_group_rows', data, tags=[cluster_name, environment])
        print("app db number of group rows: ", data)
        return
    except Exception as e:
        raise SystemExit(e)


@command()
@argument('env')
def main(env):
    data = get_db_group_rows(env)
    put_db_group_rows(env, data)


main()
