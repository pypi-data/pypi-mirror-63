#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function

import sys

from .tools import logger, run_process, find_output_arg, try_to_wrap_executable, execute, check_program
from .constants import LD, WASI_SYSROOT



def run(args):
    # has_sysroot = any([arg.startswith("--sysroot") for arg in args])
    # has_target = any([arg.startswith("--target") for arg in args])

    # if not has_sysroot:
    #     args.append("--sysroot={}".format(WASI_SYSROOT))
    
    # if not has_target:
    #     args.append("--target=wasm32-wasi")
    check_program(LD)
    proc_args = [LD]+args[1:]
    return_code = run_process(proc_args, check=False)
    target, outargs = find_output_arg(args)
    args.append('-lwasi-emulated-mman')
    if target:
        try_to_wrap_executable(target)
    return return_code


if __name__ == '__main__':
    execute(run)
