
from .spheres import Spheres
from . import cluster, configuration, utilities
import inspect
import itertools
import logging
import numpy as np
import os
import sys

logger = logging.getLogger(__name__)

def pocket(**opts):
    """Calculates the SES for a binding pocket

    Args:
      prot_file (str): filename for the input pdb file containing the peptidee
      mode (str): pocket identification mode (can be largest, all, or specific) (Default value = "largest")
      lig_file (str): filename for the input pdb file containing a ligand (Default value = None)
      coordinate ([float]): 3D coordinate used for pocket specification (Default value = None)
      resid (str): residue identifier for pocket specification (Default value = None)
      coordinates ([float]): 3D coordinate of an atom in a surrounding residue used for pocket specification (Default value = None)
      min_rad (float): radius for SES calculations (Default value = 1.4)
      max_rad (float): radius used to identify the outer, bulk solvent exposed surface (Default value = 3.4)
      lig_excl_rad (float): maximum distance from a provided ligand that can be included in calculated pockets (Default value = None)
      lig_incl_rad (float): minimum distance from a provided ligand that should be included in calculated pockets when solvent border is ambiguous (Default value = None)
      subdivide (bool): calculate subpockets? (Default value = False)
      min_volume (float): minimum volume of pockets returned when running in 'all' mode (Default value = 200)
      min_subpocket_rad (float): minimum radius that identifies distinct subpockets (Default value = 1.7)
      min_subpocket_surf_rad (float): radius used to calculate subpocket surfaces (Default value = 1.0)
      max_clusters (int): maximum number of clusters (Default value = None)
      min_cluster_size (int): minimum number of spheres in a proper cluster; used to eliminate insignificant subpockets (Default value = 50)
      inclusion_radius_buffer (float): buffer radius in excess of the nonextraneous radius from the identified pocket used to identify atoms pertinent to subpocket clustering (Default value = 1.0)
      radial_sampling (float): radial sampling used for subpocket clustering (Default value = 0.1)
      prefix (str): identifying string for output (Default value = None)
      output_dir (str): filename of the directory in which to place all output; can be absolute or relative (Default value = None)
      constrain_inputs (bool): restrict quantitative input parameters to tested values? (Default value = False)

    Returns:
      pockets ([Spheres]): a list of Spheres objects each of which contains the geometric information describing a distinct pocket or subpocket

    """




    p_s = Spheres(pdb=opts.get("prot_file"))
    logger.debug("Protein geometry read from {0}".format(opts.get("prot_file")))

    if opts.get("lig_file") is not None:
        l_s = Spheres(pdb=lig_file, r=opts.get("lig_incl_rad"))
        logger.debug("Ligand geometry read from {0}".format(opts.get("lig_file")))
        if opts.get("lig_incl_rad") is not None:
            logger.debug("Ligand-inclusion radius of {0} applied".format(opts.get("lig_incl_rad")))
    else:
        l_s = None

    pl_s = p_s + l_s

    pl_bs = pl_s.calculate_surface(probe_radius=opts.get("max_rad"))[0]
    logger.debug("Outer bulk-solvent surface calculated")

    pa_s = p_s + pl_bs
    if (l_s is not None) and (opts.get("lig_excl_rad") is not None):
        le_s = Spheres(xyz=l_s.xyzr, r=opts.get("lig_excl_rad"))
        le_bs = le_s.calculate_surface(probe_radius=opts.get("max_rad"))[0]
        pa_s = pa_s + le_bs
        logger.debug("Ligand-excluded radius of {0} applied".format(opts.get("lig_excl_rad")))

    if opts.get("mode") == "all":
        all_pockets = pa_s.calculate_surface(probe_radius=opts.get("min_rad"), all_components=True, minimum_volume=opts.get("minimum_volume"))
        for index, pocket in enumerate(all_pockets):
            pocket.name = "{0}_p{1}".format(opts.get("prefix"), index)
        logger.info("Pockets calculated using mode 'all': {0}".format(len(all_pockets)))
        if subdivide:
            logger.warning("Subpocket clustering not currently supported when calculating all independent pockets")
    else:
        if opts.get("mode") == "largest":
            bp_bs = pa_s.calculate_surface(probe_radius=opts.get("min_rad"), all_components=True, largest_only=True)[0]
            logger.info("Largest pocket identified")
        elif opts.get("mode") == "specific":
            if opts.get("coordinates") is not None:
                coordinate = opts.get("coordinates")
                logger.info("Specific pocket identified from coordinate: {0}".format(opts.get("coordinates")))
            elif opts.get("resid") is not None:
                resid = str(opts.get("resid"))
                chain = None
                if not resid[0].isdigit():
                    chain = resid[0]
                    resid = int(resid[1:])
                else:
                    resid = int(resid)
                res_coords = utilities.coordinates_for_resid(opts.get("prot_file"), resid=resid, chain=chain)
                p_bs = p_s.calculate_surface(probe_radius=opts.get("min_rad"))[0]
                coordinate = p_bs.nearest_coord_to_external(res_coords).reshape(1, -1)
                logger.info("Specific pocket identified from residue: {0} -> {1}".format(opts.get("resid"), coordinate))
            elif opts.get("residue_coordinates") is not None:
                p_bs = p_s.calculate_surface(probe_radius=opts.get("min_rad"))[0]
                coordinate = p_bs.nearest_coord_to_external(opts.get("residue_coordinates")).reshape(1, -1)
                logger.info("Specific pocket identified from residue coordinate: {0} -> {1}".format(opts.get("residue_coordinates"), coordinate))
            elif l_s is not None:
                lig_coords = l_s.xyz
                coordinate = np.mean(l_s.xyz, axis=0).reshape(1, -1)
                logger.info("Specific pocket identified from mean ligand position: {0}".format(coordinate))
            else:
                logger.error("A coordinate, ligand, or residue must be supplied to run in specific mode")
                return None
            bp_bs = pa_s.calculate_surface(probe_radius=opts.get("min_rad"), coordinate=coordinate)[0]
        else:
            logger.error("Unrecognized mode <{0}>--should be 'all', 'largest', or 'specific'".format(opts.get("mode")))
            return None

        bp_bs.name = "{0}_p0".format(opts.get("prefix"))

        if bp_bs.mesh.volume > pl_bs.mesh.volume:
            logger.error("Binding pocket not correctly identified--try an alternative method to specify the binding pocket")
            return None
        else:
            all_pockets = [bp_bs]

        if opts.get("subdivide"):
            all_pockets.extend(subpockets(bounding_spheres = pa_s, ref_spheres = bp_bs, **opts))
            logger.info("Subpockets identified: {0}".format(len(all_pockets) - 1))

    if opts.get("output_dir") is not None:
        write_report(all_pockets, **opts)
        write_cfg(**opts)

    return all_pockets


