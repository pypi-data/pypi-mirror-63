.. image:: /ONT_logo.png
  :width: 800

******************

Megalodon
"""""""""

Megalodon is a research command line tool to extract high accuracy modified base and sequence variant calls from raw nanopore reads by anchoring the information rich basecalling neural network output to a reference genome/transriptome.

Raw nanopore reads are processed by a single command to produce basecalls (FASTA/Q), reference mappings (SAM/BAM/CRAM), sequence variant calls (per-read and VCF) and modified base calls (per-read and bedgraph/bedmethyl/modVCF).

Detailed documentation for all ``megalodon`` arguments and algorithms can be found on the `megalodon documentation page <https://nanoporetech.github.io/megalodon/>`_.

Prerequisites
-------------

As of version 2.0, the primary megalodon run mode requires the guppy basecaller.
See the `community page for download/installation instructions <https://community.nanoporetech.com/downloads>`_.

All other requirements are handled by ``pip`` or ``conda`` installation.
If installing from source, ``numpy`` must be installed before running installation for cython optimizations.

.. note::

   `Taiyaki <https://github.com/nanoporetech/taiyaki>`_ is no longer required to run megalodon, but installation is required for two specific run modes:
   1) output mapped signal files (for basecall models training)
   2) runing the taiyaki basecalling backend (for neural network designs including experimental layers)

Installation
------------

Megalodon is a command line tool.
``pip`` and ``conda`` are the recommended installation interfaces for megalodon.

::

   pip install megalodon
   # or
   conda install megalodon

Getting Started
---------------

Megalodon is accessed via the command line interface ``megalodon`` command.
The path to the ``guppy_basecall_server`` executable is required to run megalodon.
By default, megalodon assumes this path is ``./ont-guppy/bin/guppy_basecall_server``.
Use the ``--guppy-server-path`` argument to specify a different path.

::

    # megalodon help (common args)
    megalodon -h
    # megalodon help (all args)
    megalodon --help-long

    # Example command to output basecalls, mappings, variants and CpG methylation
    #   Compute settings: GPU devices 0 and 1 with 40 CPU cores
    megalodon raw_fast5s/ \
        --outputs basecalls mappings variants mods \
        --reference reference.fa --variant-filename variants.vcf.gz \
        --mod-motif Z CG 0 --devices 0 1 --processes 40 \
        --verbose-read-progress 3

This command produces the ``megalodon_results`` output directory containing all requested output files and logs.
The format for each output is described briefly below and in more detail in the `full documentation <https://nanoporetech.github.io/megalodon/>`_

Inputs
------

- Raw reads

  - Directory containing raw read FAST5 files
  - By default, the directory will be searched recursively for read files (ending in ``.fast5``)
- Reference

  - Genome or transcriptome sequence reference (FASTA or minimap2 index)
- Variants File

  - Format: VCF or BCF
  - Megalodon requires a set of candidate variants for ``--outputs variants`` (provide via ``--variant-filename`` argument).
  - Only small indels (default less than ``50`` bases) are tested by default.

Outputs
-------

All megalodon outputs are written into the directory specified with the ``--output-directory`` option with standard file names and extensions.

- Basecalls

  - Format: FASTQ (default) or FASTA
  - Basecall-anchored modified base scores are also available in HDF5 format (``--outputs mod_basecalls``).
- Mappings

  - Format: SAM, BAM (default), or CRAM
  - A tab-separated mapping text summary is also produced including per-read alignment statistics.
- Modified Base Calls

  - Per-read modified base calls

    - Per-read SQL DB containing modified base scores at each covered reference location
    - Tab-delimited output can be produced by adding the ``--write-mods-text`` flag or produced post-run using the ``megalodon/scripts/write_per_read_modified_base_text.py`` script.

      - This output can drastically slow processing, especially on slower disk or when outputting modified bases at all contexts.
  - Aggregated calls

    - Format: bedgraph, bedmethyl (default), and/or modVCF
  - In order to restrict modified base calls to a specific motif(s) specify the ``--mod-motif`` argument. For example, to restrict calls to CpG sites specify ``--mod-motif Z CG 0``.
- Sequence Variant Calls

  - Per-read Variant Calls

    - SQL DB containing per-read variant scores for each covered variant
    - Tab-delimited output can be produced by adding the ``--write-variants-text`` flag or produced post-run using the ``megalodon/scripts/write_per_read_sequence_variant_text.py`` script.
  - Aggregated calls

    - Format: VCF
    - Default run mode is diploid. To run in haploid mode, set ``--haploid`` flag.
    - For best results on a diploid genome see the variant phasing workflow on the `full documentation page <https://nanoporetech.github.io/megalodon/variant_phasing.html>`_.

Guppy Models and Parameters
---------------------------

By default, megalodon uses the ``dna_r9.4.1_450bps_modbases_dam-dcm-cpg_hac.cfg`` guppy config.
This config is compatible with DNA, R9.4.1, MinION/GridION reads and allows output of 5mC and 6mA calls in biological contexts (CpG, dcm and dam sites).
Use the ``--guppy-config`` option to specify a different guppy model config.

All configs can be used to output basecalls and mappings (as well as signal mapping files for basecall training; see ``--output-signal-mappings`` in ``--help-long``).
Modified base and sequence variant outputs require megalodon calibration files.
To list configs with default calibration files, run ``megalodon --list-supported-guppy-configs``.

Only flip-flop configs/models are currently supported by megalodon (this excludes k-mer based and RLE model types).

In addition to the ``--guppy-config`` and ``--guppy-server-path`` options, a number of additional arguments control the behavior of the guppy backend.
An alternative server port can be specified with the ``--guppy-server-port`` argument (useful when multiple megalodon/guppy_server are active on the same machine).
The ``--guppy-params`` argument will pass arguments directly to the ``guppy_basecall_server`` initialization call.
These arguments must be valid arguments for the provided guppy server executable.
For example to optimize GPU usage for an nvidia V100 GPU, the following option might be specified: ``--guppy-parmas "--num_callers 5 --ipc_threads 6"``

Finally the ``--guppy-timeout`` arguments ensures that a run will not stall on a small number of reads taking a very long time (default 5 seconds).

High Quality Phased Variant Calls
---------------------------------

In order to obtain the highest quality diploid sequence variant calls the full variant phasing pipeline employing whatshap should be applied.
This pipeline is described in detail on the `full documentation page <https://nanoporetech.github.io/megalodon/variant_phasing.html>`_.
The default diploid variant settings are optimized for the full phasing pipeline and not the highest quality diploid calls directly from a single megalodon call.

High-Density Variants
*********************

When running megalodon with a high density of variants (more than 1 variant per 100 reference bases), certain steps can be taken to increase performace.
In particular, megalodon requires variants to be atomized first.
In order to improve performance, this step can be carried out as a pre-processing step.

To perform this pre-processing use the ``megalodon/scripts/atomize_variants.py`` command.
This will produce an atomized variants file.
When running megalodon with this variants file the ``--variants-are-atomized`` flag should be set.

Disk Performance Considerations
*******************************

Per-read modified base and variant statistics are stored in an on-disk sqlite database.
As of version 2.0, the status of output queues is displayed by default.
If any of these status bars indicate a full queue, megalodon will stall waiting on that process to write data to disk.
Moving the  ``--output-directory`` to a location with faster disk I/O performance should imporove performance.

For the aggregation stage of processing the disk read speed has a magnified effect.
During aggregation binary searches for results grouped per-site must be performed over the on-disk database.
While database optimization to reduce the disk reads has been implemented, the performance for data extraction can be extremely slow for large runs.
Moving the database location from a remote or network file system to a local fast (SSD) disk can increase compute efficiency as much as 100X-1000X.

RNA
---

Megalodon provides experimental support for direct RNA processing.
This support can be accessed within the ``rna`` github branch (access via ``git clone --branch rna https://github.com/nanoporetech/megalodon``).

Licence and Copyright
---------------------

|copy| 2019-20 Oxford Nanopore Technologies Ltd.

.. |copy| unicode:: 0xA9 .. copyright sign

Megalodon is distributed under the terms of the Oxford Nanopore
Technologies, Ltd.  Public License, v. 1.0.  If a copy of the License
was not distributed with this file, You can obtain one at
http://nanoporetech.com
