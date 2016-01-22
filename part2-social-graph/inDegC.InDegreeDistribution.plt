#
# In-degree Distribution. G(8145, 10270). 370 (0.0454) nodes with in-deg > avg deg (2.5), 88 (0.0108) with >2*avg.deg (Wed Oct 14 18:08:21 2015)
#

set title "In-degree Distribution. G(8145, 10270). 370 (0.0454) nodes with in-deg > avg deg (2.5), 88 (0.0108) with >2*avg.deg"
set key bottom right
set logscale xy 10
set format x "10^{%L}"
set mxtics 10
set format y "10^{%L}"
set mytics 10
set grid
set xlabel "In-degree"
set ylabel "Count (CCDF)"
set tics scale 2
set yrange[1.000000:]
set terminal png size 1000,800
set output 'inDegC.InDegreeDistribution.png'
plot 	"inDegC.InDegreeDistribution.tab" using 1:2 title "" with linespoints pt 6,\
	f1(x)=5039.280026*x**-2.246233, f1(x) title "5e+003 * x^{-2.246}  R^2:0.98" with lines linewidth 3
