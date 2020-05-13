from troposphere import FindInMap, GetAtt, Join
from troposphere import Output, Parameter, Ref, Select, Tags, Template, ec2

t = Template()

keyname_param = t.add_parameter(Parameter(
    "KeyName",
    Description="Name of an existing EC2 KeyPair to enable SSH "
                "access to the instance",
    Type="String",
))

vpcid_param = t.add_parameter(Parameter(
    "VpcID",
    Description="VpcId of your existing Virtual Private Cloud (VPC)",
    Type="String",
))

subnetid_param = t.add_parameter(Parameter(
    "SubnetId",
    Description="SubnetId of an existing subnet (for the primary network) in "
                "your Virtual Private Cloud (VPC)" "access to the instance",
    Type="String",
))

secondary_ip_param = t.add_parameter(Parameter(
    "SecondaryIPAddressCount",
    Description="Number of secondary IP addresses to assign to the network "
                "interface (1-5)",
    ConstraintDescription="must be a number from 1 to 5.",
    Type="Number",
    Default="1",
    MinValue="1",
    MaxValue="5",
))

sshlocation_param = t.add_parameter(Parameter(
    "SSHLocation",
    Description="The IP address range that can be used to SSH to the "
                "EC2 instances",
    Type="String",
    MinLength="9",
    MaxLength="18",
    Default="0.0.0.0/0",
    AllowedPattern="(\\d{1,3})\\.(\\d{1,3})\\.(\\d{1,3})\\.(\\d{1,3})"
                   "/(\\d{1,2})",
    ConstraintDescription="must be a valid IP CIDR range of the "
                          "form x.x.x.x/x."
))

t.add_mapping('RegionMap', {
    "us-east-1": {"AMI": "ami-7f418316"},
    "us-west-1": {"AMI": "ami-951945d0"},
    "us-west-2": {"AMI": "ami-16fd7026"},
    "eu-west-1": {"AMI": "ami-24506250"},
    "sa-east-1": {"AMI": "ami-3e3be423"},
    "ap-southeast-1": {"AMI": "ami-74dda626"},
    "ap-northeast-1": {"AMI": "ami-dcfa4edd"}
})

eip1 = t.add_resource(ec2.EIP(
    "EIP1",
    Domain="vpc",
))

ssh_sg = t.add_resource(ec2.SecurityGroup(
    "SSHSecurityGroup",
    VpcId=Ref(vpcid_param),
    GroupDescription="Enable SSH access via port 22",
    SecurityGroupIngress=[
        ec2.SecurityGroupRule(
            IpProtocol="tcp",
            FromPort="22",
            ToPort="22",
            CidrIp=Ref(sshlocation_param),
        ),
    ],
))

eth0 = t.add_resource(ec2.NetworkInterface(
    "Eth0",
    Description="eth0",
    GroupSet=[Ref(ssh_sg), ],
    SourceDestCheck=True,
    SubnetId=Ref(subnetid_param),
    Tags=Tags(
        Name="Interface 0",
        Interface="eth0",
    ),
    SecondaryPrivateIpAddressCount=Ref(secondary_ip_param),
))

eipassoc1 = t.add_resource(ec2.EIPAssociation(
    "EIPAssoc1",
    NetworkInterfaceId=Ref(eth0),
    AllocationId=GetAtt("EIP1", "AllocationId"),
    PrivateIpAddress=GetAtt("Eth0", "PrimaryPrivateIpAddress"),
))

ec2_instance = t.add_resource(ec2.Instance(
    "EC2Instance",
    ImageId=FindInMap("RegionMap", Ref("AWS::Region"), "AMI"),
    KeyName=Ref(keyname_param),
    NetworkInterfaces=[
        ec2.NetworkInterfaceProperty(
            NetworkInterfaceId=Ref(eth0),
            DeviceIndex="0",
        ),
    ],
    Tags=Tags(Name="MyInstance",)
))

t.add_output([
    Output(
        "InstanceId",
        Description="InstanceId of the newly created EC2 instance",
        Value=Ref(ec2_instance),
    ),
    Output(
        "EIP1",
        Description="Primary public IP address for Eth0",
        Value=Join(" ", [
            "IP address", Ref(eip1), "on subnet", Ref(subnetid_param)
        ]),
    ),
    Output(
        "PrimaryPrivateIPAddress",
        Description="Primary private IP address of Eth0",
        Value=Join(" ", [
            "IP address", GetAtt("Eth0", "PrimaryPrivateIpAddress"),
            "on subnet", Ref(subnetid_param)
        ]),
    ),
    Output(
        "FirstSecondaryPrivateIPAddress",
        Description="First secondary private IP address of Eth0",
        Value=Join(" ", [
            "IP address",
            Select("0", GetAtt("Eth0", "SecondaryPrivateIpAddresses")),
            "on subnet", Ref(subnetid_param)
        ]),
    ),
])

fh = open("template.yaml", "a")
fh.writelines(t.to_yaml())
fh.close()