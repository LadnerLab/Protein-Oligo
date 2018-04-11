#!/usr/bin/env python3
import protein_oligo_library as oligo
import optparse

def main():
   usage = "usage: %prog [options]"
   option_parser = optparse.OptionParser( usage )

   add_program_options( option_parser )

   options, arguments = option_parser.parse_args()


def add_program_options( option_parser ):
    option_parser.add_option( '-w', '--windowSize', type = 'int', \
                                       default = 100, \
                                       help = "Amount of characters from each alignment sequence to look at. Default is 100"
                                     )
    option_parser.add_option( '-s', '--stepSize', type = 'int', \
                             default = 100, \
                             help = "Amount of space to move over after each alignment of sequences. Default is 100"
                            )


if __name__ == '__main__':
    main()




