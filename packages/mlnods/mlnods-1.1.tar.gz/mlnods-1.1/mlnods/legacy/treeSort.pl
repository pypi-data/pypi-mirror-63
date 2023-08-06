#!/usr/bin/perl

################################################################
# Author: Yana Bromberg					       #
# Affiliation: CUBIC and Department of Biomedical Informatics  #
#		Columbia University			       #
#E-mail: bromberg@rostlab.org				       #
#	this is THE FINAL VERSION for March 14, 2006	       #
################################################################
use Getopt::Long;
select STDOUT; $| = 1;


#tree contains linked node information
%tree = ();
#links contains the number of links for each node
%links = ();
#head is the hash of knowledge where the node in the tree came from
%head = ();
#number is the hash of sequence number of each node
%number= ();
#accessory hash for printing cluster information
%cluster = ();
#accessory hash for printing cluster information
%muts = ();

#get the input
#($hssp, $splits, $cut, $opt, $gene_list, $links_lim, $file_opt) = @ARGV;

#set the default in case  no option is given
$links_lim = "infinite";
$opt = 0;
$f_opt = "self5";
$lin = 1;

$Lok = GetOptions ('t_file=s' => \$hssp,
                   's=i' => \$splits,
                   'cut=i' => \$cut,
                   'opt=i' => \$opt,
                   'g_file=s'     => \$gene_list,
                   'l=i' => \$links_lim,
		   'f_opt=s' => \$f_opt,
                   'help'  => \$opt_help,
		   	'arch=s' => \$arch
                   );

if ( ! $Lok ) {
	print STDERR "Invalid arguments found, -h or --help for help\n";
	exit(1);
}
if ( $opt_help ) {
	&help();
	exit(1);
}

if ($arch eq "win"){
	print STDOUT "architecture is windows\n";
	$lin = 0;
}
else{
	print STDOUT "architecture is linux/default \n";
}
#check if all the given files are present
if (!(-e "$gene_list")){
	print STDERR "No instance file $gene_list present. Exiting.\n";
	exit(1);
}
if (!(-e "$hssp")){
	print STDERR "No table file $hssp present. Exiting.\n";
	exit(1);
}

#check if all options are intact
if (!$splits){
	print STDOUT "What is the desired set number?\n";
	$splits = <STDIN>;
	$splits =~ s/\n//;
	if ($splits =~ /[^0-9]/){
		print STDERR "$splits is not a valid set number. Exiting.\n";
		exit(1);
	}
	else{
		print STDOUT "Using $splits as the desired set number\n";
	}
}
if (!($cut =~ /\d/)){
	print STDOUT "What is the desired similarity cutoff?\n";
	$cut = <STDIN>;
	$cut =~ s/\n//;
	if ($cut =~ /[^0-9]/){
		print STDERR "$cut is not a valid similarity cutoff. Exiting.\n";
		exit(1);
	}
	else{
		print STDOUT "Using $cut as the similarity cutoff\n";
	}
}
if (!$lin){
	$t_start = `time /T`;
	$rm = "del";
	$mv = "move";
}
else{
	$t_start = `date`;
	$rm = "rm";
	$mv = "mv";
}
		
#check for presence of previous junction files
if (-e "jctMuts1"){
	print STDOUT "Remove existing jctMuts files?[yes/no]\n";
	$i = <STDIN>;
	if ($i eq "yes\n"){
		`$rm jctMuts*`;
	}
	elsif ($i eq "no\n"){
		print STDERR "Please rename or move them\n";
		exit (1);
	}
	else{
		print STDERR "Answer not understood. Exiting.\n";
		exit (1);
	}
}