def pocket_wrapper(**opts):
    """ wrapper for pocket that configures the logger, sanitizes inputs, and catches errors; useful when running from the command line or PyMOL but split from the core code for programmatic usage

    """

    opts = configuration.clean_opts(opts)

    if opts.get("output_dir") is not None:
        utilities.check_dir(opts.get("output_dir"))

        log_file = os.path.join(opts.get("output_dir"), "{0}.log".format(opts.get("prefix")))
        utilities.configure_logger(filename=log_file, stream_level=opts.get("logger_stream_level"), file_level=opts.get("logger_file_level"))
    else:
        utilities.configure_logger(stream_level=opts.get("logger_stream_level"))
    logger.debug("Logger configured")

    try:
        all_pockets = pocket(**opts)
    except:
        sys.exit(1)

    return all_pockets


def subpockets(bounding_spheres, ref_spheres, **opts):
    """

    Args:
      bounding_spheres (Spheres): a Spheres object containing both the peptide and solvent exposed face external spheres
      ref_spheres (Spheres): a Spheres object holding the interior spheres that define the pocket to be subdivided
      min_rad (float): radius for original SES calculations (Default value = 1.4)
      max_rad (float): radius originally used to identify the outer, bulk solvent exposed surface (Default value = 3.4)
      min_subpocket_rad (float): minimum radius that identifies distinct subpockets (Default value = 1.7)
      min_subpocket_surf_rad (float): radius used to calculate subpocket surfaces (Default value = 1.0)
      max_subpocket_rad (float): maximum spheres radius used for subpocket clustering (Default value = None)
      sampling (float): radial sampling frequency for clustering (Default value = 0.1)
      inclusion_radius_buffer (float): defines the inclusion distance for nonextraneous spheres in combination with min_rad and max_rad (Default value = 1.0)
      min_cluster_size (int): minimum number of spheres that can constitute a proper clusterw (Default value = 50)
      max_clusters (int): maximum number of clusters (Default value = None)
      prefix (str): identifying string for output (Default value = None)

    Returns:
      pockets ([Spheres]): a list of Spheres objects each of which contains the geometric information describing a distinct subpocket

    """

    nonextraneous_rad = opts.get("min_rad") + opts.get("max_rad") + opts.get("inclusion_radius_buffer")
    nonextraneous_spheres = bounding_spheres.identify_nonextraneous(ref_spheres=ref_spheres, radius=nonextraneous_rad)

    sampling_radii = np.flip(np.arange(opts.get("min_rad"), opts.get("max_subpocket_rad"), opts.get("radial_sampling")), axis=0)
    unmerged_sphere_lists = utilities.sphere_multiprocessing(nonextraneous_spheres, sampling_radii, all_components=True)
    spheres = cluster.merge_sphere_list(itertools.chain(*unmerged_sphere_lists))

    cluster.hierarchically_cluster_spheres(spheres, ordered_radii=sampling_radii, min_new_radius=opts.get("min_subpocket_rad"), min_cluster_size=opts.get("min_cluster_size"), max_clusters=opts.get("max_clusters"))

    cluster.remove_overlap(spheres, radii=sampling_radii, spacing=opts.get("radial_sampling"))
    cluster.remove_overlap(spheres)
    cluster.remove_interior(spheres)
    grouped_list = cluster.extract_groups(spheres, surf_radius=opts.get("min_subpocket_surf_rad"), prefix=opts.get("prefix"))
    return grouped_list


