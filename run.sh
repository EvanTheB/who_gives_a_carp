A=$(python3 tp.py | fzf)
B=$(python3 tp.py $A | fzf)
C=$(python3 tp.py $A $B | fzf)

echo $A $B $C
python3 tp.py $A $B $C
