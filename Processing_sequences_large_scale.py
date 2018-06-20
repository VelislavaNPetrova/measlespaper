#!/usr/bin/python
#import math
import sys
#from collections import defaultdict
import os
import commands

def Get_info(file):
  (id,  sample,  info,  gene,  directory,pair,pair_final,dir, platform,spec,primer,other)=([],[],[],[],[],[],[],[],[],[],[],[])
  fh=open(file,"r")
  for l in fh:
    if(l[0]!="#"):
      l=l.strip().split()
      id.append(l[0])
      sample.append(l[1])
      info.append(l[2])
      gene.append(l[3])
      directory.append(l[4])
      pair.append(l[5])
      pair_final.append(l[6])
      dir.append(l[7])
      platform.append(l[8])
      spec.append(l[9])
      if(len(l)>=11):primer.append(l[10])
      else:primer.append("LIBRARY/FR1_primers.txt")
      if(len(l)>=12):
        lis = []
        for i in range(11,len(l)):
          lis.append(l[i])
        other.append(",".join(lis))
      else:other.append('')
  fh.close()
  return(id,  sample,  info,  gene,  directory, pair,pair_final,dir, platform,spec,primer,other)

args=sys.argv
#select memory limit
#mem = '-R"select[mem>1800] rusage[mem=1800]" -M1800 '
mem = '-R"select[mem>3800] rusage[mem=3800]" -M3800 '
#mem = '-R"select[mem>5800] rusage[mem=5800]" -M5800 '
#mem = '-R"select[mem>13800] rusage[mem=13800]" -M13800 '
#mem = ''
#2.select a queue to run the jobs on
queue = '-q yesterday'
#queue= "-q normal"
#queue = "-q parallel"
#queue= "-q long"
#queue ="-q small"
#queue = "-q test"
command = 'bsub -G team152 '+queue+' python Processing_sequences.prog '
span = '-n3 -R"span[hosts=1]"'
span=''

if (len(args)<5):
  queue = '-q normal'
  command = 'python Processing_sequences_large_scale.py [sample file list] [commands (comma separated list)] [bsub command: Y/N] [print commands: Y/N] [run commands: Y/N]'
  print "SEQUENCE ANALYSIS PIPELINE: Creates networks from MiSeq data"
  print "USAGE:"
  print command,"\n"
  os.system("cat Command_outline.txt")
  print "\n"
