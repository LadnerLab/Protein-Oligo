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
   oligo.write_fastas( names, sequences, options.outPut )  



def add_program_options( option_parser ):
    option_parser.add_option( '-a', '--alignment', help = "Fasta query file of sequence alignment to be used by program. [None, Required]"
                            )

    option_parser.add_option( '-w', '--windowSize', type = 'int', \
                                       default = 100, \
                                       help = "Amount of characters from each alignment sequence to look at. [100]"
                                     )
    option_parser.add_option( '-o', '--outPut', default = "oligo_out.txt", help = "Name of file program output will be written to. [oligo_out.txt]"
                            )


if __name__ == '__main__':
    main()


def create_subset_sequence_list( names_list, sequence_list, window_size, delimeter_chars ):
   subset_names_list = []
   subset_sequences_list = []

   for current_sequence in range( len( subset_sequences_list ) ):
      if not subset_sequences_list[ current_sequence ].find( delimeter_chars, 0, window_size ):
         subset_names_list.append( names_list[ current_sequence ]
         subset_sequences_list.append( sequence_list[ current_sequence ]
         

