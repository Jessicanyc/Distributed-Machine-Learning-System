# this script is responsible for both compiling the Kubeflow pipeline and triggering its deployment and execution on k8s cluster.
import kfp
from kfp import compiler
import sys

def compile_and_deploy_pipeline(pipeline_script, host_url, pipeline_name, experiment_name):
    # Dynamically import the pipeline definition module
    spec = importlib.util.spec_from_file_location("module.name", pipeline_script)
    pipeline_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(pipeline_module)

    # Compile the pipeline
    pipeline_func = getattr(pipeline_module, pipeline_name)
    pipeline_filename = pipeline_func.__name__ + '.zip'
    compiler.Compiler().compile(pipeline_func, pipeline_filename)

    # Connect to the Kubeflow Pipelines server
    client = kfp.Client(host=host_url)

    # Upload the compiled pipeline
    pipeline = client.upload_pipeline(pipeline_filename, pipeline_name)

    # Create or get existing experiment
    experiment = client.create_experiment(experiment_name)

    # Run the pipeline
    run = client.run_pipeline(experiment.id, f'{pipeline_name} run', pipeline_id=pipeline.id)

if __name__ == "__main__":
    # Usage: python deploy_pipeline.py <path_to_pipeline.py> <pipeline_function_name> <kubeflow_host> <experiment_name>
    compile_and_deploy_pipeline(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
