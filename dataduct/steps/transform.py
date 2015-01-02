"""
ETL step wrapper for shell command activity can be executed on Ec2 / EMR
"""
from .etl_step import ETLStep
from ..pipeline import ShellCommandActivity
from ..s3 import S3File
from ..utils.helpers import exactly_one
from ..utils.exceptions import ETLInputError
from ..utils import constants as const

SCRIPT_ARGUMENT_TYPE_STRING = 'string'
SCRIPT_ARGUMENT_TYPE_SQL = 'sql'


class TransformStep(ETLStep):
    """Transform Step class that helps run scripts on resouces
    """

    def __init__(self,
                 command=None,
                 script=None,
                 output_node=None,
                 script_arguments=None,
                 additional_s3_files=None,
                 depends_on=None,
                 output_path=None,
                 **kwargs):
        """Constructor for the TransformStep class

        Args:
            command(str): command to be executed directly
            script(path): local path to the script that should executed
            output_node(dict): output data nodes from the transform
            script_arguments(list of str): list of arguments to the script
            additional_s3_files(list of S3File): additional files used
            **kwargs(optional): Keyword arguments directly passed to base class
        """
        if not exactly_one(command, script):
            raise ETLInputError('Both command or script found')

        super(TransformStep, self).__init__(**kwargs)

        if depends_on is not None:
            self._depends_on = depends_on

        # Create output_node based on output_path
        base_output_node = self.create_s3_data_node(
            self.get_output_s3_path(output_path))

        # Create S3File if script path provided
        if script:
            script = self.create_script(S3File(path=script))

        script_arguments = self.translate_arguments(script_arguments)

        self.create_pipeline_object(
            object_class=ShellCommandActivity,
            input_node=self._input_node,
            output_node=base_output_node,
            resource=self.resource,
            schedule=self.schedule,
            script_uri=script,
            script_arguments=script_arguments,
            command=command,
            max_retries=self.max_retries,
            depends_on=self.depends_on,
            additional_s3_files=additional_s3_files,
        )

        # Translate output nodes if output map provided
        if output_node:
            self._output = self.create_output_nodes(
                base_output_node, output_node)
        else:
            self._output = base_output_node

    def translate_arguments(self, script_arguments):
        """Translate script argument to lists

        Args:
            script_arguments(list of str/dict): arguments to the script

        Note:
            Dict: (k -> v) is turned into an argument "--k=v"
            List: Either pure strings or dictionaries with name, type and value
        """
        if script_arguments is None:
            return script_arguments

        elif isinstance(script_arguments, list):
            result = list()
            for argument in script_arguments:
                if isinstance(argument, dict):
                    argument_type = argument.get('type',
                                                 SCRIPT_ARGUMENT_TYPE_STRING)
                    if argument_type == SCRIPT_ARGUMENT_TYPE_SQL:
                        # TODO: Change to SQL Parsing
                        result.append(self.input_format(
                            argument['name'], argument['value']))
                    else:
                        result.append(self.input_format(
                            argument['name'], argument['value']))
                else:
                    result.append(str(argument))
            return result

        elif isinstance(script_arguments, dict):
            return [self.input_format(key, value)
                    for key, value in script_arguments.iteritems()]

        elif isinstance(script_arguments, str):
            return [script_arguments]

        else:
            raise ETLInputError('Script Arguments for unrecognized type')

    @staticmethod
    def input_format(key, value):
        """Format the key and value to command line arguments
        """
        return ''.join('--', key, '=', value)

    @classmethod
    def arguments_processor(cls, etl, input_args):
        """Parse the step arguments according to the ETL pipeline

        Args:
            etl(ETLPipeline): Pipeline object containing resources and steps
            step_args(dict): Dictionary of the step arguments for the class
        """
        step_args = cls.base_arguments_processor(etl, input_args)
        if step_args.pop('resource_type', None) == const.EMR_CLUSTER_STR:
            step_args['resource'] = etl.emr_cluster
        else:
            step_args['resource'] = etl.ec2_resource

        return step_args
