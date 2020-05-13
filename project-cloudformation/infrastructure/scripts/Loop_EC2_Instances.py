"""
Your module description
"""
from troposphere import Ref, Template
import troposphere.ec2 as ec2

template = Template()

envs = ['dev', 'test', 'prod']

for x in envs:
    instancename = x + "Ec2"
    ec2_instance = template.add_resource(ec2.Instance(
        instancename,
        ImageId="ami-a7a242da",
        InstanceType="t2.nano",
        ))

fh = open("template.yaml", "a")
fh.writelines(template.to_yaml())
fh.close()