
set term postscript eps enhanced color solid
set encoding utf8
set output "dh.eps"
#set size 1.0,0.6

set style line 10 lt 1 lw 2 lc rgb "#000000"
set style line 11 lt 2 lw 2 lc rgb "#ff0000" 
set style line 12 lt 3 lw 1 lc rgb "#0000ff" dt(10,3)
set style line 13 lt 2 lw 2 lc rgb "#269800"
set style line 14 lt 2 lw 2 lc rgb "#6500cb" dt 8
set style line 15 lt 2 lw 1 lc rgb "#009898"
set style line 16 lt 2 lw 1 lc rgb "#ff7f00"
set style line 4 lt 1 pt 7 ps 1.2 lc rgb "#000000"

set tics font "Helvetica,12"
set xlabel font "Helvetica,12"
set ylabel font "Helvetica,12"
set y2label font "Helvetica,12"
set key font "Helvetica,12"
set title font "Helvetica,12"

exp="/Users/okumuras/Dropbox/calculations/oyak/experimental/"
# https://www.utf8-chartable.de/unicode-utf8-table.pl

set multiplot layout 3,1 margins screen 0.1,0.5,0.1,0.96 spacing screen 0.02

set log x
set format x ""

set key top right
set yrange [0:1]
set ylabel "t · DH({/Symbol b}) (MeV/fission)"
plot exp.'ORNL/exp235b_or' u 1:2:3 w yerr ti 'ORNL_{th}' ls 15 pt 7,\
     exp.'Lowell/ExpU235B' u 1:2:3 w yerr ti 'Lowell_{th}' ls 13 pt 9,\
     'JENDL4.0+JENDFPD2015.out' u 2:6 w l ti 'JENDL/FPY-2011' ls  12,\
     'GEF+JENDFPD2015.out' u 2:6 w l ti 'GEF+TALYS' ls  11,\
#     "JENDL4.0+ENDFBV8DDL.out" u 2:6 w l ti 'ENDF' ls  9,\

set key top right
set yrange [0:1.0]
set ylabel "t · DH({/Symbol g}) (MeV/fission)"
plot exp.'ORNL/exp235g_or' u 1:2:3 w yerr ti 'ORNL_{th}' ls 15 pt 7,\
     exp.'Lowell/ExpU235G' u 1:2:($2*$3/100.0) w yerr  ti 'Lowell_{th}' ls 13 pt 9,\
     'JENDL4.0+JENDFPD2015.out' u 2:7 w l ti 'JENDL/FPY-2011' ls  12,\
     'GEF+JENDFPD2015.out' u 2:7 w l ti 'GEF+TALYS' ls  11

#"JENDL4.0+ENDFBV8DDL.out" u 2:7 w l ti 'ENDF' ls  9,\

unset format x
set log x
set ylabel offset 2.5
set xlabel "cooling time (sec.)"
set key top right
set yrange [0:0.005]
set ylabel "t · DN (/fission)"
plot exp.'keepin.an2' i 0 u 1:($2*(0.0160/0.0148)):3  ti 'Keepin_{th}' w yerror ls 15 pt 7,\
     'JENDL4.0+JENDFPD2015.out' u 2:8 w l ti 'JENDL/FPY-2011' ls  12,\
     'GEF+JENDFPD2015.out' u 2:8 w l ti 'GEF+TALYS' ls  11,\

#"JENDL4.0+ENDFBV8DDL.out" u 2:8 w l ti 'ENDF' ls  9,\
  