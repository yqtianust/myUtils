import os
gpu_env = os.environ.copy()
print(gpu_env['CUDA_VISIBLE_DEVICES'], file=open("./test.txt", "w"))
