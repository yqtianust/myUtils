# A tool to run multiple jobs in multiple GPUs

You can specify how many jobs per GPU. 

```python
import os, sys
from myUtils.parallelCMDinGPU import parallel_in_multiple_gpus, get_parser


def attack_mnist():
    pass

def attack_cifar():
    pass


if __name__ == '__main__':
    parser = get_parser()
    parser.add_argument("--job", required=True, type=str)

    args = parser.parse_args()

    if args.gpus is None:
        args.gpus = [0, 1]

    this_module = sys.modules[__name__]

    try:
        f = getattr(this_module, args.job)()
    except AttributeError:
        print("This is not a valid job in the following list")
        keys = list(this_module.__dict__.keys())
        for key in keys:
            if callable(this_module.__dict__[key]):
                if key != "get_parser" and key != "parallel_in_multiple_gpus":
                    print("\t" + key)
```