#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep  5 13:13:39 2022

@author: ekateria
"""

from Bio import SeqIO
from Bio.SeqRecord import SeqRecord
from Bio.Seq import Seq
import os
import pandas as pd
import numpy as np

workdir='/cluster/projects/nn9383k/arfa/mockcommunity/MC_genomes'
folders=[x[0] for x in os.walk(workdir)]

for f in folders[1::]:
    files=os.listdir(f)
    newdir=f.replace('refseq','concatenated')
    os.mkdir(newdir)
    for fi in files[1:]:
        qfasta=SeqIO.parse('/'.join([f, fi]),'fasta')
        concat=str('')      
        for fasta in qfasta:
            concat=''.join([concat,str(fasta.seq)])
        record = SeqRecord(Seq(concat, name=fi.replace('.fna',''),
                           id=fi.replace('.fna',''), description=''))
        SeqIO.write(record,'/'.join([newdir,fi]),'fasta')

##Concatenate all files into 'fungi.fna' using cat *.fna > fungi.fna
## in terminal

       
## Find lengths of each genome
workdir='/cluster/projects/nn9383k/arfa/mockcommunity/MC_genomes'
summary=pd.read_csv('/'.join([workdir, 'Fungal_MC_GCF.txt']), sep='\t')
fdir='/'.join([workdir, 'concatenated/all'])
files=os.listdir(fdir)
for fi in files[1:]:
    qfasta=SeqIO.parse('/'.join([fdir,fi]),'fasta')
    for fasta in qfasta:
        x='_'.join(fasta.name.split('_')[:2])
        summary.loc[summary['RefSeqID']==x,'Length, bp']=len(fasta)

summary.to_csv('/'.join([workdir, 'Fungal_MC_GCF.txt']),index=False)


##Read the simulated dataset (check 100000 reads per sequence)
workdir='/cluster/projects/nn9383k/arfa/mockcommunity/MC_genomes'
qfastq=SeqIO.parse('/'.join([workdir,'MC_100000_1.fq']),'fastq')
fastq_sum=pd.DataFrame(columns=['ReadName','AvgQual'])
for seq in qfastq:
    fastq_sum = pd.concat([fastq_sum, pd.DataFrame([['_'.join(seq.name.split('_')[:2]),
                                                     np.mean(seq.letter_annotations['phred_quality'])]],
                                                   columns=['ReadName', 'AvgQual'])], ignore_index=True)

#Check how many reads per genome there are
reads_per_seq=fastq_sum['ReadName'].value_counts()

#Check the average quality of the reads per each genome
qual_per_genome=pd.DataFrame(fastq_sum.groupby('ReadName')['AvgQual'].mean(), columns=['AvgQual'])
qual_per_genome=qual_per_genome.reset_index()
qual_per_genome=qual_per_genome.rename(columns={'ReadName':'RefSeqID'})
summary=summary.merge(qual_per_genome, on='RefSeqID', how='left')
summary=summary.drop(columns='AvgQual_x')
summary=summary.rename(columns={'AvgQual_y':'AvgQual'})
summary['NumReads']=100000
summary.to_csv('/'.join([workdir, 'Fungal_MC_GCF.txt']),index=False, sep ='\t')
