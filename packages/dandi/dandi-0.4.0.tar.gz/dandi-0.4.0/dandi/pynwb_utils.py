import h5py
import re
import warnings
from distutils.version import LooseVersion
from collections import Counter

import pynwb
from pynwb import NWBHDF5IO

from . import get_logger

lgr = get_logger()

from .consts import (
    metadata_nwb_file_fields,
    metadata_nwb_computed_fields,
    metadata_nwb_subject_fields,
)
from .support.cache import PersistentCache

from . import __version__

# strip away possible development version marker
dandi_rel_version = __version__.split("+", 1)[0]
dandi_cache_tokens = [pynwb.__version__, dandi_rel_version]
metadata_cache = PersistentCache(name="metadata", tokens=dandi_cache_tokens)
validate_cache = PersistentCache(name="validate", tokens=dandi_cache_tokens)


def get_nwb_version(filepath):
    """Return a version of the NWB standard used by a file

    Returns
    -------
    str or None
       None if there is no version detected
    """
    with h5py.File(filepath, "r") as h5file:
        # 2.x stored it as an attribute
        try:
            return h5file.attrs["nwb_version"]
        except KeyError:
            pass

        # 1.x stored it as a dataset
        try:
            return h5file["nwb_version"][...].tostring().decode()
        except:
            lgr.debug("%s has no nwb_version" % filepath)


def get_neurodata_types_to_modalities_map():
    """Return a dict to map neurodata types known to pynwb to "modalities"

    It is an ugly hack, largely to check feasibility.
    It would base modality on the filename within pynwb providing that neural
    data type
    """
    import inspect

    ndtypes = {}

    # TODO: if there are extensions, they might have types subclassed from the base
    # types.  There might be a map within pynwb (pynwb.get_type_map?) to return
    # known extensions. We would need to go along MRO to the base to figure out
    # "modality"
    #
    # They import all submods within __init__
    for a, v in pynwb.__dict__.items():
        if not (inspect.ismodule(v) and v.__name__.startswith("pynwb.")):
            continue
        for a_, v_ in v.__dict__.items():
            # now inspect all things within and get neural datatypes
            if inspect.isclass(v_) and issubclass(v_, pynwb.core.NWBMixin):
                ndtype = v_.__name__

                v_split = v_.__module__.split(".")
                if len(v_split) != 2:
                    print("Skipping %s coming from %s" % v_, v_.__module__)
                    continue
                modality = v_split[1]  # so smth like ecephys

                if ndtype in ndtypes:
                    if ndtypes[ndtype] == modality:
                        continue  # all good, just already known
                    raise RuntimeError(
                        "We already have %s pointing to %s, but now got %s"
                        % (ndtype, ndtypes[ndtype], modality)
                    )
                ndtypes[ndtype] = modality

    return ndtypes


@metadata_cache.memoize_path
def get_neurodata_types(filepath):
    with h5py.File(filepath, "r") as h5file:
        all_pairs = _scan_neurodata_types(h5file)

    # so far descriptions are useless so let's just output actual names only
    # with a count if there is multiple
    # return [': '.join(filter(bool, p)) for p in all_pairs]
    names = [p[0] for p in all_pairs if p[0] not in {"NWBFile"}]
    counts = Counter(names)
    out = []
    for name, count in sorted(counts.items()):
        if count > 1:
            out.append("%s (%d)" % (name, count))
        else:
            out.append(name)
    return out


def _scan_neurodata_types(grp):
    out = []
    if "neurodata_type" in grp.attrs:
        out.append((grp.attrs["neurodata_type"], grp.attrs.get("description", None)))
    for v in list(grp.values()):
        if isinstance(v, h5py._hl.group.Group):
            out += _scan_neurodata_types(v)
    return out


def _get_pynwb_metadata(path):
    out = {}
    with NWBHDF5IO(path, "r", load_namespaces=True) as io:
        nwb = io.read()
        for key in metadata_nwb_file_fields:
            value = getattr(nwb, key)
            if isinstance(value, h5py.Dataset):
                # serialize into a basic container (list), since otherwise
                # it would be a closed Dataset upon return
                value = list(value)
            out[key] = value

        # .subject can be None as the test shows
        for subject_feature in metadata_nwb_subject_fields:
            out[subject_feature] = getattr(nwb.subject, subject_feature, None)
        # Add a few additional useful fields

        # "Custom" DANDI extension by Ben for now to contain additional metadata
        # not present in nwb-schema
        dandi_icephys = getattr(nwb, "lab_meta_data", {}).get(
            "DandiIcephysMetadata", None
        )
        if dandi_icephys:
            out.update(dandi_icephys.fields)

        # Counts
        for f in metadata_nwb_computed_fields:
            if f in ("nwb_version", "nd_types"):
                continue
            if not f.startswith("number_of_"):
                raise NotImplementedError(
                    "ATM can only compute number_of_ fields. Got {}".format(f)
                )
            key = f[len("number_of_") :]
            out[f] = len(getattr(nwb, key, []) or [])

    return out


def validate(path):
    """Run validation on a file and return errors

    In case of an exception being thrown, an error message added to the
    returned list of validation errors

    Parameters
    ----------
    path: str or Path
    """
    path = str(path)  # Might come in as pathlib's PATH
    try:
        with pynwb.NWBHDF5IO(path, "r", load_namespaces=True) as reader:
            errors = pynwb.validate(reader)
    except Exception as exc:
        errors = [f"Failed to validate {path}: {exc}"]

    # To overcome
    #   https://github.com/NeurodataWithoutBorders/pynwb/issues/1090
    #   https://github.com/NeurodataWithoutBorders/pynwb/issues/1091
    re_ok_prior_210 = re.compile(
        "general/(experimenter|related_publications)\): "
        "incorrect shape - expected an array of shape .\[None\]."
    )
    try:
        version = get_nwb_version(path)
    except:
        # we just will not remove any errors
        pass
    else:
        if version and LooseVersion(version) < "2.1.0":
            errors_ = errors[:]
            errors = [e for e in errors if not re_ok_prior_210.search(str(e))]
            if errors != errors_:
                lgr.debug(
                    "Filtered out %d validation errors on %s",
                    len(errors_) - len(errors),
                    path,
                )
    return errors


# Many commands might be using load_namespaces but it causes HDMF to whine if there
# is no cached name spaces in the file.  It is benign but not really useful
# at this point, so we ignore it although ideally there should be a formal
# way to get relevant warnings (not errors) from PyNWB.  It is a bad manner
# to have this as a side effect of the importing this module, we should add/remove
# that filter in our top level commands
def ignore_benign_pynwb_warnings():
    #   See https://github.com/dandi/dandi-cli/issues/14 for more info
    for s in (
        "No cached namespaces found .*",
        "ignoring namespace '.*' because it already exists",
    ):
        warnings.filterwarnings("ignore", s, UserWarning)


def get_object_id(path):
    """Read, if present an object_id

    if not available -- would simply raise a corresponding exception
    """
    with h5py.File(path, "r") as f:
        return f.attrs["object_id"]
