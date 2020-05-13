from troposphere import Output, Ref, Template, Parameter, GetAtt
from troposphere import ec2

t = Template()

# Set parameters for stack

t.set_description(
    "Antonette Caldwell / Udacity Cloud DevOps Nanodegree Program "
    "This template deploys a public NAT gate as the infrastructure "
    "for creating a highly available web application")

vpc_cidr = t.add_parameter(Parameter(
    'VpcCIDR',
    Default='10.0.0.0/16',
    Description='The IP address space for this VPC in CIDR notation',
    Type='String',
))

public_subnet_1 = t.add_parameter(Parameter(
    'PublicSubnet1CIDR',
    Type='String',
    Description='Public Subnet CIDR',
    Default='10.0.0.0/24'
))

public_subnet_2 = t.add_parameter(Parameter(
    'PublicSubnet2CIDR',
    Type='String',
    Description='Public Subnet CIDR',
    Default='10.0.1.0/24'
))

private_subnet_1 = t.add_parameter(Parameter(
    'PrivateSubnet1CIDR',
    Description='Private Subnet CIDR',
    Default='10.0.2.0/24'
))

private_subnet_2 = t.add_parameter(Parameter(
    'PrivateSubnet1CIDR',
    Description='Private Subnet CIDR',
    Default='10.0.3.0/24'
))

fh = open("template.yaml", "a")
fh.writelines(t.to_yaml())
fh.close()