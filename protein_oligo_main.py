#!/usr/bin/env python3

import protein_oligo_library as oligo
import sys
import optparse

def main():
   usage = "usage: %prog [options]"
   option_parser = optparse.OptionParser( usage )

   add_program_options( option_parser )

   options, arguments = option_parser.parse_args()

   # Make sure that a file was provided to script
   if options.alignment is None:
      print( "Fasta alignment file must be provided, exiting." )
      sys.exit( 1 )

   names, sequences = oligo.read_fasta_lists( options.alignment )

 
   names, sequences = create_subset_sequence_list( names, sequences, options ) 
   oligo.write_fastas( names, sequences, output_name = options.outPut )





def add_program_options( option_parser ):
   option_parser.add_option( '-a', '--alignment', help = "Fasta query file of sequence alignment to be used by program. [None, Required]"
   )

   option_parser.add_option( '-w', '--windowSize', type = 'int', \
                             default = 100, \
                             help = "Amount of characters from each alignment sequence to look at. [100]"
   )
   option_parser.add_option( '-o', '--outPut', default = "oligo_out.txt", help = "Name of file program output will be written to. [oligo_out.txt]"
   )
   option_parser.add_option( '-p', '--percentValid', type = 'float', default = 90.0, help = (
      "Percent of non '-' characters present in order for the sequence to be considered valid, "  
      "sequences with less than specified amount will not be present in program out put. [90.00] "
   )
   )
   option_parser.add_option( '-l', '--minLength', type = 'int', help = (
      "Minimum length of concurrent non-dash characters that must be present in order for "
      "the sequence to be considered valid, sequences with a maximum length of concurrent non-dash "
      "characters less than this parameter will not be included in program output. [None, Required] "
   )
   )
    
def create_subset_sequence_list( names_list, sequence_list, options ):
   """
       Creates a sequence list of valid sequences.
       A valid sequence is defined by not having any 'X' characters,
       and not violating the parameters of either options.outPut or options.percentValid
       
       Returns:
           a list of names of those sequences that were valid, with the new bounds appended to the name
           a list of the sequences that were found valid
   """
   valid_names = []
   valid_sequences = []

   for sequence in range( len( sequence_list ) ):
      current_sequence = sequence_list[ sequence ][ 0: options.windowSize ]
      current_sequence = oligo.remove_char_from_string( current_sequence, '-' )

      if is_valid_sequence( current_sequence, options ):
           valid_names.append( names_list[ sequence ] )
           valid_sequences.append( current_sequence[ 0: options.windowSize ] )

   names_list = append_suffix( valid_names, options.windowSize )

   return names_list, valid_sequences

def is_valid_sequence( sequence, options ):
   """
       Determines whether a given sequence is valid 
       A valid sequence is defined by not having any 'X' characters,
           and not violating the parameters of either options.outPut or options.percentValid
   """
   if not oligo.char_in_string( sequence, 'X' ):
       if options.minLength is None:
           return oligo.percentage_of_char_in_string( sequence, '-' ) < options.percentValid
       else:
           return ( oligo.min_concurrent_chars( sequence, '-' ) >= options.minLength )
   return False

         
def append_suffix( string_list, max_length ):
   """
       Appends "_0_length of string to each string in a list provided
   """
   new_list = []
   for current_string in string_list:
      new_list.append( current_string + "_0_" + str( max_length ) )
   return new_list

if __name__ == '__main__':
           main()


