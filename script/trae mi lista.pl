#!/usr/bin/perl

use strict;
use warnings;
use English;

use Path::Tiny;
use Try::Tiny;


# main
{
	my @target_directories = map { Path::Tiny::path($ARG) } @ARGV;
	push @target_directories, Path::Tiny->cwd;

	print "#------------------------------------------#\n";
	print "#                TackMyList                #\n";
	print "#------------------------------------------#\n";

	my $copied;
	for my $target(@target_directories){
		if($target->exists){
			$copied += SeekAndCopy($target);
		}
	}
	print "\n\nResumen: He copiado $copied canciones. Lo peto.\n\nya está cosaaa! :)\n\n";
}


sub SeekAndCopy {
	my $directory = shift;
	my @listas;
	my $n = 0;

	for my $file ( $directory->children(qr/\.m3u$/) ){
		
		print "\nHe encontrado la lista $file !\n";

		my $destino = Path::Tiny->cwd()->child($file->basename('.m3u'));
		$destino->mkpath;

		print "\n\tVeamos qué musiquilla tiene...\n\n";
		for my $song_path ( map {Path::Tiny::path($ARG) } $file->lines( {chomp => 1} ) ){
			if ( $song_path->is_absolute ){
				if( $song_path->exists and $destino->exists ){
					$song_path->copy( $destino->child( $song_path->basename) );
					print "\t\tcopiado $song_path a $destino\n";
					$n++;
				}else{
					print "\t\tERROR AL COPIAR $song_path\n";
				}
			}

		}
	}
	return $n;
}

exit 0;