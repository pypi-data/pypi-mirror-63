from localstack.utils.aws import aws_models
nOBJs=super
nOBJr=None
nOBJq=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  nOBJs(LambdaLayer,self).__init__(arn)
  self.cwd=nOBJr
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class RDSDatabase(aws_models.Component):
 def __init__(self,nOBJq,env=nOBJr):
  nOBJs(RDSDatabase,self).__init__(nOBJq,env=env)
 def name(self):
  return self.nOBJq.split(':')[-1]
# Created by pyminifier (https://github.com/liftoff/pyminifier)
