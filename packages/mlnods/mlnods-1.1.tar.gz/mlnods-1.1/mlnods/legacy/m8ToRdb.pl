#! /usr/bin/perl

##################################################################
#  Script used to parse the m8 files created by PsiBlastRun.pl   #
#  results in rdb file used in tmphsspsums.pl script to          #
#  evaluate Accuracy and Coverage.                               #
#  (created by DP 2/4/02) DEBUGGED 5/24/03                       #
#  for actual Debug comments look at the m8toRDB script in       #
#  ~kaz/temp/m8toRdb.pl_tmp                                      # 
##################################################################

#create m8.list from m8 files with unix command ls -1 *_m8 > m8.list or \ls.

($m8List,$FileOut)=@ARGV;   
die "$0: arguments m8List not defined\n"
    if(!defined $m8List );
if(! defined $dbg){ $dbg=0; }

#$par{'fasta_dir'}="/data/derived/big/splitPdb/";
open(FHLIST,$m8List) ||
    die "failed to open m8List=$m8List, stopped";
@m8Files=<FHLIST>;
close FHLIST;
@m8Files=map {s/\s//g; $_; } @m8Files;

if(! defined $FileOut ){ 
    $tmp=$m8List; 
    $tmp=~s/.*\///; 
    $tmp=~s/\..*$//;
    $FileOut=$tmp."_NEW.rdb";
}

$par{'MinLali'}         =12;    #minimum alignment length to be considered
$par{'MinHsspDistRep'}  =-1000;   #minimum hssp distance to report 
$par{'MinIdeRep'}       =-10;   #minimum pid to report 

$HsspThresh =$par{'MinHsspDistRep'};
$IDEThresh  =$par{'MinIdeRep'};
open(FHOUT, ">".$FileOut) ||   
    die "ERROR, failed to open FileOut=$FileOut, stopped";

FILE: foreach $m8File (@m8Files){
    undef %h_Results;
    open(FHIN,$m8File) || die "did not open m8File=$m8File<<, stopped";
    while(<FHIN>){
	#print;
	next if(/^\s+$/);
	next if(/^\#/);
	s/^\s+|\s+$//g;
	@data=split(/\s+/, $_);
	if($#data != 11){ print  "wrong format of m8File=$m8File, continue..."; next FILE; }  #check format
	($Query,$Subject,$ideWgap,$lenWgap,$mismatchNo,$gapOpenNo,$qstart,$qend,$sstart,$send,$Escore,$Bitscore)
	    =@data;
	
	$Subject=~s/.*\|//; $Query=~s/.*\|//; $Subject=~s/\w+://;
	$Subject=~tr[A-Z][a-z]; $Query=~tr[A-Z][a-z];

	undef $gapOpenNo; undef $psim; 
	$ideNo=sprintf "%3.0f", $lenWgap * $ideWgap/100;
	$aliLen=$ideNo + $mismatchNo;
	$gapLen=2 * $lenWgap -($qend-$qstart +1 + $send-$sstart +1);
	$aliLenCheck=$lenWgap -$gapLen;
	#die "alignment lengths in file=$m8File $Query $Subject calculated in independent ways not eqal: $aliLen vs $aliLenCheck in line:\n$_\n, stopped" 
	 #   if($aliLen != $aliLenCheck);
	$pide=$ideNo/$aliLen * 100;
	$psim=$mismatchNo/$aliLen * 100;
	
     
	#next if($Subject eq $Query);
	if($aliLen < $par{'MinLali'} ){ print "too short $aliLen vs $par{MinLali}\n"; next;}
	#($pid,$msg)=&getDistanceNewCurveIde($LEN);
	#if(!$pid) {print "\nERROR getDistanceNewCurveIde failed for m8File=$m8File Query=$Query Subject=$Subject with message=$msg...continue..."; next File;}
	$HsspDist=&hssp_dist($pide,$aliLen);
  
	if($HsspDist < $par{'MinHsspDistRep'} ){print "below threshold\n"; next;}
	$EThreshFlag=$HsspThreshFlag=$IDEThreshFlag=1;
	if( defined $HsspThresh ){
	    if( $HsspDist >= $HsspThresh )   { $HsspThreshFlag=1; }
	}
	else                                 { $HsspThreshFlag=1; }
	
	if( defined $EThresh ){
	    if( $Escore <= $EThresh )        { $EThreshFlag=1; }
	}
	else                                 { $EThreshFlag=1; }
	
	if( defined $IDEThresh ){
	    if( $pide >= $IDEThresh )        { $IDEThreshFlag=1; }
	}
	else                                 { $IDEThreshFlag=1; }

	if( $EThreshFlag && $HsspThreshFlag && $IDEThreshFlag ){
	    if(defined $h_Results{$Query}{$Subject} ){ 
		#print "WARNING: alignment $Query and $Subject already found\n"; 
		next;
	    }
	    $h_Results{$Query}{$Subject}{'score'}=$Escore;
	    $HsspDist   =sprintf "%6.1f", $HsspDist;
	    $Escore     =sprintf "%3.1e", $Escore;
	    $Bitscore   =sprintf "%6.1f", $Bitscore;
	    $pide       =sprintf "%6.1f", $pide;
	    #print "got here!!!!!!!!!!!!!!!!!!!!!!!!!\n";
	    $h_Results{$Query}{$Subject}{'data'}=$Query."\t".$Subject."\t".$aliLen."\t".$pide."\t".$HsspDist."\t".$Escore."\t".$Bitscore."\n";
	}#else{ #print "$Subject not considered\n"; }
	 #print "Query: $Query\n";
    }
    close FHIN;
    @SortedIds=sort { $h_Results{$Query}{$a}{'score'} <=> $h_Results{$Query}{$b}{'score'} } keys %{ $h_Results{$Query} };
    #print "Query check: $Query\n";
    #@SortedIds=sort keys %{ $h_Results{$Query} };
    #print "SortedIds: @SortedIds\n"; 
    foreach $Subject (@SortedIds){
	if($h_Results{$Query}{$Subject}{'data'} !~ /\n$/){$h_Results{$Query}{$Subject}{'data'}.="\n"; }
	print FHOUT $h_Results{$Query}{$Subject}{'data'};
    }				
    undef %h_Results;
}
close FHOUT;



#=========================================================================
# calculates HSSP-Distance using the formula from Burkhard's
# HSSP-Paper 1999
sub hssp_dist {
    my $sbr="hssp_dist";
    my($pi) = shift;
    my($len) = shift;

    die "$sbr: args not defined, stopped"
	if(! defined $pi || ! defined $len);
    if ($len <= 11) {
        return -999;
    }
    elsif ($len > 450) {
        return $pi - 19.5;
    }
    else {
        my($exp) = -0.32 * (1 + exp(- $len / 1000));
        return $pi - (480 * ($len ** $exp));
    }
}
#=====================================================================
#==============================================================================
sub getDistanceNewCurveIde {
    local($laliLoc)=@_; local($expon,$loc);
    
#-------------------------------------------------------------------------------
#   getDistanceNewCurveIde      out= pide value for new curve
#       in:                     $lali
#       out:                    $pide
#                               pide= 510 * L ^ { -0.32 (1 + e ^-(L/1000)) }
#-------------------------------------------------------------------------------
    $sbrName="lib-br:getDistanceNewCurveIde";
    return(0,"*** ERROR $sbrName: lali not defined \n") if (! defined $laliLoc);
    return(0,"*** ERROR $sbrName: '$laliLoc' = alignment length??\n") 
	if (length($laliLoc)<1 || $laliLoc=~/[^0-9.]/);

    $expon= - 0.32 * ( 1 + exp (-$laliLoc/1000) );
    $loc= 510 * $laliLoc ** ($expon);
    $loc=100 if ($loc>100);     # saturation
    return($loc,"ok $sbrName");
}				# end of getDistanceNewCurveIde

#------------------------------------------------------------------------------------------------------------------

# Perl-RDB  format
#
# NOTA: id1          =  guide sequence
# NOTA: id2          =  aligned sequence
# NOTA: lali         =  alignment length
# NOTA: pide         =  percentage sequence identity
# NOTA: dist         =  distance from new HSSP curve
# NOTA: Escore       =  BLAST expectation score
# NOTA: score        =  BLAST raw score
# --------------------------------------------------------------------------------
# PARA: minLali      =     12
# PARA: minDist      =   -10.0
# --------------------------------------------------------------------------------
#id1	id2	lali	pide	dist	Escore	score













