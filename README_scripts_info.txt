Description of programmes for analysis:

#####################################################################################################################################################

#The pipeline requires an input file with sample parameters described below:

1. Sample description file [Sample_file.txt]

S21_M   S21_M   Lane_1  IGH     /lustre/scratch115/teams/anderson/users/vp5/Cram_files/20075_1#3.cram   OVERLAPPING     UNPAIRED        /lustre/scratch115/teams/anderson/users/IsoTyper_FLU/   Multiplex       HOMO_SAPIENS    LIBRARY/Primers_HOMO_SAPIENS_IG_RBR_Constant_region_MPLX.txt
Where Sample_file.txt must be in the following format: 

Column 1: Sample ID                 (to be used as an identifier for all files in analysis)
Column 2: Sample name/patient/etc   (for owner identification)
Column 3: Sample group              (for batch identification)
Column 4: Gene amplified            (e.g. IGH, IGK, IGL)  
Column 5: Input file                (location of raw BAM file)
Column 6: Initial read pairing      (e.g. OVERLAPPING (if reads to be joined together))
Column 7: Final read pairing        (e.g. UNPAIRED (if single sequence per BCR) or PAIRED (if two reads with gap between per BCR))
Column 8: Output directory          (for output files)      
Column 9: Library preparation       (e.g. Multiplex, 5RACE)
Column 10:Species                  (e.g. HOMO_SAPIENS, etc: must ensure that the reference files for species of interest are in the 
                                    LIBRARY/ directory or will cause error)
Column 11: Primer file              (e.g. LIBRARY/FR1_primers.txt for human 
                                    Note: a) The letter "J" must be present in the title of the reverse sequences, and not in the forward sequences.
                                          b) The primers must be orientated in the direction that can be found in the the sequences 
                                              (reverse primer with reverse complement).
                                          c) Barcoded regions must be designated by "N"s. If an "N" is present in the primer sequence, 
                                              the reads will be filtered to accept only a single read per barcode. Reads will be 
                                              removed if there are multiple different BCRs per barcode.

If the symbol "#" is at the beginning of any line, then the line will not be read by analysis programmes (i.e. if you want to only 
analyse a subset of samples in your file).

#####################################################################################################################################################
2. Processing_sequences_large_scale.py

Usage: 
python Processing_sequences_large_scale.py [sample file list] [commands (comma separated list)] [bsub command: Y/N] [print commands: Y/N] [run commands: Y/N]

This will run all the analysis programs in BIN as indicated in the script over the samples in Sample_file.txt. This script is written for submission to the Sanger Institute cloud system and thus the usage has an option for bsub command to specific queue in the local cluster. 

Command options for program: 
  1: BIN/Read_processing_and_quality_2.8.py             (this performs initial BAM->fastq analysis)                                                     
  2: BIN/Read_processing_and_quality_2.8.py 		(this performs read filtering based on UMIs, read joining, IGHV-J gene primer matching, ORF identification)                            
  3: BIN/Read_processing_and_quality_2.8.py 		(this performs sequence clustering based on 1 nt difference between each BCR, and calculates network statistics and cluster properties) 
  4: BIN/Generate_repertoire_statistics_2.1.py          (this performs gene annotation of each BCR and calculation of IGHV-J gene frequencies, isotype frequencies and diversity of isotype-specific populations based on network analysis)
  5: BIN/Get_figure_params.py          			(this collects parameters for network figures and generates a sample-specific R script used in command 6 to generate a network figure) 
  6: BIN/Network_generation_coloured_"+desc+"_"+id+".R  (this runs a R script to produce a network of BCR sequences based on sequence relatedness and the clustering produced in command 3)
  




