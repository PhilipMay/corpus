import sys
import time
from somajo import SoMaJo


filename = sys.argv[1]

out_filename = filename.replace(".txt", "_split.txt")

out_f_p = open(out_filename, "wt")

start_time = time.time()

LANGUAGE = "de_CMC"
tokenizer = SoMaJo(LANGUAGE)


# see https://github.com/tsproisl/SoMaJo/issues/17
def detokenize(tokens):
    """Convert SoMaJo tokens to sentence (str)."""
    result_list = []
    for token in tokens:
        if token.original_spelling is not None:
            result_list.append(token.original_spelling)
        else:
            result_list.append(token.text)

        if token.space_after:
            result_list.append(" ")
    result = "".join(result_list)
    result = result.strip()
    return result


def process_text_line(_line):
    _sentences = tokenizer.tokenize_text([_line])

    result = []

    for s in _sentences:
        sentence_string = detokenize(s)
        result.append(sentence_string)

    return result


with open(filename, "rt") as f_p:
    for line in f_p:
        try:

            sentences = process_text_line(line)

            for sentence in sentences:
                # ignore blank lines and make sure that stuff like "\n" is also ignored:
                if len(sentence) > 2:
                    # output_file.write(f"{sentence}\n")
                    out_f_p.write(sentence + "\n")

        except Exception as e:
            print(e)

print("Filtering for", filename, "took:", round(time.time() - start_time, 2), "seconds.")

out_f_p.close()
