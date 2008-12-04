#!/bin/bash
for i in `cat top95.txt`; do time python $1 $i; done
