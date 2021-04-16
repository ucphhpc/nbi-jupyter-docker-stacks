import json
import os
import argparse
from fcntl import flock, LOCK_EX
from jupyter_client import kernelspec

PACKAGE_NAME = "update_kernel_spec"


class ParseKwargs(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, dict())
        for value in values:
            key, value = value.split("=")
            getattr(namespace, self.dest)[key] = value


parser = argparse.ArgumentParser(prog=PACKAGE_NAME)
argument_group = parser.add_argument_group(title="Update Kernel Spec Arguments")
argument_group.add_argument("kernel_name")
argument_group.add_argument("--env-kwargs", nargs="*", action=ParseKwargs)
argument_group.add_argument("-v", "--verbose", default=False, action="store_true")
args, extras = parser.parse_known_args()


def update_kernel(spec):
    kernel_path = os.path.join(spec.resource_dir, "kernel.json")
    kernel_lock_path = os.path.join(spec.resource_dir, "kernel.json.lock")
    with open(kernel_lock_path, "a") as lock_file:
        flock(lock_file.fileno(), LOCK_EX)
        with open(kernel_path, "w") as kernel_file:
            kernel_dict = spec.to_dict()
            json.dump(kernel_dict, kernel_file, indent=4)
    return True


def main():
    kernel_name = args.kernel_name
    kernel_env_kwargs = args.env_kwargs
    kernelspecs = kernelspec.find_kernel_specs()
    if not kernelspecs:
        if args.verbose:
            print("No kernelspecs were found: {}".format(kernelspecs))
        exit(0)

    if kernel_name not in kernelspecs:
        print(
            "The target kernel: {} does not exist on this system, the avilable are: {}".format(
                kernel_name, kernelspecs
            )
        )
        exit(0)

    kernel_spec = kernelspec.get_kernel_spec(kernel_name)
    # Update the kernel spec env with provided environment
    if kernel_env_kwargs:
        for key, value in kernel_env_kwargs.items():
            # Expand value if environement variables are used
            expanded_value = os.path.expandvars(value)
            kernel_spec.env.update({key: expanded_value})

    if update_kernel(kernel_spec) and args.verbose:
        print("Updated kernel: {}".format(kernel_name))


if __name__ == "__main__":
    main()
