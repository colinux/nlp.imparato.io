from .tokenizer import custom_tokenizer

def configure(nlp):
    nlp.add_pipe(nlp.create_pipe('sentencizer'))
    nlp.tokenizer = custom_tokenizer(nlp)
