#!/usr/bin/perl

use strict;
use warnings;
use File::Copy qw(copy move);

opendir (DIR, '.') or die "CALAMIDAD!! $!";

my @listas;

while (my $archivo = readdir(DIR)) {	
	if ($archivo =~ /.*\.m3u$/){
		print "He encontrado la lista $archivo !\n";
		open ENTRADA, "<$archivo";
		my $carpeta = substr $archivo,0,-4;
	
		unless(-e $carpeta or mkdir $carpeta) {
			die "No he podido crear carpeta $carpeta :(\n";
		}

		my $n=0;
		my @no_copiadas;
		print "\tVeamos qué musiquilla tiene...\n\n";
		while (defined(my $linea = <ENTRADA>)) {
			chomp($linea);
			if (substr ($linea,0,1) eq '/'){
					$n++;
				my $ok = copy($linea,'./'.$carpeta );
                my @nombre_cancion = split /\//,$linea;
                move $carpeta.'/'.$nombre_cancion[-1], 
                                $carpeta."/".$n.' - '.$nombre_cancion[-1];
				if( $ok ){
					print "\t\tcopiado $linea\n";
				}else{
					print "\t\tERROR AL COPIAR $linea\n";
					$n--;
				}
			}
		}
		print "\n\tHe copiado $n canciones. Lo peto.\n\n";
		close ENTRADA;
		}
}

print "ya está cosaaa! :)\n\n";
