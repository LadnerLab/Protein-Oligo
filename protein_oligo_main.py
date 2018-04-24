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

   subset_names = []
   subset_seqs = []

   for index in range(0, len( sequences[ 0 ] ) - options.windowSize + 1, options.stepSize ):

      win_seqs = [ x [ index:index + options.windowSize] for x in sequences]
      win_names, win_seqs = oligo.create_valid_sequence_list( names, win_seqs, options.minLength, options.percentValid )
      win_seqs = [ oligo.remove_char_from_string( item, '-' ) for item in win_seqs ]


      for each in set( win_seqs ):
         subset_seqs.append( each )
         subset_names.append( win_names[ win_seqs.index( each ) ] )


   win_xmers_dict = {}
   # create dictionary of xmer-size keys to track score of each xmer
   for sequence in sequences:

      subset_name, subset_xmer = oligo.subset_lists_iter( [], sequence, options.XmerWindowSize, 1 )
      subset_name, subset_xmer = oligo.create_valid_sequence_list( "", subset_xmer, options.minLength, options.percentValid )
      subset_xmer = [ oligo.remove_char_from_string( item, '-' ) for item in subset_xmer ]

      for item in subset_xmer:
         if item in win_xmers_dict:
            win_xmers_dict[ item ] += 1
         win_xmers_dict[ item ] = 0

   ymer_seq_list = []

   subset_ymers = set()
   
   for index in range( len( sequences ) ):
      subset_name, subset_sequence = oligo.subset_lists_iter( names[ index ], sequences[ index ], options.windowSize, options.stepSize )
      subset_sequence = [ oligo.remove_char_from_string( item, '-' ) for item in subset_sequence ]

      for current_subset in subset_sequence:

         subset_name, subset_ymer = oligo.subset_lists_iter( "", current_subset, options.XmerWindowSize, 1 )

         # add each element in subset_ymer if the length of that item is > 1 and it is a valid sequence 
         [ subset_ymers.add( item ) for item in subset_ymer if len( item ) > 1 and oligo.is_valid_sequence( item, options.minLength, options.percentValid ) ] 

         if oligo.is_valid_sequence( current_subset, options.minLength, options.percentValid ):
            ymer_seq_list.append( current_subset )


   output_names, output_seqs = oligo.create_list_of_uniques(subset_names, subset_seqs)

   oligo.write_fastas( output_names, output_seqs, output_name = options.outPut )

   percent_total = ( len( output_seqs ) / float( len( ymer_seq_list ) ) ) * 100 
   percent_xadf =  ( len( subset_ymers ) / len( win_xmers_dict ) ) * 100 

   print( "Final design includes %d %d-mers ( %.2f%% of total )" % ( len( output_seqs ), options.windowSize, percent_total ) )
   print( "%d unique %d-mers in final %d-mers ( %.2f%% of total )" % ( len( subset_ymers), options.XmerWindowSize, options.windowSize, percent_xadf ) )





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
   option_parser.add_option( '-x', '--XmerWindowSize', type = 'int', default = 8, help = (
      "Window size of Xmer sequences used in redundancy calculations [8]."
      )
      )
    
  

if __name__ == '__main__':
           main()


