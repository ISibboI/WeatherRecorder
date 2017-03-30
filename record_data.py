#!/usr/bin/python3

from wr.adapters.RDMAdapter import RDMAdapter
from wr.adapters.DWDAdapter import DWDAdapter


def record_data():
    adapters = [RDMAdapter('RDM'), DWDAdapter('DWD')]

    for adapter in adapters:
        for point in adapter.receive_data():
            point.create()


if __name__ == '__main__':
    record_data()
