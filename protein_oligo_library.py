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
    in_sequence = False 
    sequence = ''

    for current_line in in_file.readlines():

        current_line = current_line.strip()
        if current_line[ 0 ] == '>':
            # Add the sequence that was built to the list
            sequences.append( sequence )

            current_line = current_line.split( '>' )
            names.append( current_line[ 1 ] )
            in_sequence = True

        else:
            if in_sequence:
                sequence += current_line
            else:
                in_sequence = False
                sequence = ''

    in_file.close()
    return names[ 0: ], sequences

def write_fastas( names_list, sequence_list, output_name="out.txt" ):
    out_file = open( output_name, 'w+' )
    for index in range( len( names_list ) ):
        out_file.write( '>' + names_list[ index ] + '\n' + 
                        sequence_list[ index ] + '\n'
                      )
    out_file.close()
        

def char_in_string( test_string, character ):
    for index in range( len( test_string ) ):
        if test_string[ index ] == character:
            return True
    return False

def percentage_of_char_in_string( test_string, character ):
    """
        Calculates what percent of a given test_string is given character
    
        Params:
           test_string- string to test for character
           character- character to test for in string
       Returns:
           floating point value percent of the string that
           is character
    """
    length = len( test_string )
    char_count = 0.0

    for index in range( length ):
        if test_string[ index ] == character:
            char_count += 1
    return char_count / length

def count_char_in_string( test_string, character ):
    """
        Counts how much of a certain character are in test_string

        Params:
            test_string- string to count
            character- character to count in string
        Returns:
            integer value representing the number of character 
                were found in test_string
    """
    length = len( test_string )
    count = 0

    for index in range( length ):
        if test_string[ index ] == character:
            count += 1
    return count

def min_concurrent_chars( test_string, delimeter_char ):
    """
        Finds the minimum number of concurrent non-delimiter char in 
        test_string
    
        Params:
          test_string- string to search
          delimeter_char- character to reset the count
        Returns:
          integer value, the smallest amount of concurrent characters
               between delimeter character
    """

    split_string = test_string.split( delimeter_char )
    min_length = len( split_string[ 0 ] )

    for substring in split_string[ 1: ]:
        current_length = len( substring )
        if current_length > 0 and current_length < min_length:
            min_length = current_length

    return min_length


        

