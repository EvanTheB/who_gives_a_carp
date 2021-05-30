A=$(python3 tp.py | fzf)
B=$(python3 tp.py $A | fzf --preview "python3 tp.py $A {}" --preview-window=down)
C=$(python3 tp.py $A $B | fzf)

echo $A $B $C
python3 tp.py $A $B $C