#if everything is in order  -- start 
#####################################
#this is the timing function
#####################################
#get strating time in seconds
print STDOUT "start time = $t_start";
if ($lin){
	$t_start =~ s/.+[^\d](\d+)\:(\d+):(\d+).+\n/$1\:$2\:$3/;
	$h_s = $1;
	$m_s = $2;
	$s_s = $3;
	$h_s *= 3600;
	$m_s *= 60;
	$s_ss = $h_s + $m_s + $s_s;
	$rm = "rm";
}
else{
	$t_start =~ s/(\d+)\:(\d+) ([A|P])M.*\n/$1\:$2 $3M/;
	$h_s = $1;
	$m_s = $2;
	$a = $3;
	if ($a eq "P"){
		$h_s += 12;
	}
	$h_s *= 3600;
	$m_s *= 60;
	$s_ss = $h_s + $m_s;
	$rm = "del";
}
$t_start=~ s/(\:|\s)/\_/g;
	
#####################################

#get the output file name
$out = $hssp;
$out =~ s/(.+\/)*([^\/]+)/$2/;
$error = $out;
$error = "$out.deleted";
open (ERR, ">$error");
$out .= ".jack";
if (!($f_opt eq "self")){
	$f_temp = $out;
	$f_temp =~ s/\.jack/\.table/;
}

if (-e "$out"){
	print STDOUT "$out exists. Move it to $out.$t_start?[yes/no]\n";
	$i = <STDIN>;
	if ($i eq "no\n"){
		print "Overwriting\n";
	}
	else{
		print STDOUT "Moved\n";
		`$mv $out $out.$t_start`;
	}
}
#reset the largest cluster's values
$max = $max_number = 0;
$muts_count = 0;
#get the sequences
print STDOUT "Get IDs from $gene_list\n";
open (IN, $gene_list) || die "Can't open $gene_list\n";
foreach $line (<IN>){
	if ($line =~ /\>/){
		$name = $line;
		#if counting the  number of instances to get the score
		if ($opt){
			$name =~ s/\>(.+\|)*([^ ]+)( |\n)//;
			$name = $2;
			$name =~ tr/a-z/A-Z/;
			$name =~ s/ |\n|\t//g;
			$name = " ".$name;
			#print STDOUT $name."\n";
			$muts_count++;
			if (exists $genes{$name}){
				$genes{$name}{"seq"} .= $line;
				$genes{$name}{"score"}++;
			}
			else{
				$genes{$name}{"seq"} = $line;
				$genes{$name}{"score"} = 1;
			}
		}
		else{
			$name =~ s/\>(.+\|)*([^ ]+)(\s+\d+)*( |\n)//;
			$name = $2;
			$score = $3;
			if (!($score)){
				$score = 50;
			}
			$score =~ s/\s+//g;
			$name =~ tr/a-z/A-Z/;
			$name =~ s/ |\n|\t//g;
			$name = " ".$name;
			$genes{$name}{"seq"} = $line;
			$genes{$name}{"score"} = $score;
			$score = 50;
		}
	}
	else{
		$genes{$name}{"seq"} .= $line;
	}		
}	
close IN;

#figure out how to get the table of values
#default where to get the similarity
$line_num = 2;
if ($f_opt =~ /blast/){
	print STDOUT "Getting blast output.  File is $f_temp.blast. Similarity is \%id\n";
	if (-e "$f_temp.blast"){
		print STDOUT "Use existing $f_temp.blast?[yes/no]\n";
		$i = <STDIN>;
		if ($i eq "no\n"){
			print STDOUT "Moving existing $f_temp.blast to $f_temp.blast.$t_start\n";
			`$mv $f_temp.blast $f_temp.blast.$t_start`;
			&getBlast();
		}
		else{
			print STDOUT "Using existing $f_temp.blast\n";
		}
	}
	else{
		&getBlast();
	}
	$hssp = "$f_temp.blast";
}
elsif ($f_opt eq "hssp"){
	print STDOUT "Running HSSP extraction. File is $f_temp.hssp. Similarity is HSSP distance\n";
	if (-e "$f_temp.hssp"){
		print STDOUT "Use existing $f_temp.hssp?[yes/no]\n";
		$i = <STDIN>;
		if ($i eq "no\n"){
			print STDOUT "Moved existing $f_temp.hssp to $f_temp.hssp.$t_start\n";
			`$mv $f_temp.hssp $f_temp.hssp.$t_start`;
			$j = `perl m8ToRdb.pl $hssp $f_temp.hssp`;
			if (!$j){
				print STDERR "Problem running the HSSP extraction. Exiting\n";
				exit (1);
			}
		}
		else{
			print STDOUT "Using existing $f_temp.hssp\n";
		}
	}
	else{
		`perl m8ToRdb.pl $hssp $f_temp.hssp`;		
		if (!(-e "$f_temp.hssp")){
			print STDERR "Problem running the HSSP extraction. Exiting\n";
			exit (1);
		}
	}
	$hssp = "$f_temp.hssp";
	$line_num = 4;
}
elsif ($f_opt =~ /self/){
	$line_num = $f_opt;
	$line_num =~ s/[^0-9]//g;
	$line_num--;
}

