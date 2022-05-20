#!/usr/bin/env python3
# Copyright 2017-present, Facebook, Inc.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
"""Tokenizer that is backed by spaCy (spacy.io).

Requires spaCy package and the spaCy english model.
"""

import spacy
import copy
from .tokenizer import Tokens, Tokenizer


class SpacyTokenizer(Tokenizer):

    def __init__(self, **kwargs):
        """
        Args:
            annotators: set that can include pos, lemma, and ner.
            model: spaCy model to use (either path, or keyword like 'en').
        """
        model = kwargs.get('model', 'en_core_web_sm')
        self.annotators = copy.deepcopy(kwargs.get('annotators', set()))
        #print(self.annotators)
        #nlp_kwargs = {'parser': False}
        nlp_kwargs = {}
        #if not any([p in self.annotators for p in ['lemma', 'pos', 'ner']]):
        #    nlp_kwargs['tagger'] = False
        #if 'ner' not in self.annotators:
        #    nlp_kwargs['entity'] = False
        #print(nlp_kwargs)
        #self.nlp = spacy.load(model, **nlp_kwargs)
        self.nlp = spacy.load(model)

    def tokenize(self, text, no_spaces = False):
        # We don't treat new lines as tokens.
        #print("hi")
        if no_spaces:
            clean_text = text.replace('\n', ' ')
        else:
            clean_text = text
        tokens = self.nlp.tokenizer(clean_text)
        #if any([p in self.annotators for p in ['lemma', 'pos', 'ner']]):
        #    self.nlp.tagger(tokens)
        #if 'ner' in self.annotators:
        #    self.nlp.entity(tokens)

        data = []
        for i in range(len(tokens)):
            # Get whitespace
            start_ws = tokens[i].idx
            if i + 1 < len(tokens):
                end_ws = tokens[i + 1].idx
            else:
                end_ws = tokens[i].idx + len(tokens[i].text)

            data.append((
                tokens[i].text,
                text[start_ws: end_ws],
                (tokens[i].idx, tokens[i].idx + len(tokens[i].text)),
                tokens[i].tag_,
                tokens[i].lemma_,
                tokens[i].ent_type_,
            ))

        # Set special option for non-entity tag: '' vs 'O' in spaCy
        return Tokens(data, self.annotators, opts={'non_ent': ''})