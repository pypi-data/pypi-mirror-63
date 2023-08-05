# coding: utf-8

"""
ROOT-related utilities.
"""


__all__ = ["import_ROOT", "hadd_task"]


import six

from law.target.local import LocalFileTarget, LocalDirectoryTarget
from law.util import map_verbose, interruptable_popen, human_bytes, quote_cmd


_ROOT = None


def import_ROOT(batch=True, ignore_cli=True, reset=False):
    """
    Imports, caches and returns the ROOT module and sets certain flags when it was not already
    cached. When *batch* is *True*, the module is loaded in batch mode. When *ignore_cli* is *True*,
    ROOT's command line parsing is disabled. When *reset* is *True*, the two settings are enforced
    independent of whether the module was previously cached or not. This entails enabling them in
    case they were disabled before.
    """
    global _ROOT

    was_empty = _ROOT is None

    if was_empty:
        import ROOT
        _ROOT = ROOT

    if was_empty or reset:
        _ROOT.gROOT.SetBatch(batch)

    if was_empty or reset:
        _ROOT.PyConfig.IgnoreCommandLineOptions = ignore_cli

    return _ROOT


def hadd_task(task, inputs, output, cwd=None):
    """
    This method is intended to be used by tasks that are supposed to merge root files, e.g. when
    inheriting from :py:class:`law.contrib.tasks.MergeCascade`. *inputs* should be a sequence of
    local targets that represent the files to merge into *output*. *cwd* is the working directory
    in which hadd is invoked. When empty, a temporary directory is used. The *task* itself is
    used to print and publish messages via its :py:meth:`law.Task.publish_message` and
    :py:meth:`law.Task.publish_step` methods.
    """
    # ensure inputs are targets
    inputs = [
        LocalFileTarget(inp) if isinstance(inp, six.string_types) else inp
        for inp in inputs
    ]

    # ensure output is a target
    if isinstance(output, six.string_types):
        output = LocalFileTarget(output)

    # default cwd
    if not cwd:
        cwd = LocalDirectoryTarget(is_tmp=True)
    elif isinstance(cwd, six.string_types):
        cwd = LocalDirectoryTarget(cwd)
    cwd.touch()

    # fetch inputs
    with task.publish_step("fetching inputs ...", runtime=True):
        def fetch(inp):
            inp.copy_to_local(cwd.child(inp.unique_basename, type="f"), cache=False)
            return inp.unique_basename

        def callback(i):
            task.publish_message("fetch file {} / {}".format(i + 1, len(inputs)))

        bases = map_verbose(fetch, inputs, every=5, callback=callback)

    # start merging
    with task.publish_step("merging ...", runtime=True):
        with output.localize("w", cache=False) as tmp_out:
            if len(bases) == 1:
                tmp_out.path = cwd.child(bases[0]).path
            else:
                # merge using hadd
                cmd = quote_cmd(["hadd", "-n", "0", "-d", cwd.path, tmp_out.path] + bases)
                code = interruptable_popen(cmd, shell=True, executable="/bin/bash",
                    cwd=cwd.path)[0]
                if code != 0:
                    raise Exception("hadd failed")

                task.publish_message("merged file size: {:.2f} {}".format(
                    *human_bytes(tmp_out.stat.st_size)))
