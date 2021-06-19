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
lentp = len(tps)

if "isascii" not in str.__dict__:
	isascii = lambda x: all(ord('a') <= ord(c) <= ord('Z') for c in x)
else:
	isascii = str.isascii


dictionary = set.union({
	w.lower() for w in
	open("/usr/share/dict/words.pre-dictionaries-common").read().split("\n")
	if isascii(w) and w.isalpha() and lentp >= len(w) > 2
	}, {
	"evan",
	"lulu",
	"louise",
	"arlo",
	"lou",
})

alpha = set("abcdefghijklmnopqrstuvwxyz")

letter_to_tp = {
	k: set(q for q in range(len(tps)) if k in tps[q])
	for k in alpha
}

all_tps = set(range(len(tps)))
