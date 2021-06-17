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

dictionary = set(
	open("/usr/share/dict/words.pre-dictionaries-common").read().lower().split("\n")
)

dictionary = set.union(dictionary, [
	"evan",
	"lulu",
        "louise",
        "arlo",
        "lou",
])

alpha = set("abcdefghijklmnopqrstuvwxyz")

letter_to_tp = {
	k: set(q for q in range(len(tps)) if k in tps[q])
	for k in alpha
}
