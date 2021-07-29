import os.path
import subprocess
import time
from .others import get_timestamp
import argparse


def get_parser():
    parser = argparse.ArgumentParser("Run multiple jobs in multiple GPUs")
    parser.add_argument('-g', '--gpus', help="gpus to run the jobs", nargs='+', type=int)
    parser.add_argument('-j', '--job_per_gpu', help="jobs per gpu", type=int, default=1)

    return parser


def parallel_in_multiple_gpus(commands_list, output_file_path_list=None, GPU_list=None, jobs_per_GPU=1):
    if output_file_path_list is None:
        output_file_path_list = [None for ele in commands_list]

    if GPU_list is None:
        GPU_list = [1, 2, 3, 4, 5, 6, 7]

    GPU_tasks = {}
    for i in GPU_list:
        for j in range(0, jobs_per_GPU):
            GPU_tasks[j * 10 + i] = {
                "opened_file": None,
                "cmd": None,
                "process": None
            }
    print("Start to spawn the process")

    continue_check = True
    while continue_check:

        running_task = 0
        for gpu in GPU_tasks.keys():
            proc = GPU_tasks[gpu]["process"]
            add_new_task = False
            if proc is None:
                add_new_task = True
            else:
                return_code = proc.poll()
                if return_code is None:
                    # not finished
                    running_task += 1
                else:
                    # finished
                    add_new_task = True
                    GPU_tasks[gpu]["process"] = None

                    opened_file = GPU_tasks[gpu]["opened_file"]
                    if opened_file is not None:
                        opened_file.close()
                        GPU_tasks[gpu]["opened_file"] = None

                    finished_cmd = GPU_tasks[gpu]["cmd"]
                    if return_code == 0:
                        print("{} Done: {}".format(get_timestamp(), finished_cmd))
                    else:
                        print("{} MyError! {}".format(get_timestamp(), finished_cmd))
                    GPU_tasks[gpu]["cmd"] = None

            if add_new_task:
                if len(commands_list) > 0:
                    cmd = commands_list.pop(0)
                    output_file_path = output_file_path_list.pop(0)
                    gpu_env = os.environ.copy()
                    gpu_env["CUDA_VISIBLE_DEVICES"] = str(gpu % 10)
                    if output_file_path is not None:
                        f = open(output_file_path, 'w')
                        GPU_tasks[gpu]["opened_file"] = f
                        GPU_tasks[gpu]["process"] = subprocess.Popen(cmd, env=gpu_env, stdout=f, stderr=f)
                        print("{} Start: {} at GPU {} to path {}".format(get_timestamp(), cmd, gpu % 10,
                                                                         output_file_path))
                        print("{} TODO: {}".format(get_timestamp(), len(commands_list)))
                    else:
                        GPU_tasks[gpu]["opened_file"] = None
                        GPU_tasks[gpu]["process"] = subprocess.Popen(cmd, env=gpu_env)
                        print("{} Start: {} at GPU {}".format(get_timestamp(), cmd, gpu % 10))
                        print("{} TODO: {}".format(get_timestamp(), len(commands_list)))

                    GPU_tasks[gpu]["cmd"] = " ".join(cmd)
                    running_task += 1

        if len(commands_list) == 0 and running_task == 0:
            continue_check = False
        time.sleep(30)


def test_parallel_in_multiple_gpus():
    models = ["alexnet", "densenet121", "densenet161", "densenet169", "densenet201", "resnet101", "resnet152",
              "resnet18", "resnet34", "resnet50", "squeezenet1_0", "squeezenet1_1", "vgg11",
              "vgg11_bn", "vgg13", "vgg13_bn", "vgg16", "vgg16_bn", "vgg19", "vgg19_bn"][5:]
    interpolation_methods = [
        "NEAREST", "BILINEAR", "BICUBIC", "BOX", "HAMMING", "LANCZOS",
    ]
    output_dir = "./test_log_pytorch/"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    commands_list = []
    output_file_path_list = []
    for model in models:
        for interpolation in interpolation_methods:
            output_file_path_list.append(output_dir + "{}_{}.log".format(model, interpolation))

            cmd = ["python3", "main_val.py",
                   "-j", "8", "-b", "64", "--seed", "1",
                   "-a", model,
                   "--pretrained",
                   "--evaluate", "/ssddata/ytianas/ILSVRC2012_slim/raw-data/",
                   "--eval-interpolation", interpolation]
            # capture_output=False,
            # the above parameter can only be used after python 3.7
            commands_list.append(cmd)

    parallel_in_multiple_gpus(commands_list, output_file_path_list)


if __name__ == '__main__':
    print("test parallel_in_multiple_gpus")
    # test_parallel_in_multiple_gpus()

    args = get_parser().parse_args()
    print(args)