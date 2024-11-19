#!/bin/bash
n_try=1
t_out=3

# I01A
b_ip=192.168.108
for c in {1..4}; do (wget http://$b_ip.$c -t $n_try -T $t_out -O index_I01A$c.html); done

# I02A
b_ip=192.168.109
for c in {1..4}; do (wget http://$b_ip.$c -t $n_try -T $t_out -O index_I02A$c.html); done

# I03A
b_ip=192.168.110
for c in {1..4}; do (wget http://$b_ip.$c -t $n_try -T $t_out -O index_I03A$c.html); done
