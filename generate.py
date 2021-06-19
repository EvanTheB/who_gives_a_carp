import itertools
from collections import defaultdict

from tpconf import tps, dictionary, alpha, letter_to_tp, all_tps

def ints_to_quads(ints):
	return (list(itertools.combinations(ints, 5))
	 + list(itertools.combinations(ints, 4))
	 + list(itertools.combinations(ints, 3))
	 # + list(itertools.combinations(ints, 2))
	 # + list(itertools.combinations(ints, 1))
	)

# this is all the 12 choose 4 comboes of tp rolls
# + the other lengths, still called quads
quads = ints_to_quads(list(range(len(tps))))

# all the words that can be made from a quad
# by considering all permutations
def words(quad):
	"""
	time is sum(k=1, k=n)(n choose k * k!)
	= n! / (n-1)! + ... + n! / 0!
	n = 12, ~1e9
	"""
	ret = []
	for order in itertools.permutations(quad):
		quad_tps = [tps[i] for i in order]
		for word in itertools.product(*quad_tps):
			word = ''.join(word)
			if word in dictionary:
				# print(word)
				ret.append(word)
			elif word[-1] in "?!" and word[:-1] in dictionary:
				ret.append(word)
			# elif word[0] in "#" and word[1:] in dictionary:
			# 	ret.append(word)
	return set(ret)

# by trying to spell each word
def words2():
	"""
	time is #words * #letters * #tps
	~1e5 * ~6 * 12 = 1e7
	"""
	# mapping from word to what quads spell it
	# use sets because multiple ways to spell a word from a quad
	wordquads = defaultdict(set)
	# quad to words it spells
	quadwords = defaultdict(set)

	# same but with bitset
	iletter_to_tp = {}
	for k in alpha:
		iletter_to_tp[k] = 0
		for i, tp in enumerate(tps):
			if k in tp:
				iletter_to_tp[k] |= 1 << i

	bits_to_quads = {}
	for i in range(1 << len(tps)):
		toadd = list()
		j = i
		while j > 0:
			ffs = (j & (-j)).bit_length() - 1
			j -= j & (-j)
			toadd.append(ffs)
		bits_to_quads[i] = frozenset(toadd)


	iall_tps = (1 << len(tps)) - 1
	def canspell(word, suffix, tps_left):
		if suffix == "":
			used_tps = iall_tps & (~tps_left)
			# assert(len(used_tps) == len(word))
			wordquads[word].add(bits_to_quads[used_tps])
			quadwords[bits_to_quads[used_tps]].add(word)
			return
		# mask to only tps with next letter
		next_tps = tps_left & iletter_to_tp[suffix[0]]
		# foreach set bit
		while next_tps > 0:
			next_bit = next_tps & (-next_tps)
			next_tps -= next_bit
			canspell(word, suffix[1:], tps_left - next_bit)

	for word in dictionary:
		canspell(word, word, iall_tps)

	return wordquads, quadwords

# print(len(quads)) # 1507

# mapping from quad to the words they can spell
# quadwords = {}
# for quad in quads:
# 	quadwords[quad] = words(quad)

wordquads, quadwords = words2()

# all the possible words
allwords = set.union(*list(quadwords.values()))

print(f"wordquads = {dict(wordquads)}")
print(f"quadwords = {dict(quadwords)}")
print(f"allwords = {allwords}")

