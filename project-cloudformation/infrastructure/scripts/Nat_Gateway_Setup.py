from troposphere import Output, Ref, Template, Parameter, GetAtt, Tags
from troposphere import ec2, GetAZs, Select, Sub

t = Template()

# Set parameters
environmet = t.add_parameter(Parameter(
    'EnvironmentName',
    Description='An environment name',
    Type='String'
))

vpc_cidr = t.add_parameter(Parameter(
    'VpcCIDR',
    Default='10.0.0.0/16',
    Description='The IP address space for this VPC, in CIDR notation',
    Type='String',
))

# Public and Private Subnet 1
public_subnet = t.add_parameter(Parameter(
    'PublicSubnet1CIDR',
    Type='String',
    Description='Public Subnet CIDR',
    Default='10.0.0.0/24'
))
private_subnet = t.add_parameter(Parameter(
    'PrivateSubnetCidr',
    Type='String',
    Description='Public Subnet CIDR',
    Default='10.0.2.0/24'
))

# Public and Private Subnet 2
public_subnet_2 = t.add_parameter(Parameter(
    'PublicSubnet2CIDR',
    Type='String',
    Description='Public Subnet CIDR',
    Default='10.0.1.0/24'
))
private_subnet_2 = t.add_parameter(Parameter(
    'PrivateSubnet2CIDR',
    Type='String',
    Description='Private Subnet CIDR',
    Default='10.0.3.0/24'
))

ref_environment_id = Ref('EnvironmentName')

# Add resources
vpc = t.add_resource(ec2.VPC(
    'VPC',
    CidrBlock=Ref(vpc_cidr),
    Tags=Tags(
        Name=ref_environment_id
    )
))

# Public and Private Subnet 1
public_net_1 = t.add_resource(ec2.Subnet(
    'PublicSubnet',
    CidrBlock=Ref(public_subnet),
    MapPublicIpOnLaunch=True,
    VpcId=Ref(vpc),
    AvailabilityZone=Select(0, GetAZs(''))
))
private_net_1 = t.add_resource(ec2.Subnet(
    'PrivateSubnet',
    CidrBlock=Ref(private_subnet),
    MapPublicIpOnLaunch=False,
    VpcId=Ref(vpc),
    AvailabilityZone=Select(0, GetAZs(''))
))

# Public and Private Subnet 2
public_net_2 = t.add_resource(ec2.Subnet(
    'PublicSubnet2',
    CidrBlock=Ref(public_subnet_2),
    MapPublicIpOnLaunch=True,
    VpcId=Ref(vpc),
    AvailabilityZone=Select(1, GetAZs(''))
))
private_net_2 = t.add_resource(ec2.Subnet(
    'PrivateSubnet2',
    CidrBlock=Ref(private_subnet_2),
    MapPublicIpOnLaunch=False,
    VpcId=Ref(vpc),
    AvailabilityZone=Select(1, GetAZs(''))
))

# Setup internet gateway
igw = t.add_resource(ec2.InternetGateway(
    'InternetGateway',
    Tags=Tags(
        Name=ref_environment_id
    )
))
net_gw_vpc_attachment = t.add_resource(ec2.VPCGatewayAttachment(
    'InternetGatewayAttachment',
    VpcId=Ref(vpc),
    InternetGatewayId=Ref(igw)
))

# Public and Private Route Tables 1
public_route_table = t.add_resource(ec2.RouteTable(
    'DefaultPublicRoute',
    VpcId=Ref(vpc)
))
private_route_table = t.add_resource(ec2.RouteTable(
    'DefaultPrivateRoute',
    VpcId=Ref(vpc)
))

# Public and Private Route Associations 1
public_route_association = t.add_resource(ec2.SubnetRouteTableAssociation(
    'PublicSubnet1RouteTableAssociation',
    SubnetId=Ref(public_net_1),
    RouteTableId=Ref(public_route_table),
))
private_route_association = t.add_resource(ec2.SubnetRouteTableAssociation(
    'PrivateSubnet1RouteTableAssociation',
    SubnetId=Ref(private_net_1),
    RouteTableId=Ref(private_route_table),
))

# Public and Private Route Tables
public_route_table_2 = t.add_resource(ec2.RouteTable(
    'DefaultPublicRoute2',
    VpcId=Ref(vpc)
))
private_route_table_2 = t.add_resource(ec2.RouteTable(
    'DefaultPrivateRoute2',
    VpcId=Ref(vpc)
))

# Public and Private Route Associations 2
public_route_association_2 = t.add_resource(ec2.SubnetRouteTableAssociation(
    'PublicSubnet2RouteTableAssociation',
    SubnetId=Ref(public_net_2),
    RouteTableId=Ref(public_route_table_2),
))
private_route_association_2 = t.add_resource(ec2.SubnetRouteTableAssociation(
    'PrivateSubnet2RouteTableAssociation',
    SubnetId=Ref(private_net_2),
    RouteTableId=Ref(private_route_table_2),
))

# Nat Gateway EIP 1
nat_eip = t.add_resource(ec2.EIP(
    'NatGateway1EIP',
    Domain="vpc",
))

nat = t.add_resource(ec2.NatGateway(
    'NatGateway',
    AllocationId=GetAtt(nat_eip, 'AllocationId'),
    SubnetId=Ref(public_net_1),
))

t.add_resource(ec2.Route(
    'NatRoute',
    RouteTableId=Ref(private_route_table),
    DestinationCidrBlock='0.0.0.0/0',
    NatGatewayId=Ref(nat),
))

# Nat Gateway 2
nat_eip_2 = t.add_resource(ec2.EIP(
    'NatGateway2EIP',
    Domain="vpc",
))

nat_2 = t.add_resource(ec2.NatGateway(
    'NatGateway2',
    AllocationId=GetAtt(nat_eip_2, 'AllocationId'),
    SubnetId=Ref(public_net_2),
))

t.add_resource(ec2.Route(
    'NatRoute2',
    RouteTableId=Ref(private_route_table_2),
    DestinationCidrBlock='0.0.0.0/0',
    NatGatewayId=Ref(nat_2),
))

# Outputs
t.add_output(Output(
    'VPCId',
    Value=Ref(vpc),
    Description='VPC ID',
))

fh = open("template.yaml", "a")
fh.writelines(t.to_yaml())
fh.close()