#!/usr/bin/env python3

import protein_lib as oligo
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

   # Determine what gaps constraints to use, if any
   gap_constraints = options.minLength if options.minLength else options.percentValid

   subset_names = []
   subset_seqs = []
   total_ymers = 0

   span_gaps = options.dont_span_gaps == None

   subset_names, subset_seqs, total_ymers = oligo.get_kmers_from_seqs( names,
                                                                       sequences,
                                                                       options.windowSize,
                                                                       options.stepSize,
                                                                       span_gaps,
                                                                       gap_constraint = gap_constraints
                                            )

   
   # create subset xmers from out ymers
   design_ymer_subset_names, subset_ymers, total_xmers = oligo.get_kmers_from_seqs( "",
                                                                       subset_seqs,
                                                                       options.XmerWindowSize,
                                                                       1,
                                                                       span_gaps
                                                                      )

   subset_xmer_names, subset_xmers, total_xmers = oligo.get_kmers_from_seqs( "",
                                                                             sequences,
                                                                             options.XmerWindowSize,
                                                                             1,
                                                                             span_gaps
                                                                           )  

   win_xmers_dict = {}
   for item in subset_xmers:
        win_xmers_dict[ item ] = 0

   output_names, output_seqs = subset_names, subset_seqs

   # Calculate redundancy of each xmer in the output ymers
   for current_output in set( subset_ymers ):
     if current_output in win_xmers_dict:
         win_xmers_dict[ current_output ] += 1 

   oligo.write_fastas( output_names, output_seqs, output_name = options.outPut )

   xmer_avg_redundancy = sum( win_xmers_dict.values() ) / float( len( win_xmers_dict ) )
   percent_total = calculate_percentage( len( output_seqs ), total_ymers )
   percent_output_xmers = calculate_percentage( len( subset_ymers ), len( win_xmers_dict ) ) 

   print( "Final design includes %d %d-mers ( %.2f%% of total )" % ( len( output_seqs ), options.windowSize, percent_total ) )
   print( "%d unique %d-mers in final %d-mers ( %.2f%% of total )" % ( len( subset_ymers), options.XmerWindowSize, options.windowSize, percent_output_xmers ) )
   print( "Average redundancy of %d-mers in %d-mers: %.2f" % ( options.XmerWindowSize, options.windowSize, xmer_avg_redundancy ) )


def calculate_percentage( first, second ):
   """
      Calculates what percent of second first is
      Params:
          first: integer or float first value
          second: integer or float second value
   """
   return ( first / float( second ) ) * 100 


def add_program_options( option_parser ):
   option_parser.add_option( '-a', '--alignment', help = "Fasta query file of sequence alignment to be used by program. [None, Required]"
   )

   option_parser.add_option( '-w', '--windowSize', type = 'int', \
                             default = 100, \
                             help = "Amount of characters from each alignment sequence to look at. [100]"
   )
   option_parser.add_option( '-o', '--outPut', default = "oligo_out.fasta", help = "Name of file program output will be written to. [oligo_out.fasta]"
   )
   option_parser.add_option( '-p', '--percentValid', type = 'float', default = 99.00, help = (
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
   option_parser.add_option( '--dont_span_gaps', help = (
                             "Include if you do not want sliding window approach to span gaps as it "
                             "walks across each sequence. Kmers with more than percentValid percent of gaps "
                             "or less than minLength number of gaps will be included. Otherwise, kmer searching will "
                             "be done across gaps."
                                                         ),
                             action = "store_true"

   )

    
  

if __name__ == '__main__':
           main()


