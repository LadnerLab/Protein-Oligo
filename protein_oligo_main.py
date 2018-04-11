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


def add_program_options( option_parser ):
    option_parser.add_option( '-a', '--alignment', help = "Fasta query file of sequence alignment to be used by program. [None, Required]"
                            )

    option_parser.add_option( '-w', '--windowSize', type = 'int', \
                                       default = 100, \
                                       help = "Amount of characters from each alignment sequence to look at. [100]"
                                     )
    option_parser.add_option( '-s', '--stepSize', type = 'int', \
                             default = 100, \
                             help = "Amount of space to move over after each alignment of sequences. [100]"
                            )


if __name__ == '__main__':
    main()




