#!/usr/bin/env python3
   
def read_fasta_lists( file_to_read ):
    """
       Reads a list of fastas from file_to_read
    
       Returns:
        names- a list of names of the sequences found in the fasta file
        sequences- a list of the sequences found in the fasta file
    """


    file_in = open( file_to_read, 'r' )
    count = 0

    names = []
    sequences = []
    current_sequence = ''

    for line in file_in:
        line = line.strip()
        if line and line[ 0 ] == '>':
            count += 1
            names.append( line[ 1: ] )
            if count > 1:
                sequences.append( current_sequence )
            current_sequence = ''

        else:
            current_sequence += line

    sequences.append( current_sequence )
    file_in.close()

    return names, sequences
 
def write_fastas( names_list, sequence_list, output_name="out.txt" ):
    """
        Writes a fast file from a list of names an dsequences to output file provided

    """
    out_file = open( output_name, 'w+' )
    for index in range( len( names_list ) ):
        out_file.write( '>' + names_list[ index ] + '\n' + 
                        sequence_list[ index ] + '\n'
                      )
    out_file.close()
        

def char_in_string( test_string, character ):
    """
        Checks if a character is found within a given string
    """
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
    return ( char_count / length ) * 100

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


def remove_char_from_string( test_string, to_remove ):
    output = ""
    for index in range( len( test_string ) ):
        if test_string[ index ] != to_remove:
            output += test_string[ index ]
    return output
