#
# Out-degree Distribution. G(8145, 10270). 471 (0.0578) nodes with out-deg > avg deg (2.5), 433 (0.0532) with >2*avg.deg (Wed Oct 14 18:08:21 2015)
#

set title "Out-degree Distribution. G(8145, 10270). 471 (0.0578) nodes with out-deg > avg deg (2.5), 433 (0.0532) with >2*avg.deg"
set key bottom right
set logscale xy 10
set format x "10^{%L}"
set mxtics 10
set format y "10^{%L}"
set mytics 10
set grid
set xlabel "Out-degree"
set ylabel "Count (CCDF)"
set tics scale 2
set yrange[1.000000:]
set terminal png size 1000,800
set output 'outDegC.OutDegreeDistribution.png'
plot 	"outDegC.OutDegreeDistribution.tab" using 1:2 title "" with linespoints pt 6,\
	f1(x)=5723.002784*x**-1.350144, f1(x) title "6e+003 * x^{-1.35}  R^2:0.66" with lines linewidth 3
