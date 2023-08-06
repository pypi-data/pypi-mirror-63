name = "ai_pipeline_params"

import kfp.dsl as dsl

def use_ai_pipeline_params(secret_name, secret_volume_mount_path='/app/secrets', image_pull_policy='IfNotPresent'):
    def _use_ai_pipeline_params(task):
        from kubernetes import client as k8s_client
        task = task.add_volume(k8s_client.V1Volume(name=secret_name,  # secret_name as volume name
                                                   secret=k8s_client.V1SecretVolumeSource(secret_name=secret_name)))
        task.container.add_volume_mount(k8s_client.V1VolumeMount(mount_path=secret_volume_mount_path, 
                                                                 name=secret_name))
        task.container.set_image_pull_policy(image_pull_policy)
        return task
    return _use_ai_pipeline_params

def set_ai_pipeline_params(secret_name, arguments, file_outputs, secret_file="creds.ini"):
    args = ['/app/config.py'] + arguments
    return dsl.ContainerOp(
        name = "config",
        image = "aipipeline/wml-config",
        command = ['python3'],
        arguments = args,
        file_outputs = file_outputs)
