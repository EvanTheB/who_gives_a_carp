#!/usr/bin/env bash

set -euo pipefail


case $# in
	0 )
		A=$(python3 tp.py | fzf)
		exec bash $0 $A
		;;
	1 )
		B=$(python3 tp.py $1 | fzf --preview "python3 tp.py $1 {}" --preview-window=down)
		exec bash $0 $1 $B
		;;
	2 )
		C=$(python3 tp.py $1 $2 | fzf)
		exec bash $0 $1 $2 $C
		;;
	3 )
		python3 tp.py $1 $2 $3
		echo $1 $2 $3
		;;
esac
