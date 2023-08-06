import click
from qaenv import mongo_ip

from QIFIAccount.QARealtimeStockSim import QIFI_StockSIM_Account


@click.command()
@click.option('--user')
@click.option('--password')
@click.option('--eventmq_ip', default='192.168.2.117')
@click.option('--eventmq_port', default=5672)
@click.option('--trade_host', default=mongo_ip)
def qasimStock(user, password, eventmq_ip, eventmq_port, trade_host):
    QIFI_StockSIM_Account(username=user, password=password, eventmq_ip=eventmq_ip,
                          eventmq_port=eventmq_port, trade_host=trade_host)
