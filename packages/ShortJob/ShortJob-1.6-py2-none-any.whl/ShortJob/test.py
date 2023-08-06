from MkMulJob import MkMulJob
mk = MkMulJob(["cut.cxx", "fit"])
mk.Make(1, [[1.1, 1.2,0], ["d<1"]])
