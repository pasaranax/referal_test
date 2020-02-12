import json

from parser import Parser


def test_log():
    log = json.load(open("log.json"))
    parser = Parser(log)
    counter = 0
    for customer, record in zip(parser.records(), log):
        counter += 1
        assert customer.client_id == record["client_id"]
    assert counter == 20


def test_purchases():
    log = json.load(open("log.json"))
    parser = Parser(log, sort=True)
    counter = 0
    for customer in parser.records(only_purchases=True):
        counter += 1
        assert customer.purchase is not None
    assert counter == 7


def test_ours_purchases():
    log = json.load(open("log.json"))
    parser = Parser(log, sort=True)
    counter = 0
    for customer in parser.records(partner="referal.ours.com", only_purchases=True):
        counter += 1
        assert customer.purchase is not None
        assert customer.last_partner == "referal.ours.com"
    assert counter == 4
