from python_terraform import *
from .devops_terraform_build import DevopsTerraformBuild


def add_aws_mixin_config(config, account_name):
    config.update({'AwsMixin':
                   {'account_name': account_name}})
    return config


class AwsMixin(DevopsTerraformBuild):

    def __init__(self, project, config):
        super().__init__(project, config)
        aws_mixin_config = config['AwsMixin']
        self.account_name = aws_mixin_config['account_name']
        
    def backend_config(self):
        return "backend." + self.account_name + "." + self.stage + ".properties"

    def project_vars(self):
        ret = super().project_vars()
        ret.update({'account_name': self.account_name})
        return ret

    def init_client(self):
        tf = Terraform(working_dir=self.build_path())
        tf.init(backend_config=self.backend_config())
        if self.use_workspace:
            try:
                tf.workspace('select', slef.stage)
            except:
                tf.workspace('new', self.stage)
        return tf

    def plan(self):
        tf = self.init_client()
        tf.plan(capture_output=False, var=self.project_vars(),
                var_file=self.backend_config())

    def apply(self, p_auto_approve=False):
        tf = self.init_client()
        tf.apply(capture_output=False, auto_approve=p_auto_approve,
                 var=self.project_vars(), var_file=self.backend_config())
        self.write_output(tf)

    def destroy(self, p_auto_approve=False):
        tf = self.init_client()
        tf.destroy(capture_output=False, auto_approve=p_auto_approve,
                   var=self.project_vars(), var_file=self.backend_config())
