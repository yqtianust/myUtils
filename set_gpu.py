import os
import subprocess

gpu_env = os.environ.copy()
if 'CUDA_VISIBLE_DEVICES' in gpu_env.keys():
    print(gpu_env['CUDA_VISIBLE_DEVICES'])
gpu_env['CUDA_VISIBLE_DEVICES']='1'
subprocess.Popen(args=["python3", "print_gpu.py"], env=gpu_env).wait()
