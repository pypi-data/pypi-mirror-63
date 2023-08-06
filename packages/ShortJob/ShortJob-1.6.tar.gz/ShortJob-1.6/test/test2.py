#!/usr/bin/env python
import os
from ShortJob import MkMulJob

mk = MkMulJob.MkMulJob(["run.C", "test.py", "run.sh"])
for i  in range(10):
    mk.Make(i, [(3.14, 2.3, "a"), ("a", "b", "c"), ("a")])
