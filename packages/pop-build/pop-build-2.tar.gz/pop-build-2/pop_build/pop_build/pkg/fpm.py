# Import python libs
import tempfile
import os
import shutil
import subprocess


def build(hub, bname):
    """
    Build a new package using fpm
    """
    opts = hub.pop_build.BUILDS[bname]
    root = os.path.join(tempfile.mkdtemp(), opts["name"])
    os.makedirs(root)
    # Move files into a tempdir, return config files
    # Set the specific flags, like checksum type, based on the pkg_tgt
    # Run fpm
    config = _prep_tmpdir(
        hub,
        opts["name"],
        root,
        opts["pkg"],
        opts["pkg_tgt"],
        opts["dir"],
        opts["onedir"],
    )
    cmd = _get_cmd(
        opts["name"], root, opts["pkg"], opts["pkg_tgt"], opts["version"], config
    )
    _run_fpm(cmd)
    # shutil.rmtree(root)


def _run_fpm(cmd):
    subprocess.run(cmd)


def _get_fpm_tgt(pkg_tgt):
    """
    Turn the pkg_tgt into a target for fpm
    """
    rpm = ("rhel", "opensuse", "suse", "cent", "sles", "sle")
    deb = ("ubuntu", "deb")
    pacman = ("arch", "manjaro")
    if pkg_tgt.lower().startswith(rpm):
        return "rpm"
    elif pkg_tgt.startswith(deb):
        return "deb"
    elif pkg_tgt.lower().startswith(pacman):
        return "pacman"


def _get_cmd(name, root, pkg, pkg_tgt, version, config):
    """
    Return the command line args list to shell out to fpm with
    """
    fpm_tgt = _get_fpm_tgt(pkg_tgt)
    cmd = ["fpm", "-s", "dir", "-n", name, "-t", fpm_tgt]
    for fn in sorted(list(config)):
        cmd.append("--config-files")
        cmd.append(fn)
    if fpm_tgt == "rpm":
        cmd.append("--rpm-digest")
        cmd.append("sha512")
    cmd.append("--version")
    cmd.append(version)
    cmd.append("-C")
    cmd.append(root)
    return cmd


def _prep_tmpdir(hub, name, root, pkg, pkg_tgt, dir_, onedir):
    """
    Make the tempdir and copy the configured files into it
    """
    dist = os.path.join(dir_, "dist", name)
    configs = set()
    bin_tgt = os.path.join(root, "usr", "bin")
    if onedir:
        tree_tgt = os.path.join(root, "opt", name, "bins")
        os.makedirs(tree_tgt)
        shutil.copytree(dist, tree_tgt)
    else:
        os.makedirs(bin_tgt)
        shutil.copy(dist, bin_tgt)
    for tpath, spath in pkg.get("config", {}).items():
        tpath = tpath.strip(os.sep)
        src = os.path.join(dir_, spath)
        tgt = os.path.join(root, tpath)
        tgt_dir = os.path.dirname(tgt)
        if not os.path.isdir(tgt_dir):
            os.makedirs(tgt_dir)
        shutil.copy(src, tgt)
        configs.add(tpath)
    for spath in pkg.get("scripts", {}):
        src = os.path.join(dir_, spath)
        if not os.path.isdir(bin_tgt):
            os.makedirs(bin_tgt)
        shutil.copy(src, bin_tgt)
    if pkg_tgt in hub.pop_build.SYSTEMD:
        tgt = os.path.join(root, hub.pop_build.SYSTEMD_DIR)
        for spath in pkg.get("systemd", {}):
            if not os.path.isdir(tgt):
                os.makedirs(tgt)
            src = os.path.join(dir_, spath)
            shutil.copy(src, tgt)
    if pkg_tgt in hub.pop_build.SYSV:
        tgt = os.path.join(root, hub.pop_build.SYSV_DIR)
        for spath in pkg.get("sysv", {}):
            if not os.path.isdir(tgt):
                os.makedirs(tgt)
            src = os.path.join(dir_, spath)
            shutil.copy(src, tgt)
    return configs