else:
  file = args[1]
  command = args[2]
  bsub_command = args[3]
  print_command = args[4]
  run_command = args[5]
  command=command.split(",")
  if(bsub_command not in ["Y","N"]):print 'python Processing_sequences.py [sample file list] [commands (comma separated list)] [bsub command: Y/N] [print commands: Y/N] [run commands: Y/N]\n\tError: bsub command must be: Y or N'
  if(bsub_command not in ["Y","N"]):print 'python Processing_sequences.py [sample file list] [commands (comma separated list)] [bsub command: Y/N] [print commands: Y/N] [run commands: Y/N] \n\tError: print command must be: Y or N'
  if(bsub_command not in ["Y","N"]):print 'python Processing_sequences.py [sample file list] [commands (comma separated list)] [bsub command: Y/N] [print commands: Y/N] [run commands: Y/N] \n\tError: run command must be: Y or N'
  (ids,  samples,  infos,  gene,  source,pairs,pairs_final,dirs, platform,spec,primer,others)=Get_info(file)
  idss,dirss='',''
  commands = []
  for i in range(0,len(samples)):
    info,sample, gene_types, pair,pair_final, dir,platforms, primers,other=infos[i], samples[i], gene[i], pairs[i],pairs_final[i], dirs[i], platform[i], primer[i],others[i]
    bsub = ''
    if( "3" in command):span = '-n3 -R"span[hosts=1]"'
    else:span=''
    id,sources,species=ids[i],source[i],spec[i]
    if(bsub_command=="Y"):bsub = "bsub -G team152 "+queue+" -o out_SPLITTING_"+id+" "+mem+" "+span+" "
    #if(bsub_command=="Y"):bsub = "bsub -P team146 "+queue+" -o out_SPLITTING_"+id+" "+mem+" "+span+" "
    #if(bsub_command=="Y"):bsub = "bsub -P team146 "+queue+" -o out_STANDARD_"+id+" "+mem+" "+span+" "
    if(dir=="/lustre/scratch115/teams/anderson/users/vp5/IsoTyper_Measles/"):dir="/lustre/scratch115/teams/anderson/users/vp5/IsoTyper_Measles/" # sorry, directory location change for one group of samples
    if( "1" in command):
      command1 = "python BIN/Read_processing_and_quality_2.8.py "+dir+" "+id+" "+sample+" "+gene_types+" "+pair+" "+species+" "+sources +" "+str(200)+" "+primers+" "+platforms+" 1 "+other
      commands.append(bsub+command1)
    if( "123" in command):
      command1 = "python BIN/Read_processing_and_quality_2.8.py "+dir+" "+id+" "+sample+" "+gene_types+" "+pair+" "+species+" "+sources +" "+str(200)+" "+primers+" "+platforms+" 2,3 "+other
      commands.append(bsub+command1)
    if( "2" in command):
      command1 = "python BIN/Read_processing_and_quality_2.8.py "+dir+" "+id+" "+sample+" "+gene_types+" "+pair+" "+species+" "+sources +" "+str(200)+" "+primers+" "+platforms+" 2 "+other
      commands.append(bsub+command1)
    if( "3" in command):
      command1 = "python BIN/Read_processing_and_quality_2.8.py "+dir+" "+id+" "+sample+" "+gene_types+" "+pair+" "+species+" "+sources +" "+str(200)+" "+primers+" "+platforms+" 3 "+other
      commands.append(bsub+command1)
    if( "4" in command):
      command2 = "python BIN/Generate_repertoire_statistics_2.1.py "+dir+"ORIENTATED_SEQUENCES/ANNOTATIONS/ "+id+" "+dir+"ORIENTATED_SEQUENCES/NETWORKS/Fully_reduced_"+id+".fasta "+dir+"ORIENTATED_SEQUENCES/Filtered_ORFs_sequences_all_"+id+".fasta "+gene_types+" "+species+" "+dir+"ORIENTATED_SEQUENCES/NETWORKS/Cluster_identities_"+id+".txt ANNOTATE,STATISTICS"
      commands.append(bsub+command2)
    if("ISO1" in command):
      command1 = "python BIN/IsoTyper_1.0.py "+id+" "+id+" "+dir+" "+species+" "
      commands.append(bsub+command1)
    if("5" in command): ## Generate separate network plots
      desc = file.replace("Samples_","").replace(".txt","")
      command10 = "python BIN/Get_figure_params.py "+dir+"ORIENTATED_SEQUENCES/ "+desc+"_"+id+" "+id
      commands.append(bsub+command10)
    if("6" in command): ## Generate separate network plots
      desc = file.replace("Samples_","").replace(".txt","")
      command11 = "/software/bin/R-dev CMD BATCH "+dir+"ORIENTATED_SEQUENCES/Network_generation_"+desc+"_"+id+".R"
      commands.append(bsub+command11)
    if("6.5" in command): ## Generate separate coloured network plots
      desc = file.replace("Samples_","").replace(".txt","")
      command11 = "/software/bin/R-dev CMD BATCH "+dir+"ORIENTATED_SEQUENCES/Network_generation_coloured_"+desc+"_"+id+".R"
      commands.append(bsub+command11)
  idss,dirss = idss[1:len(idss)],dirss[1:len(dirss)]
  desc = file.replace("Samples_","").replace(".txt","")
  if("10" in command):
    command10 = "python BIN/Get_figure_params.py "+dirss+" "+desc+" "+idss
    commands.append(bsub+command10)
  if("10.5" in command):
    command10 = "python BIN/Get_coloured_figures.py "+dirss+" "+desc+" "+idss
    commands.append(bsub+command10)
  if("11" in command):
    command11 = "/software/bin/R-dev CMD BATCH "+dirs[0]+"ORIENTATED_SEQUENCES/Network_generation_"+desc+".R"
    commands.append(bsub+command11)
  for comm in commands:
    if(print_command=="Y"):print comm, "\n"
    if(run_command=="Y"): os.system(comm)