print STDOUT "Get similarity scores and create the tree\nGetting	.";
&getSim();
print STDOUT "\n";


$total_link = keys %links;
$total = $k_total = keys %genes;
print STDOUT "Total IDs $total read. Total with links $total_link\n";

#the limit of number of genes that can be in a single cluster
$limit = ceil($total/$splits);

if ($splits > $total){
	print STDERR "You want more sets ($splits) than there are IDs ($total)\n";
	exit (1);
}
print STDOUT "Largest cluster size should be no more than $limit to split $total IDs into $splits sets\n";

$cluster = 1;
$sum = 0;
$del = 0;
print STDOUT "Processing	";
open (OUT, ">$out\n");
#while linked nodes exist print them
while ((keys %links) >= 2){
	#start at random node V with minimal number of links and highest score
	@array = sort {$links{$a} <=> $links{$b} || $genes{$b}{"score"} <=> $genes{$a}{"score"}} keys %links;
	$orgnode = $array[0];
	#if this is a node with no links other than to itself
	#just print it as a cluster
	if ($links{$orgnode} == 1){
		$sum += &printResult($orgnode, $cluster);
		$cluster++;
		next;
	}
	#else if this node hasn't yet been deleted
	elsif (exists $tree{$orgnode}){
		#reset all calculations to starting point
		#variables changed in other subs are $traversed and $number
		$traversed = "";
		$number = 1;
		#reset the starting point to 0 here
		$head{$orgnode} = 0;
		#get the tree 
		#(passes name of node, number of node, head of node, option of backtacking, note that this is the original traversion)
		@result = &depthFirst($orgnode, 1, 0, 0, 1);
		print STDOUT ".";
		#if there's stuff in the traversed line, something is wrong
		if (!($traversed =~ /\w/)){
			print STDERR "Something's wrong in processing. Please contact the authors at bromberg\@rostlab.org. Exiting\n";
			exit(1);
		}
		#if everything is fine
		if ($result[2] == 0){
			#get rid of the nodes with more than set links_lim
			if (!($links_lim =~ /infinite/)){
				&shakeLinks();
			}
			#print the clusters
			$sum += &printResult($traversed, $cluster);
			$cluster++;
		}
		else{
			print STDERR "Something's wrong in processing. Please contact the authors at bromberg\@rostlab.org. Exiting\n";
			exit(1);
		}
	}
}

#for the remaining genes, just print them
foreach $key (keys %genes){
	if ($key =~ /\w/){
		$sum += &printResult($key, $cluster);
		$cluster++;
	}
}
close OUT;
close ERR;
print STDOUT "\nTotal remaining is $sum\n";
print STDOUT "Total deleted in splitting is - $del\n";
$link_del = $k_total - $sum - $del;
if ($link_del){
	print STDOUT "The rest ($link_del) was deleted by links limitations. If more instances are needed, loosen this feature\n";
}
print STDOUT "Printing $splits unique instance sets\n";

#if counting instances, reset the limit_muts by the number of instances, not number of genes
if ($opt){
	$limit_muts = &ceil($muts_count/$splits) ;
}
#else just get the remaining stuff
else{
	$limit_muts = &ceil($sum/$splits);
}
print STDOUT "Looking for approximately $limit_muts per set\n";

