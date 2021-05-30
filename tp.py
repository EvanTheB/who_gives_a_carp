tps = [
	"xqr",
	"obk",
	"#hw",
	"y&t",
	"hsi",
	"ayg",
	"dcf",
	"mez",
	"l?p",
	"auv",
	"!nr",
	"pej",
]

def rec(words, pre, tps):
	if len(pre) == 4 and pre in dictionary:
		# print(pre)
		words = words + [pre]
		pre = ""
		if len(words) == 3:
			print(" ".join(words))

	if tps and len(pre) < 4:
		for next_roll in tps:
			next_tps = list(tps)
			next_tps.remove(next_roll)
			for next_letter in next_roll:
				rec(words, pre + next_letter, next_tps)

dictionary = set(
	open("/usr/share/dict/words.pre-dictionaries-common").read().split("\n")
)

rec([], "", tps)
