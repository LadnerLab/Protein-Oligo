#!/usr/bin/env python3

def main():
    in_file = open( "lassa_seq_example.fasta" , 'r' )
    names, sequences = read_fasta_lists( in_file )
    print( names )
    print( sequences )
    
def read_fasta_lists( file_to_read ):
    """
       Reads a list of fastas from file_to_read
    
       Returns:
        names- a list of names of the sequences found in the fasta file
        sequences- a list of the sequences found in the fasta file
    """

    names = []
    sequences = []

    for current_line in file_to_read.readlines():

        current_line = current_line.strip()
        if current_line[ 0 ] == '>':
            current_line = current_line.split( '>' )
            names.append( current_line[ 1 ] )

        else:
            sequences.append( current_line )

    return names[ 0: ], sequences




if __name__ == '__main__':
    main()

    