#set the limits
$order = 1;
while ($order <= $splits){
	$muts{$order}{"diff"} = $limit_muts;
	$order++;
}
#now cluster mutants starting from largest cluster
$order = 1;
$org_splits = $splits;
foreach $key (sort {$cluster{$b}{"count"} <=> $cluster{$a}{"count"}} keys %cluster){
	#this loop ends only when entry is placed
	TOTAL: while (1){
		#if these instances fit into the current bin - place them
		if ($muts{$order}{"diff"} >= $cluster{$key}{"count"}){
			$muts{$order}{"diff"} -= $cluster{$key}{"count"};
			$muts{$order}{"seq"} .= $cluster{$key}{"seq"};
			#reset the flag
			$flag = 0;
			last TOTAL;
		}
		#else is the number of instances is more than can fit into any bin
		#place them into a new one
		elsif ($cluster{$key}{"count"} > $limit_muts){
			print STDOUT "jctMuts$order file is larger than normal: size ".$cluster{$key}{"count"}." instead of $limit_muts\n";
			print STDOUT "	Look for a smaller size last jctMuts file [default: jctMuts$org_splits]\n";
			$muts{$order}{"seq"} = $cluster{$key}{"seq"};
			$muts{$order}{"diff"} = 0;
			$order++;
			last TOTAL;
		}
		#else just go on to next bin 
		else{
			if ($order == $splits){
				if ($flag == 0){
					$flag = 1;
					$order = 1;
				}
				else{
					print STDOUT "Extra jctMuts cluster will be created\n";
					$splits++;
					$muts{$splits}{"diff"} = $limit_muts;
					$order++;
				}
			}
			else{
				$order++;
			}
		}
	}
}
#print instances sorted as above
foreach $key (keys %muts){
	open (OUT, ">jctMuts$key");
	print OUT $muts{$key}{"seq"};
	close OUT;
}

#############################################
#time function end
#############################################
if ($lin){
	$t_start = `date`;
	print STDOUT "End time = $t_start\n";
	$t_start =~ s/[^\d](\d+)\:(\d+):(\d+)//;
	$h_e = $1;
	$m_e = $2;
	$s_e = $3;
	$h_e *= 3600;
	$m_e *= 60;
	$s_se = $h_e + $m_e + $s_e;
}
else{	
	$t_start =~ s/(\d+)\:(\d+) ([A|P])M//;
	$h_s = $1;
	$m_s = $2;
	$a = $3;
	if ($a eq "P"){
		$h_s += 12;
	}
	$h_s *= 3600;
	$m_s *= 60;
	$s_ss = $h_s + $m_s;
	if ($s_ss < 0){
		$s_ss += (24*60);
	}
}
$s_se = $s_se - $s_ss;
print STDOUT "Total running time is $s_se ";
if ($lin){
	print "seconds\n";
}
else{
	print "minutes\n";
}
##############################################

print STDOUT "Total clusters $cluster. Largest cluster (# $max_number) is of size $max\n";
print STDOUT "Output files are:\n";
print STDOUT " jctMuts[1..$splits] -- unique sets of instances \n";
print STDOUT " $out -- list of clusters created\n";
print STDOUT " $error -- list of deleted instances\n";


