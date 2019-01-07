import regex as re
from copy import deepcopy
from spacy.tokenizer import Tokenizer
from spacy.lang.fr.tokenizer_exceptions import _hyphen_prefix, _other_hyphens, _elision_prefix, HYPHENS, ELISION, ALPHA_LOWER, URL_PATTERN
from spacy import util

_regular_exp = [
    '^droits?[{hyphen}]de[{hyphen}]l\'homm[{alpha}]+$'.format(hyphen=HYPHENS, alpha=ALPHA_LOWER),
    '^zig[{hyphen}]zag[{alpha}]*$'.format(hyphen=HYPHENS, alpha=ALPHA_LOWER),
    '^prud[{elision}]homm[{alpha}]*$'.format(elision=ELISION, alpha=ALPHA_LOWER)]
_regular_exp += ["^{prefix}[{hyphen}][{alpha}][{alpha}{elision}]*$".format(
                 prefix=p, hyphen=HYPHENS,
                 elision=ELISION, alpha=ALPHA_LOWER)
                 for p in _hyphen_prefix]
_regular_exp += ["^{prefix}[{elision}][{alpha}][{alpha}{elision}{hyphen}\-]*$".format(
                 prefix=p, elision=ELISION, hyphen=_other_hyphens, alpha=ALPHA_LOWER)
                 for p in _elision_prefix]
_regular_exp.append(URL_PATTERN)

TOKEN_MATCH = re.compile('|'.join('(?:{})'.format(m) for m in _regular_exp), re.IGNORECASE).match

def custom_tokenizer(nlp):
    prefixes = deepcopy(nlp.Defaults.prefixes)
    prefixes += ("-",)

    infixes = deepcopy(nlp.Defaults.infixes)
    infixes += ("^{prefix}[{hyphen}][{alpha}][{alpha}{elision}]*".format(
        prefix=p, hyphen=HYPHENS,
        elision=ELISION, alpha=ALPHA_LOWER)
        for p in _hyphen_prefix)

    suffixes = deepcopy(nlp.Defaults.suffixes)
    suffixes += ("-", "(?<!\.[A-Z])(?<=[A-Z])\.",)


    prefix_re = util.compile_prefix_regex(prefixes)
    infix_re = util.compile_infix_regex(infixes)
    suffix_re = util.compile_suffix_regex(suffixes)

    return Tokenizer(nlp.vocab, prefix_search=prefix_re.search,
                                suffix_search=suffix_re.search,
                                infix_finditer=infix_re.finditer,
                                token_match=TOKEN_MATCH)
