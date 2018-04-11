#!/usr/bin/env python3
import protein_oligo_library as oligo
import optparse

def main():
   usage = "usage: %prog [options]"
   option_parser = optparse.OptionParser( usage )

   add_program_options( option_parser )


def add_program_options( option_parser ):
    option_parser.add_program_options( '-w', '--windowSize', type = 'int', \
                                       default = 100, \
                                       help = "Amount of characters from each alignment sequence to look at."
                                     )
    option_parser.add_option( '-s', '--stepSize', type = 'int', \
                             default = option_parser.windowSize, \
                             help = "Amount of space to move over after each alignment of sequences. Default is set to window_size."
                            )


if __name__ == '__main__':
    main()




