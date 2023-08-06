import sys

import click
from fritzconnection.lib.fritzstatus import FritzStatus

# sensu check exit codes
SENSU_EXIT_OK = 0
SENSU_EXIT_WARNING = 1
SENSU_EXIT_CRITICAL = 2


@click.command()
@click.option(
    "--address",
    required=True,
    type=click.STRING,
    help="Fritz!Box hostname")
# @click.option(
#     "--password",
#     required=True,
#     type=click.STRING,
#     help="Fritz!Box UPnP password")
@click.option(
    "--uptime",
    default=10,
    type=click.INT,
    help="Minimum uptime [seconds] for valid counters (10)")
@click.option(
    "--measurement",
    default='fritz',
    type=click.STRING,
    help="influx measurement name [fritz]")
def cli(address, uptime, measurement):

    # fc = FritzStatus(address=address, password=password)
    fc = FritzStatus(address=address)

    if not fc.is_connected or not fc.is_linked:
        print(f'is_connected={fc.is_connected}, '
          f'is_linked={fc.is_linked}')
        sys.exit(SENSU_EXIT_CRITICAL)

    if not fc.bytes_received or not fc.bytes_sent:
        print(f'bytes_received={fc.bytes_received}, '
          f'bytes_sent={fc.bytes_sent}')
        sys.exit(SENSU_EXIT_CRITICAL)

    fields = {
        'received': fc.bytes_received,
        'sent': fc.bytes_sent,
        'uptime': fc.uptime
    }

    tags = {
        'hostname': address,
        'ipv4': fc.external_ip,
        'ipv6': fc.external_ipv6
    }

    def _key_values(d):
        return ['%s=%s' % (k, v) for k, v in d.items()]

    print('{measurement},{tags} {fields}'.format(
        measurement=measurement,
        tags=','.join(_key_values(tags)),
        fields=','.join(_key_values(fields))))

    sys.exit(SENSU_EXIT_OK if fc.uptime < uptime else SENSU_EXIT_WARNING)


if __name__ == '__main__':
    cli()
