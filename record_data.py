#!/usr/bin/python3

from wr.adapters.RDMAdapter import RDMAdapter
from wr.adapters.DWDAdapter import DWDAdapter
import wr.db_model as db


def record_data():
    adapters = [RDMAdapter('RDM'), DWDAdapter('DWD')]

    for adapter in adapters:
        adapter.receive_data()


if __name__ == '__main__':
    record_data()
