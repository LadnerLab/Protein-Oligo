#!/usr/bin/env python3
   
def read_fasta_lists( file_to_read ):
    """
       Reads a list of fastas from file_to_read
    
       Returns:
        names- a list of names of the sequences found in the fasta file
        sequences- a list of the sequences found in the fasta file
    """

    names = []
    sequences = []

    in_file = open( file_to_read, 'r' )

    for current_line in in_file.readlines():

        current_line = current_line.strip()
        if current_line[ 0 ] == '>':
            current_line = current_line.split( '>' )
            names.append( current_line[ 1 ] )

        else:
            sequences.append( current_line )

    in_file.close()
    return names[ 0: ], sequences

def write_fastas( names_list, sequence_list, output_name="out.txt" ):
    out_file = open( output_name, 'w+' )
    for index in range( len( names_list ) ):
        out_file.write( '>' + names_list[ index ] + '\n' + 
                        sequence_list[ index ] + '\n'
                      )
    out_file.close()
        

