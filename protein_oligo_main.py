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


   for index in range( len( sequences ) ):
      current_sequence = oligo.subset_lists_iter( names[ index ], sequences[ index ], options.windowSize, options.stepSize ) 
      names, sequences = oligo.create_list_of_uniques( names, sequences )


      names, sequences = oligo.create_valid_sequence_list( names, sequences, options.minLength, options.percentValid, 0, options.windowSize ) 
   print( len( names ) )
   print( len( sequences ) )
   # oligo.write_fastas( names, sequences, output_name = options.outPut )



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

   option_parser.add_option( '-s', '--stepSize', type = 'int', help = (
      "Step size to move over after each subset of windowSize characters has been read"
      )
      )
    
  

if __name__ == '__main__':
           main()


