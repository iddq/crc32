#!/bin/bash

commands=(
    'poly -m 0x1337'
    'poly -r 0x1337'
    'table'
    'table 0'
    'reverse 0x13371337'
    'reverse 0x13371337 0 0xedb88320 -m'
    'undo -s 1QCCco 0x13371337'
    'calc -s 1QCCco'
)

for ((i = 0; i < ${#commands[@]}; i++))
do
    c="python crc32.py ${commands[$i]}"
    echo
    echo '$' $c
    $c
done
