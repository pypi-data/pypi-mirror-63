from localstack.utils.aws import aws_models
kPyCK=super
kPyCa=None
kPyCY=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  kPyCK(LambdaLayer,self).__init__(arn)
  self.cwd=kPyCa
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class RDSDatabase(aws_models.Component):
 def __init__(self,kPyCY,env=kPyCa):
  kPyCK(RDSDatabase,self).__init__(kPyCY,env=env)
 def name(self):
  return self.kPyCY.split(':')[-1]
# Created by pyminifier (https://github.com/liftoff/pyminifier)
