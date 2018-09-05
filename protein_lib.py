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
        Writes a fasta file from a list of names and sequences to output file provided

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
    if length == 0:
        return 0
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
    """
        Removes character to_remove from string test_string
        Note: Case sensitive method, 'a' != 'A'
        Returns:
           test_string, minus any instance of to_remove character
    """
    output = ""
    for index in range( len( test_string ) ):
        if test_string[ index ] != to_remove:
            output += test_string[ index ]
    return output


def get_unique_sequences( names_list, sequence_list ):
    sequence_dict = {}
    out_names, out_seqs = list(), list()

    if len( names_list ) > 0:
        for item in range( len( sequence_list ) ):
            sequence_dict[ sequence_list[ item ] ] = names_list[ item ]

        for sequence, name in sequence_dict.items():
            out_names.append( name )
            out_seqs.append( sequence )
        return out_names, out_seqs
    return [  ], sequence_list

def create_list_of_uniques( names, sequences ):
    """
       Removes duplicates from a list
       Params:
          names- names of the sequences
       sequences:
          a list of sequences who may or may not be unique
    """
    return_names = []
    return_sequences = []

    unique_values = set()

    for index in range( len( sequences ) ):
        
        starting_length = len( unique_values )
        unique_values.add( sequences[ index ] )

        if len( unique_values ) > starting_length:
            return_names.append( names[ index ] )
            return_sequences.append( sequences[ index ] )

    return return_names, return_sequences

def create_valid_sequence_list( names_list, sequence_list, min_length, percent_valid ):
   """
       Creates a sequence list of valid sequences.
       A valid sequence is defined by not having any 'X' characters,
       and not violating the parameters of either min_length or percent_valid 
       
       Returns:
           a list of names of those sequences that were valid, with the new bounds appended to the name
           a list of the sequences that were found valid
   """
   valid_names = []
   valid_sequences = []

   for sequence in range( len( sequence_list ) ):
      current_sequence = sequence_list[ sequence ]

      if is_valid_sequence( current_sequence, min_length, percent_valid ):
           current_sequence = remove_char_from_string( current_sequence, '-' )
           valid_sequences.append( current_sequence )
           if names_list:
               valid_names.append( names_list[ sequence ] )

   return valid_names, valid_sequences

def is_valid_sequence( sequence, gap_constraint ):
   """
       Determines whether a given sequence is valid 
       A valid sequence is defined by not having any 'X' characters,
           and not violating the parameters of either min_length or percent_valid 
   """
   if sequence.count( 'X' ) == 0:
       if gap_constraint == None:
           return True
       elif isinstance( gap_constraint, float ):
           return percentage_of_char_in_string( sequence, '-' ) < ( 100 - gap_constraint )
       elif isinstance( gap_constraint, int ):
           return ( sequence.count( '-' ) <= len( sequence.replace( '-', '' ) ) - gap_constraint )
   return False

         
def append_suffix( string, start, end ):
   """
       Appends _start_end to a string
   """
   return "%s_%s_%s" % ( string, str( start ), str( end ) ) 


def subset_lists_iter( name, sequence, window_size, step_size, span_gaps, gap_constraints = None):
    new_names = []
    new_seqs = []

    start = 0
    end = window_size
    index = 0

    while end < len( sequence ):
       xmer = grab_xmer_from_seq( sequence, start, window_size, span_gaps )

       if len( xmer ) == window_size and is_valid_sequence( xmer, gap_constraints ):

           xmer_no_gaps = xmer.replace( '-', '' )
           if xmer_no_gaps:
               new_seqs.append( xmer.replace( '-', '' ) )
               new_names.append( append_suffix( name, start + 1, end ) )

       start += step_size
       end = start + window_size 

    return new_names, new_seqs

def grab_xmer_from_seq( sequence, start, window_size, span_gaps ):
   out_xmer = ""
   xmer_len = 0
   probe_index = start

   while xmer_len < window_size and probe_index < len( sequence ):

        probe_char = sequence[ probe_index ]
        skipped = False

        if span_gaps:
            while probe_char == '-' and probe_index < len( sequence ):
                probe_char = sequence[ probe_index ]
                probe_index += 1
                skipped = True

        if probe_index < len( sequence ):
            out_xmer += probe_char
            xmer_len += 1
            if not skipped:
                probe_index += 1


   return out_xmer

def get_kmers_from_seqs(            
                        names,
                        sequences,
                        window_size,
                        step_size,
                        span_gaps,
                        gap_constraint = None
    ):

   total_kmers = 0

   subset_names = list()
   subset_seqs = list()

   for index in range( len( sequences ) ):

      current_sequence = sequences[ index ]

      if len( names ) > 0:
          current_name = names[ index ]
      else:
          current_name = ""

      win_names, current_kmers = subset_lists_iter( current_name, current_sequence,
                                                    window_size, step_size,
                                                    span_gaps
                                                  )
      
      total_kmers += len( set( current_kmers ) )

      for each in set( current_kmers ):
         subset_seqs.append( each )
         subset_names.append( win_names[ current_kmers.index( each ) ] + "_" + str( index ) + "_" + str( index + window_size )   )


   subset_names, subset_seqs = get_unique_sequences( subset_names, subset_seqs )

   return subset_names, subset_seqs, total_kmers


def subset_lists( name, sequence, window_size, step_size ):
   """
       Creates a list of subsets of windowSize size in intervals of stepSize
       Note: Uses recursive subset_lists_helper for operations
   
       Params:
            name: String name of sequence to be split up
            sequence: String sequence to be split up into a list
       Returns:
            a list of the split up names, with a suffix applied, and a list of the segments 
            of the list, as specified
   """
   new_names = []
   new_seqs = []
   return subset_lists_helper( name, sequence, new_names, new_seqs, window_size, step_size, 0, window_size )

def subset_lists_helper( name, sequence, name_arr, seq_arr, window_size, step_size, start, end ):
    """
        Recursive helper method called by subset_lists
    """
    if start + window_size < len( sequence ):
       if len( sequence[ start: end ] ) == 1:
           return
       seq_arr.append( sequence[ start : end ] ) 
       name_arr.append( append_suffix( name, start + 1, end ) )

       subset_lists_helper( name, sequence, name_arr, seq_arr, window_size, step_size, start + step_size, start + step_size + window_size )
    return name_arr, seq_arr
   


            
    
