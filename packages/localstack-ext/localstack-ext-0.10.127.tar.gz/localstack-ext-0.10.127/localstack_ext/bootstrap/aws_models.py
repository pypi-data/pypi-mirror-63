from localstack.utils.aws import aws_models
BokqR=super
Bokqn=None
BokqL=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  BokqR(LambdaLayer,self).__init__(arn)
  self.cwd=Bokqn
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class RDSDatabase(aws_models.Component):
 def __init__(self,BokqL,env=Bokqn):
  BokqR(RDSDatabase,self).__init__(BokqL,env=env)
 def name(self):
  return self.BokqL.split(':')[-1]
# Created by pyminifier (https://github.com/liftoff/pyminifier)
