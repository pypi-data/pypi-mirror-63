import os
import subprocess
from .coreir_ import InsertWrapCasts
from ..compiler import Compiler
from ..frontend import coreir_ as coreir_frontend
from ..passes import InstanceGraphPass
from ..passes.insert_coreir_wires import InsertCoreIRWires


def _make_verilog_cmd(deps, basename, opts):
    cmd = "coreir"
    if deps:
        cmd += f" -l {','.join(deps)}"
    cmd += f" -i {basename}.json"
    if opts.get("split", ""):
        split = opts["split"]
        cmd += f" -o \"{split}/*.v\" -s"
    else:
        cmd += f" -o {basename}.v"
    if opts.get("inline", False):
        cmd += " --inline"
    if opts.get("verilator_debug", False):
        cmd += " --verilator_debug"
    return cmd


class CoreIRCompiler(Compiler):
    def __init__(self, main, basename, opts):
        super().__init__(main, basename, opts)
        self.namespaces = self.opts.get("namespaces", ["global"])
        self.passes = opts.get("passes", [])
        if "markdirty" not in self.passes:
            self.passes.append("markdirty")
        self.deps = self.__deps()

    def compile(self):
        self.__compile_coreir()
        if self.opts.get("output_verilog", False):
            self.__compile_verilog()

    def __compile_coreir(self):
        backend = coreir_frontend.GetCoreIRBackend()
        InsertWrapCasts(self.main).run()
        InsertCoreIRWires(self.main).run()
        backend.compile(self.main)
        backend.context.run_passes(self.passes, self.namespaces)
        main_key = self.main.coreir_name
        backend.modules[main_key].save_to_file(self.basename + ".json")

    def __compile_verilog(self):
        # TODO(rsetaluri): Expose compilation to verilog in pycoreir rather than
        # calling the binary from the command line.
        cmd = _make_verilog_cmd(self.deps, self.basename, self.opts)
        ret = subprocess.run(cmd, shell=True).returncode
        if ret:
            raise RuntimeError(f"CoreIR cmd '{cmd}' failed with code {ret}")

        backend = coreir_frontend.GetCoreIRBackend()
        # TODO: We need fresh bind_files for each compile call
        for name, file in backend.sv_bind_files.items():
            filename = os.path.join(os.path.dirname(self.basename), name)
            with open(f"{filename}.sv", "w") as f:
                f.write(file)

        if self.opts.get("sv", False):
            subprocess.run(["mv", f"{self.basename}.v", f"{self.basename}.sv"])

    def __deps(self):
        deps = self.opts.get("coreir_libs", set())
        pass_ = InstanceGraphPass(self.main)
        pass_.run()
        for key, _ in pass_.tsortedgraph:
            if key.coreir_lib:
                deps.add(key.coreir_lib)
            elif hasattr(key, "wrappedModule"):
                deps |= key.coreir_wrapped_modules_libs_used
        deps |= set(self.namespaces)
        return deps
