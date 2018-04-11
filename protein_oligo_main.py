#!/usr/bin/env python3
import protein_oligo_library as oligo

if __name__ == '__main__':
    in_file = open( "lassa_seq_example.fasta" , 'r' )
    names, sequences = oligo.read_fasta_lists( in_file )
    print( names )
    print( sequences )
 
