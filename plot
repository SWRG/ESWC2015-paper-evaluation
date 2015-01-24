set terminal postscript eps size 3.5,2.62 enhanced color font 'Helvetica,16' linewidth 2
set output filename.'.eps'
set xlabel 'triples [percentage]'
set x2label 'number of edges [x10^6]'
set xtics nomirror
set x2tics
set ylabel 'time [sec]'
set key left
set tmargin at screen 0.84
plot filename using 3:1 axes x1y1 with linespoints title 'triples', filename using 2:1 axes x2y1 with linespoints title 'edges'