#!/usr/bin/env python
from ShortJob import MkMulJob

mk = MkMulJob.MkMulJob(["cut.cxx", "fit"])
mk.Make(1, [[1.1, 1.2,0], ["d<1"]])