sub getSim{
	my $count = 0;
	open (IN, $hssp) || die "Can't open $hssp\n";
	my $del_temp = "";
	foreach $line (<IN>){
		if (($line =~ /\w/) and (!($line =~ /\#/))){
			$count++;
			if ($count == 10000){
				print STDOUT ".";
				$count = 0;
			}
			@line = split (/\s+/, $line);
			foreach $i (0..1){
				$line[$i] =~ s/\t|\n| //g;
				$line[$i] =~ tr/a-z/A-Z/;
				$line[$i] =~ s/(.+\|)*([^ ]+)/$2/;
				$line[$i] = " ".$line[$i];
			}
			#if the instances contain words
			if (($line[0] =~ /\w/) and ($line[1] =~ /\w/)){
			#and if there are no other issues
				if (exists $genes{$line[0]}){
					if (exists $genes{$line[1]}){
						if ((!($line[0] eq $line[1])) and (!(exists $tree{$line[0]}{$line[1]})) and ($line[0] =~ /\w/) and ($line[1] =~ /\w/)){
							#take care of e
							if ($line[$line_num] =~ /e/){
								$line[$line_num] =~ s/(.+)e(\-|\+)*(\d+)//;
								$base = $1;
								$sign = $2;
								$e = $3;
								while ($e > 0){
									if ($sign eq "+"){
										$line[$line_num] = $base * 10;
									}
									else{
										$line[$line_num] = $base/10;
									}
									$e--;
								}
							}
							#and if the similarity score is more than cutoff -- add the link
							if ($line[$line_num] >= $cut){
								#print "$line[0] $line[1] $line[$line_num]\n";
								&add_node ($line[0], $line[1]);
							}
						}
					}
					elsif (!($del_temp =~ / $line[1]\n/)){
						print STDOUT "\ndelete $line[1]. Not in Fasta list!\n";
						$del_temp .= " $line[1]\n";
					}
				}
				elsif (!($del_temp =~ / $line[0]\n/)){
					print STDOUT "\ndelete $line[0]. Not in Fasta list!\n";
					$del_temp .= " $line[0]\n";
				}
			}
		}
	}
	close IN;
}
#this sub gets rid of the nodes with more than the limit links
sub shakeLinks{
	my @array = split (/\n/, $traversed);
	my $clus;
	foreach $clus (sort { $links{$b} <=> $links{$a} || $genes{$a}{"score"} <=> $genes{$b}{"score"}} @array){
		if ($links{$clus} > $links_lim+1){
			print ERR "Delete key $clus that has ".$links{$clus}." links (more than $links_lim)\n"; 
			&delete_node($clus,1);
			$traversed =~ s/$clus\n//;
		}
	}
}

#this sub adds nodes into the tree
sub add_node{
	#create all needed links
	my $node = shift @_;
	my $node_prime = shift @_;
	
	if ($node =~ /\w/){		
		#in all cases establish a link between node and node_prime going both ways
		$tree{$node_prime}{$node} = 1;
		$tree{$node}{$node_prime} = 1;
		if (exists $links{$node}){
			$links{$node}++;
		}
		else{
			$links{$node} = 2;
		}
		if (exists $links{$node_prime}){
			$links{$node_prime}++;
		}
		else{
			$links{$node_prime} = 2;
		}
	}
	return;
}

#this is the actual trvaersion function
sub depthFirst{
	#this is the node name we are at right now
	my $head = shift @_;
	#this is the node number we are at right now
	my $order = shift @_;
	#this is the node number of the head of this node
	my $order_head = shift @_;
	#node to stop number going back to, if we are going back
	my $stop = shift @_;
	#note whether this is from an original call or from the inside call
	my $high = shift @_;
	
	my ($key, $temp, $c_order, $cue2, $stop2, @remaining, $t, $i, @array);
	
	#if we haven't exceeded the limit	
	if ($number <= $limit){
		#set the number of node
		$number{$order} = $head;
		#set the head of node
		$head{$head} = $order_head;
		#add name to traversed path
	#	print "adding $head $number\n";
		$traversed .= "$head\n";
		#increase the number in subtree
		$number++;
		#get the linked nodes in order of number of links
		@array = keys %{$tree{$head}};
		foreach $key (keys %{$tree{$head}}){
			if (!(exists $links{$key})){
				print STDERR "Something's wrong in processing. Please contact the authors at bromberg\@rostlab.org. Exiting\n";
				exit(1);
			}
		}
		if ((keys %{$tree{$head}}) > 1){
			@array  = sort {$links{$a} <=> $links{$b} || $genes{$b}{"score"}<=>$genes{$a}{"score"}} keys %{$tree{$head}};
		}
		else{
			@array = keys %{$tree{$head}};
		} 
		#foreach of the nodes
		$i = 0;
		$c_order = $order+1;
		while ($i < @array){
			$key = $array[$i];
			#print "acknowledging $key\n";
			#if the node still exists and isn't in the traversed path
			if ((exists $tree{$head}{$key}) and (!($traversed =~ /$key\n/))){
				#this should return temp, highest score of node reached
				#the cue to return if needed, and the number of the node at which to stop if needed
				($temp, $c_order, $cue2, $stop2) = &depthFirst($key, $c_order, $order, 0, 0);
				#if the first node of the tree has been deleted, restart
				if ($cue2 == 1){
					if ($order > $stop2){
						return ("", $c_order, 1, $stop2);
					}
					elsif ($stop2 >= $order){
						#erase everything that was done after and including max
						#and up to the node that we are at right now
						$c_order--;
						while ($c_order > $stop2){
							$temp = $number{$c_order};
							#print "deleting out of traversed $temp\n";
							#print "$traversed\n";
							$traversed =~ s/$temp\n//;
							#print "$traversed\n";
							$number--;
							delete $number{$c_order};
							delete $head{$temp};
							$c_order--;
						}
						#and just repeat this node over
						$i = -1;
					}
					
				}
			}
			$i++;
		}
		return ("", $c_order, 0, 0);
	}	
	else{
		#delete the maximal linker
		$del++;	
		$temp = $traversed;
		$temp =~ s/\n$//;
		@remaining = split(/\n/, $temp);
		
		foreach $i (@remaining){
			if (!(exists $links{$i})){
				print STDERR "Something's wrong in processing. Please contact the authors at bromberg\@rostlab.org. Exiting\n";
				exit(1);
			}
		}
		#if this is the only node in remaining then skip the rest
		if (@remaining > 1){
			#sort on the highest number of links, lowest score, and highest head, which is ladder-most location
			@sort = sort {$links{$b} <=> $links{$a} || $genes{$a}{"score"} <=> $genes{$b}{"score"} || $head{$b} <=> $head{$a}} @remaining;
			$max_key = $sort[0];
			$t = $links{$sort[0]};
		}
		else{
			$max_key = $remaining[0];
			$t = $links{$max_key};
		}
		
		$stop2 = $head{$max_key};
		$t--;
		$traversed =~ s/$max_key\n//;
		#print "deleting $max_key\n";
		print ERR "Delete maximal key $max_key with $t links.\n";#Returning to $stop2\n";
		&delete_node ($max_key, 1, 1);
		return ("", $order, 1, $stop2);
	}
	
}

#deleting the node
sub delete_node{
	#delete a node out of the tree
	my $node = shift @_;
	#flag if this is a max node being deleted
	my $flag = shift @_;
	#flag if this is the max being deletes
	my $max = shift@_;
	
	#delete the node's links
	delete $tree{$node};
	#delete the count of node's links
	delete $links{$node};
	#delete the mutants
	if ($opt and $flag){
		$muts_count -= $genes{$node}{"score"};
	}
	delete $genes{$node};
	
	#delete number stuff
	if (!$max){
		#delete head stuff
		delete $head{$node};
		foreach $key (keys %number){
			if ($number{$key} eq $node){
				delete $number{$key};
				last;
			}
		}
	}
	foreach $key (keys %tree){
		if (exists $tree{$key}{$node}){
			$links{$key}--;
			delete $tree{$key}{$node};
		}
	}
	if ($flag){
		$total--;
		$limit = &ceil($total/$splits);
	}
	
	return;
}


#print the results
sub printResult{
	my $result = shift @_;
	my $cluster = shift @_;
	my $size = 0;
	my ($mut, $t);
	
	print OUT "Cluster $cluster -- ";
	my @array = split (/\n/, $result);
	foreach $clus (@array){
		$t = $clus;
		$t =~ s/ //;
		print OUT "$t\t";
		if (exists $cluster{$cluster}{"count"}){
			$cluster{$cluster}{"seq"} .= $genes{$clus}{"seq"};
		}
		else{
			$cluster{$cluster}{"seq"} = $genes{$clus}{"seq"};
		}
			
		if ($opt){
			if (exists $cluster{$cluster}{"count"}){
				$cluster{$cluster}{"count"} += $genes{$clus}{"score"};
			}
			else{
				$cluster{$cluster}{"count"} = $genes{$clus}{"score"};
			}
		}
		else{
			if (exists $cluster{$cluster}{"count"}){
				$cluster{$cluster}{"count"}++;
			}
			else{
				$cluster{$cluster}{"count"} = 1;
			}
		}
		if ($cluster{$cluster}{"count"} > $max){
			$max = $cluster{$cluster}{"count"};
			$max_number = $cluster;
		}
		&delete_node($clus);
		$size++;
	}
	print OUT "\n";
	return $size;
}

#getting blast
sub getBlast{
	open (IN, $hssp) || die "Can't open $hssp\n";
	print STDOUT "Getting	.";
	my $count = 0;
	foreach $line (<IN>){
		$line =~ s/\n//;
		if ($line =~ /[A-Za-z0-9]/){
			$count++;
			if ($count == 1000){
				print STDOUT ".";
				$count = 0;
			}
			if (-e "$line"){
				
				`more $line >> $f_temp.blast`;
			}
			else{
				print STDOUT "No file $line exists. Skip or Exit?[s/e]\n";
				$i = <STDIN>;
				if ($i eq "s\n"){
					next;
				}
				elsif ($i eq "e\n"){
					print STDOUT "Exiting\n";
					exit(1);
				}
				else{
					print STDERR "Unknown answer $i. Exiting\n";
					exit(1);
				}
			}
		}
	}
	print STDOUT "\n";
	$hssp = "$f_temp.blast";
	close IN;
}

sub help {
    print STDERR
        "This is a script that will create independent sets of data \n",
        "Usage: treeSort.pl [options] -t_file table_file -s #_of_splits -cut similarity_cutoff -opt score_entry_option -g_file instance_list -l links_limit -f_opt file_options\n",
        "  Opt:	-h, --help	print this help\n",
	"	-arch <lin|win>		current supported architectures LINUX and Windows. \n",
	"				 Default LINUX (also seems good for MacOS 10)\n",
	"	-s <int>		number of splits required \n",
        "	-cut <int>		similarity cutoff in the units of link scores\n",
	"	-l <int>		limit on the number of links for each node(default = infinity)\n",
	"	-t_file <string>	file containing a table of instances with link scores for each pair\n",
        "	-f_opt <string>	format of the table file\n",
	"					blast - takes a list of -m 9 formated blast files and builds a table based on \%seqID\n",
	"					hssp - takes a list of -m 9 formated blast files, runs HSSP scoring script and \n",
	"					       builds an HSSP distance table\n",
	"					self<int> - space/tab separated table file, similarity score in column <int>\n",
	"						    eg \"ID1 ID2 similarity_score\" will be addressed as self3 \n",
	"						    default is self5\n",
      	"	-g_file <string>	instance file containing IDs of all instances being considered\n",
	"				IDs are case-independent (eg ABC = abc)\n",
	"				IDs are always preceeded by \">\" and followed by a white space.\n",
	"				No white spaces are allowed in an ID.\n",
	"				If score is provided for an ID, it should be surrounded by spaces and directly follow the ID\n",
	"				(eg. >abl1_human 10 gene associated with ....)\n",
	"				Everything between two IDs is printed in the junction files, but not considered in evaluation\n",
        "	-opt <int>		the option to score:\n",
	"					0 - use score provided in instance file (or default)\n",
	"					    score is optional (default score = 50)\n",
	"					    score range is [0-100]\n",
	"					1 - use score = actual number of time the ID appears in the instance file\n",	
	"If an ID is present in the instance file, but not in the table file the ID is considered to not be linked to anything else\n",
	"If an ID is present in the table file but not in the instance file, it is ignored\n";
}
sub ceil {
	my $number = shift @_;
	if (int($number) == $number){
		return $number;
	}
	else{
		return (int($number)+1);
	}
}
