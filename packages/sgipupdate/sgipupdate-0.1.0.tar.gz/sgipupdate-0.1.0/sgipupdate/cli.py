"""Console script for sgipupdate."""
import sys

import click
import click_config_file

from sgipupdate.sgipupdate import SGIPUpdate


@click.command()
@click.option(
    "--security-group",
    type=str,
    multiple=True,
    required=True,
    help="Specify the id for a security group to check/update"
)
@click.option(
    "--ingress-description",
    required=True,
    type=str,
    help="Specify the description for the ingress rule to update in the SG"
)
@click_config_file.configuration_option(
    config_file_name='config.ini'
)
def main(**kwargs):
    """Console script for sgipupdate."""
    sg_ip_update = SGIPUpdate(**kwargs)
    sg_ip_update.run()


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
