"""Main module."""
from typing import Tuple

import boto3
import botocore
import requests
import logging


class SGIPUpdate:
    """Security Group IP Update."""

    def __init__(self, **kwargs):
        """Initialize SGIPUdate."""
        self.__dict__.update(kwargs)
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        self.ec2 = boto3.resource('ec2')
        self.client = boto3.client('ec2')

    @staticmethod
    def get_public_ip():
        """Get Public IP Address."""
        ip_address = requests.get('https://api.ipify.org').text
        return ip_address

    def check_security_group(
            self,
            security_group_id: int,
            ip_address: str) -> Tuple[bool, bool]:
        """Check if the security group contains a rule for the current IP.

        Args:
            security_group_id (int): identifier of the security group to check
            ip_address (str): IP address to check for in the SG

        Returns:
            Tuple[bool, bool]: should update?, should add?

        """
        security_group = self.ec2.SecurityGroup(security_group_id)
        permissions = security_group.ip_permissions
        update = False
        add = True
        for permission in permissions:
            descriptions = [
                ip_range.get('Description', 'N')
                for ip_range in permission.get('IpRanges')
            ]
            if self.ingress_description in descriptions:
                for ingress in permission.get('IpRanges'):
                    if self.ingress_description == ingress.get(
                            'Description', 'N'):
                        update = True
                        add = False
                        if ip_address in ingress.get('CidrIp'):
                            update = False
        return update, add

    def run(self):
        """Loop over the security groups and update them if necessary."""
        ip_address = SGIPUpdate.get_public_ip()
        for security_group in self.security_group:
            update, add = self.check_security_group(security_group, ip_address)
            if update:
                self.logger.info(
                    "Description present in Security Group, updating...")
                self.update_ip_in_sg(security_group, ip_address)
            elif add:
                self.logger.info(
                    "Description not present in Security Group, adding...")
                self.add_ip_to_sg(security_group, ip_address)
            else:
                self.logger.info(
                    "IP Address already present in Security Group, "
                    "not updating..."
                )

    def update_ip_in_sg(self, security_group_id: int, ip_address: str):
        """Update IP address in Security Group.

        Args:
            security_group_id (int): identifier of the security group to update
            ip (str): IP Address to update

        """
        self.remove_description_from_sg(security_group_id)
        self.add_ip_to_sg(security_group_id, ip_address)

    def remove_description_from_sg(self, security_group_id: int):
        """Remove Description from Security Group.

        Args:
            security_group_id (int): identifier of the security group to remove

        """
        self.logger.info('Removing old IP...')
        security_group = self.ec2.SecurityGroup(security_group_id)
        permissions = security_group.ip_permissions
        permission = permissions[0]
        ranges = permission.get('IpRanges', list())
        for ip_range in ranges:
            if ip_range.get('Description', 'N') == self.ingress_description:
                cidr_ip = ip_range.get('CidrIp')
        try:
            self.client.revoke_security_group_ingress(
                GroupId=security_group_id,
                IpPermissions=[
                    {
                        'FromPort': permission['FromPort'],
                        'IpProtocol': permission['IpProtocol'],
                        'IpRanges': [
                            {
                                'CidrIp': cidr_ip,
                                'Description': self.ingress_description
                            },
                        ],
                        'ToPort': permission['ToPort'],
                    },
                ]
            )
        except botocore.exceptions.ClientError as error:
            self.logger.exception(error)

    def add_ip_to_sg(self, security_group_id: int, ip_address: str):
        """Add IP address to Security Group.

        Args:
            security_group_id (int): identifier of the security group to add
            ip_address (str): IP Address to add

        """
        self.logger.info('Adding new IP...')
        security_group = self.ec2.SecurityGroup(security_group_id)
        permissions = security_group.ip_permissions
        permission = permissions[0]
        cidr_ip = f'{ip_address}/32'
        try:
            self.client.authorize_security_group_ingress(
                GroupId=security_group_id,
                IpPermissions=[
                    {
                        'FromPort': permission['FromPort'],
                        'IpProtocol': permission['IpProtocol'],
                        'IpRanges': [
                            {
                                'CidrIp': cidr_ip,
                                'Description': self.ingress_description
                            },
                        ],
                        'ToPort': permission['ToPort'],
                    },
                ],
            )
            self.logger.info('Updated security group %s' % security_group_id)
        except botocore.exceptions.ClientError as error:
            self.logger.exception(error)
