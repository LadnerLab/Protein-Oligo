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

    for current_line in file_to_read.readlines():

        current_line = current_line.strip()
        if current_line[ 0 ] == '>':
            current_line = current_line.split( '>' )
            names.append( current_line[ 1 ] )

        else:
            sequences.append( current_line )

    return names[ 0: ], sequences



def remove_char_from_string( string, search_char, start, end ):
    """
        Removes specified character from string
        Params:
          string - the string from which to remove the character
          search_char - the character to remove from the string
          start - the beginning index of the string to search
          end - the last index of the string to search
        Returns:
          string without the specified character
    """
    output_string = ""

    for current_char in range( start, end ):
        print( start )
        print( end )
        if string[ current_char ] != search_char:
            output_string += str( string[ current_char ] )
            
    return output_string
