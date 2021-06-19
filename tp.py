import itertools
from collections import defaultdict

from tpconf import tps, dictionary, alpha, letter_to_tp, all_tps
from dat import quadwords, wordquads, allwords

# return set of frozensets
def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return set(frozenset(x) for x in
    	itertools.chain.from_iterable(itertools.combinations(s, r) for r in range(len(s)+1)))

def out_wordlist(words):
	if not words:
		print("error: nothing found", file=sys.stderr)
	print("\n".join(words))
	# print(len(words))

def out_tp(tp, word):
	tp = set(tp)
	def howspell(suffix, tps_used):
		if suffix == "":
			assert(len(tps_used) == len(word))
			return tps_used
		for next_tp in (tp - set(tps_used)) & letter_to_tp[suffix[0]]:
			r = howspell(suffix[1:], tps_used + [next_tp])
			if r:
				return r
		return False
	spell = howspell(word, [])
	for l in spell:
		print(tps[l])
	print()

def get_remaining_words(used_words):
	possible_quads = set()
	possible_tps = set()
	len_used_words = len("".join(used_words))

	# list of quad options for each word
	used = [
		wordquads[word]
		for word in used_words
	]
	# print(used)

	#
	# for every way to make the words from quads
	for used_quads in itertools.product(*used):
		used_tps = set.union(*[set(u) for u in used_quads])
		if len(used_tps) != len_used_words:
			# skip if we have re-used some tp
			continue
		# Add this iterations unused quads
		unused_tps = frozenset(all_tps - used_tps)

		possible_quads.add(unused_tps)
		possible_tps |= unused_tps

		# if we found them all early abort
		if len(possible_tps) == len(all_tps):
			break
	all_possible_quads = set.union(*[powerset(pq) for pq in possible_quads])
	# print(possible_quads)
	# print(all_possible_quads)

	return set.union(*[quadwords.get(quad, set()) for quad in all_possible_quads])

def how_to_make(used_words):
	# list of quad options for each word
	used = [
		[quad for quad, words in quadwords.items() if word in words]
		for word in used_words
	]
	# print(used)

	# for every way to make the words from quads
	for used_quads in itertools.product(*used):
		used_tps = set.union(*[set(u) for u in used_quads])
		if len(used_tps) != len("".join(used_words)):
			# skip if we have re-used some tp
			continue
		for quad, word in zip(used_quads, used_words):
			out_tp(quad, word)

		return

	print("error, cant make those words")

# how_to_make(["lexicography"])

import sys
# phrases are A B C
if len(sys.argv) == 1:
	# print all As
	out_wordlist(allwords)

elif len(sys.argv) == 2:
	# print all Bs
	A = sys.argv[1]
	words = get_remaining_words([A])
	out_wordlist(words)

elif len(sys.argv) == 3:
	A = sys.argv[1]
	B = sys.argv[2]
	words = get_remaining_words([A, B])
	out_wordlist(words)

elif len(sys.argv) == 4:
	# print how to
	A = sys.argv[1]
	B = sys.argv[2]
	C = sys.argv[3]
	how_to_make([A,B,C])