def write_cfg(**opts):
    """ write the processed configuration to file

    Args:
      output_dir (str): output directory, relative or absolute
      prefix (str): identifying prefix for the output files

    """

    utilities.check_dir(opts.get("output_dir"))
    configuration.opts_to_file(opts)


def write_report(all_pockets, **opts):
    """ Write a brief report of calculated volumes to file

    Args:
      all_pockets ([Spheres]): a list of Spheres objects each of which contains the complete information about a distinct pocket or subpocket
      output_dir (str): output directory, relative or absolute
      prefix (str): identifying prefix for output files

    """
    import os
    import pandas as pd

    utilities.check_dir(opts.get("output_dir"))

    rept_list = []

    for pocket in all_pockets:
        spheres_name = os.path.join(opts.get("output_dir"), "{0}.csv".format(pocket.name))
        pocket.write(spheres_name)
        rept_list.append({"name": pocket.name,
                          "volume": pocket.mesh.volume
                          })
    rept_df = pd.DataFrame(rept_list)
    rept_name = os.path.join(opts.get("output_dir"), "{0}_rept.csv".format(opts.get("prefix")))
    rept_df.to_csv(rept_name, index=False)
    logger.info("Report written to: {0}".format(rept_name))

    if len(all_pockets) > 1:
        combined = cluster.merge_sphere_list(all_pockets[1:])
        combined_name = os.path.join(opts.get("output_dir"), "{0}_spa.csv".format(opts.get("prefix")))
        combined.write(combined_name, output_mesh=False)
