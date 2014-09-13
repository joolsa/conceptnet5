#!/usr/bin/env python
# -*- coding: utf-8 -*-

# CAVEAT UTILITOR
#
# This file was automatically generated by Grako.
#
#    https://pypi.python.org/pypi/grako/
#
# Any changes you make to it will be overwritten the next time
# the file is generated.


from __future__ import print_function, division, absolute_import, unicode_literals
from grako.parsing import graken, Parser


__version__ = (2014, 8, 27, 18, 2, 40, 2)

__all__ = [
    'de_wiktionaryParser',
    'de_wiktionarySemantics',
    'main'
]


class de_wiktionaryParser(Parser):
    def __init__(self, whitespace='', nameguard=True, **kwargs):
        super(de_wiktionaryParser, self).__init__(
            whitespace=whitespace,
            nameguard=nameguard,
            **kwargs
        )

    @graken()
    def _left_bracket_(self):
        self._token('[')

    @graken()
    def _right_bracket_(self):
        self._token(']')

    @graken()
    def _left_brace_(self):
        self._token('{')

    @graken()
    def _right_brace_(self):
        self._token('}')

    @graken()
    def _left_brackets_(self):
        self._token('[[')

    @graken()
    def _right_brackets_(self):
        self._token(']]')

    @graken()
    def _left_braces_(self):
        self._token('{{')

    @graken()
    def _right_braces_(self):
        self._token('}}')

    @graken()
    def _left_paren_(self):
        self._token('(')

    @graken()
    def _right_paren_(self):
        self._token(')')

    @graken()
    def _hash_char_(self):
        self._token('#')

    @graken()
    def _vertical_bar_(self):
        self._token('|')

    @graken()
    def _equals_(self):
        self._token('=')

    @graken()
    def _bullet_(self):
        self._token('*')

    @graken()
    def _colon_(self):
        self._token(':')

    @graken()
    def _comma_(self):
        self._token(',')

    @graken()
    def _semicolon_(self):
        self._token(';')

    @graken()
    def _slash_(self):
        self._token('/')

    @graken()
    def _dash_(self):
        with self._choice():
            with self._option():
                self._token('-')
            with self._option():
                self._token('—')
            with self._option():
                self._token('–')
            self._error('expecting one of: - – —')

    @graken()
    def _plus_sign_(self):
        self._token('+')

    @graken()
    def _single_left_bracket_(self):
        self._left_bracket_()
        with self._ifnot():
            self._left_bracket_()

    @graken()
    def _single_right_bracket_(self):
        self._right_bracket_()
        with self._ifnot():
            self._right_bracket_()

    @graken()
    def _single_left_brace_(self):
        self._left_brace_()
        with self._ifnot():
            self._left_brace_()

    @graken()
    def _single_right_brace_(self):
        self._right_brace_()
        with self._ifnot():
            self._right_brace_()

    @graken()
    def _SP_(self):
        self._pattern(r'[ \t]*')

    @graken()
    def _NL_(self):
        self._pattern(r'\n')

    @graken()
    def _WS_(self):
        self._pattern(r'[ \t\n]*')

    @graken()
    def _term_(self):
        self._pattern(r'[^\[\]{}<>|:=\n]+')

    @graken()
    def _term_or_punct_(self):
        self._pattern(r'[^\[\]{}|\n]+')

    @graken()
    def _comment_(self):
        self._pattern(r'<!--(.|\n)+?-->')

    @graken()
    def _html_tag_(self):
        self._pattern(r'<[^>]+?>')

    @graken()
    def _one_line_text_(self):
        with self._choice():
            with self._option():
                self._term_or_punct_()
                self.ast['@'] = self.last_node
            with self._option():
                self._single_left_bracket_()
                self.ast['@'] = self.last_node
            with self._option():
                self._single_right_bracket_()
                self.ast['@'] = self.last_node
            with self._option():
                self._single_left_brace_()
                self.ast['@'] = self.last_node
            with self._option():
                self._single_right_brace_()
                self.ast['@'] = self.last_node
            self._error('no available options')

    @graken()
    def _one_line_text_without_templates_(self):
        self._pattern(r'[^{}\n]*')

    @graken()
    def _text_(self):
        with self._choice():
            with self._option():
                self._one_line_text_()
                self.ast['@'] = self.last_node
            with self._option():
                self._NL_()
                self.ast['@'] = self.last_node
            self._error('no available options')

    @graken()
    def _image_(self):
        with self._choice():
            with self._option():
                self._left_brackets_()
                self._WS_()
                self._token('Image:')
                self._term_()
                self.ast['filename'] = self.last_node

                def block1():
                    self._vertical_bar_()
                    self._wikitext_()
                self._closure(block1)
                self._WS_()
                self._right_brackets_()
            with self._option():
                with self._optional():
                    self._vertical_bar_()
                    with self._optional():
                        self._SP_()
                self._token('Bild')
                with self._optional():
                    self._SP_()
                    self._pattern(r'[0-9]+')
                self._equals_()
                self._term_()
                self.ast['filename'] = self.last_node
                self._vertical_bar_()
                self._wikitext_()
                with self._optional():
                    self._right_braces_()
            self._error('no available options')

        self.ast._define(
            ['filename'],
            []
        )

    @graken()
    def _template_arg_(self):
        with self._optional():
            self._term_()
            self.ast['key'] = self.last_node
            self._WS_()
            self._equals_()
        self._WS_()
        self._wikitext_()
        self.ast['value'] = self.last_node

        self.ast._define(
            ['key', 'value'],
            []
        )

    @graken()
    def _template_args_(self):

        def block0():
            self._WS_()
            self._vertical_bar_()
            self._WS_()
            self._template_arg_()
            self.ast.setlist('@', self.last_node)
        self._positive_closure(block0)

    @graken()
    def _template_args_1_(self):
        self._WS_()
        self._vertical_bar_()
        self._WS_()
        self._wikitext_()
        self.ast['value'] = self.last_node

        def block1():
            self._vertical_bar_()
            self._wikitext_()
        self._closure(block1)

        self.ast._define(
            ['value'],
            []
        )

    @graken()
    def _template_(self):
        self._left_braces_()
        self._WS_()
        self._term_()
        self.ast['name'] = self.last_node
        with self._optional():
            self._template_args_()
            self.ast['args'] = self.last_node
        self._right_braces_()

        self.ast._define(
            ['name', 'args'],
            []
        )

    @graken()
    def _text_with_links_(self):

        def block0():
            with self._choice():
                with self._option():
                    self._wiki_link_()
                with self._option():
                    self._text_()
                self._error('no available options')
        self._positive_closure(block0)

    @graken()
    def _one_line_text_with_links_(self):

        def block0():
            with self._choice():
                with self._option():
                    self._wiki_link_()
                with self._option():
                    self._one_line_text_()
                self._error('no available options')
        self._positive_closure(block0)

    @graken()
    def _one_line_wikitext_(self):

        def block0():
            with self._choice():
                with self._option():
                    self._template_()
                with self._option():
                    self._wiki_link_()
                with self._option():
                    self._external_link_()
                with self._option():
                    self._one_line_text_()
                self._error('no available options')
        self._positive_closure(block0)

    @graken()
    def _wikitext_(self):

        def block0():
            with self._choice():
                with self._option():
                    self._template_()
                with self._option():
                    self._wiki_link_()
                with self._option():
                    self._external_link_()
                with self._option():
                    self._text_()
                self._error('no available options')
        self._positive_closure(block0)

    @graken()
    def _template_NS_(self):
        self._pattern(r'\{\{[^}]+\}\}')

    @graken()
    def _template_args_NS_(self):
        self._WS_()
        self._vertical_bar_()
        self._term_()

    @graken()
    def _wiki_link_NS_(self):
        self._pattern(r'\[\[[^]]+\]\]')

    @graken()
    def _text_with_links_NS_(self):

        def block0():
            with self._choice():
                with self._option():
                    self._wiki_link_NS_()
                with self._option():
                    self._text_()
                self._error('no available options')
        self._positive_closure(block0)

    @graken()
    def _one_line_wikitext_NS_(self):

        def block0():
            with self._choice():
                with self._option():
                    self._template_NS_()
                with self._option():
                    self._one_line_text_without_templates_()
                self._error('no available options')
        self._positive_closure(block0)

    @graken()
    def _wikitext_NS_(self):

        def block0():
            with self._choice():
                with self._option():
                    self._template_NS_()
                with self._option():
                    self._wiki_link_NS_()
                with self._option():
                    self._external_link_()
                with self._option():
                    self._text_()
                self._error('no available options')
        self._positive_closure(block0)

    @graken()
    def _wiki_link_(self):
        self._left_brackets_()
        with self._optional():
            self._term_()
            self.ast['site'] = self.last_node
            self._colon_()
        self._term_()
        self.ast['target'] = self.last_node
        with self._optional():
            self._vertical_bar_()
            self._term_()
            self.ast['text'] = self.last_node
        self._right_brackets_()

        self.ast._define(
            ['site', 'target', 'text'],
            []
        )

    @graken()
    def _linktext_(self):

        def block0():
            with self._choice():
                with self._option():
                    self._term_()
                    self.ast.setlist('@', self.last_node)
                with self._option():
                    self._html_tag_()
                with self._option():
                    self._NL_()
                with self._option():
                    self._colon_()
                    self.ast.setlist('@', self.last_node)
                with self._option():
                    self._equals_()
                    self.ast.setlist('@', self.last_node)
                self._error('no available options')
        self._positive_closure(block0)

    @graken()
    def _urlpath_(self):
        self._pattern(r'[^ \[\]{}<>|]+')

    @graken()
    def _url_(self):
        self._term_()
        self.ast['schema'] = self.last_node
        self._colon_()
        self._urlpath_()
        self.ast['path'] = self.last_node

        self.ast._define(
            ['schema', 'path'],
            []
        )

    @graken()
    def _external_link_(self):
        self._left_bracket_()
        self._url_()
        self.ast['url'] = self.last_node
        self._WS_()
        with self._optional():
            self._linktext_()
            self.ast['text'] = self.last_node
        self._right_bracket_()

        self.ast._define(
            ['url', 'text'],
            []
        )

    @graken()
    def _pseudo_link_(self):
        self._pattern(r"''[^']+'':?")
        self._WS_()

    @graken()
    def _num_(self):
        self._pattern(r'[0-9][0-9]?[a-e]?')

    @graken()
    def _num_range_(self):
        self._num_()
        self.ast['range_start'] = self.last_node
        self._SP_()
        self._dash_()
        self._SP_()
        self._num_()
        self.ast['range_end'] = self.last_node

        self.ast._define(
            ['range_start', 'range_end'],
            []
        )

    @graken()
    def _sense_num_(self):
        self._num_()
        self.ast['first'] = self.last_node
        with self._optional():
            with self._choice():
                with self._option():
                    self._SP_()
                    with self._group():
                        with self._choice():
                            with self._option():
                                self._dash_()
                            with self._option():
                                self._slash_()
                            with self._option():
                                self._plus_sign_()
                            self._error('no available options')
                    self._SP_()
                    self._num_()
                    self.ast['last'] = self.last_node
                with self._option():

                    def block3():
                        self._comma_()
                        self._SP_()
                        with self._group():
                            with self._choice():
                                with self._option():
                                    self._num_()
                                    self.ast.setlist('next', self.last_node)
                                    with self._ifnot():
                                        self._dash_()
                                with self._option():
                                    self._num_range_()
                                    self.ast.setlist('next_range', self.last_node)
                                self._error('no available options')
                    self._positive_closure(block3)
                self._error('no available options')

        self.ast._define(
            ['first', 'last'],
            ['next', 'next_range']
        )

    @graken()
    def _lang_code_(self):
        self._left_braces_()
        self._pattern(r'[a-z][a-z]')
        self.ast['code'] = self.last_node
        self._right_braces_()

        self.ast._define(
            ['code'],
            []
        )

    @graken()
    def _gender_(self):
        self._left_braces_()
        self._pattern(r'[fmn]')
        self._right_braces_()

    @graken()
    def _bullet_no_links_(self):
        with self._group():
            with self._choice():
                with self._option():
                    self._bullet_()
                with self._option():
                    self._hash_char_()
                self._error('no available options')
        self._SP_()
        self._one_line_wikitext_()
        self._NL_()

    @graken()
    def _gloss_(self):
        self._left_paren_()
        with self._optional():
            self._equals_()
        self._term_()
        self._SP_()

    @graken()
    def _sense_(self):
        self._left_bracket_()
        with self._group():
            with self._choice():
                with self._option():
                    self._sense_num_()
                with self._option():
                    self._token('?')
                self._error('expecting one of: ?')
        self.ast['num'] = self.last_node
        self._right_bracket_()
        with self._optional():
            with self._choice():
                with self._option():
                    self._SP_()
                with self._option():
                    self._comma_()
                self._error('no available options')

        self.ast._define(
            ['num'],
            []
        )

    @graken()
    def _sense_no_links_(self):
        self._sense_()
        self._one_line_text_()

    @graken()
    def _sense_group_(self):

        def block0():
            with self._optional():
                self._sense_()
                self.ast['sense'] = self.last_node
            with self._optional():
                self._pseudo_link_()
            with self._optional():
                self._term_()
            with self._optional():
                self._html_tag_()
            with self._optional():
                self._left_paren_()
                with self._optional():
                    self._term_()
                    self._right_paren_()
            self._wiki_link_()
            self.ast['link'] = self.last_node
            self._SP_()
            with self._optional():
                with self._choice():
                    with self._option():
                        self._sense_()
                    with self._option():
                        self._gloss_()
                    with self._option():
                        self._gender_()
                    self._error('no available options')
            with self._optional():
                self._right_paren_()
            with self._optional():
                self._html_tag_()
            with self._optional():
                with self._choice():
                    with self._option():
                        self._comma_()
                    with self._option():
                        self._slash_()
                    with self._option():
                        self._colon_()
                    with self._option():
                        self._equals_()
                    with self._option():
                        self._dash_()
                    with self._option():
                        self._semicolon_()
                    self._error('no available options')
        self._positive_closure(block0)

        self.ast._define(
            ['sense', 'link'],
            []
        )

    @graken()
    def _link_section_(self):

        def block0():
            with self._choice():
                with self._option():
                    self._bullet_no_links_()
                with self._option():
                    with self._group():
                        self._colon_()
                        self._SP_()

                        def block1():
                            with self._choice():
                                with self._option():
                                    self._sense_group_()
                                    self.ast.setlist('group', self.last_node)
                                with self._option():
                                    self._sense_no_links_()
                                    with self._optional():
                                        with self._group():
                                            with self._choice():
                                                with self._option():
                                                    self._semicolon_()
                                                    self._SP_()
                                                with self._option():
                                                    self._term_()
                                                self._error('no available options')
                                self._error('no available options')
                        self._closure(block1)
                        self._NL_()
                self._error('no available options')
        self._positive_closure(block0)

        self.ast._define(
            [],
            ['group']
        )

    @graken()
    def _synonym_section_(self):
        self._link_section_()
        self.ast['links'] = self.last_node

        self.ast._define(
            ['links'],
            []
        )

    @graken()
    def _to_german_(self):
        with self._optional():
            self._colon_()
        self._left_braces_()
        self._token('Übersetzungen umleiten')
        self._vertical_bar_()
        self._sense_num_()
        self.ast['sense'] = self.last_node
        self._vertical_bar_()
        self._text_()
        self.ast['target'] = self.last_node
        with self._optional():
            self._vertical_bar_()
            with self._optional():
                self._sense_num_()
                self.ast['target_sense'] = self.last_node
        self._right_braces_()
        with self._optional():
            self._SP_()
            self._gender_()
        self._WS_()

        self.ast._define(
            ['sense', 'target', 'target_sense'],
            []
        )

    @graken()
    def _tr_base_(self):
        with self._optional():
            self._left_bracket_()
            self._sense_num_()
            self.ast['num'] = self.last_node
            self._right_bracket_()
            self._SP_()
        self._left_braces_()
        self._pattern(r'Ü[x]*')
        self._vertical_bar_()
        self._text_()
        self._vertical_bar_()
        with self._optional():
            self._term_()
            self.ast['target'] = self.last_node
            with self._optional():
                self._vertical_bar_()
                self._term_()
                self.ast['original'] = self.last_node
        self._right_braces_()
        with self._optional():
            self._SP_()
            self._gender_()
        with self._optional():
            with self._group():
                with self._choice():
                    with self._option():
                        self._comma_()
                    with self._option():
                        self._semicolon_()
                    self._error('no available options')
            self._SP_()

        self.ast._define(
            ['num', 'target', 'original'],
            []
        )

    @graken()
    def _from_german_(self):
        self._bullet_()
        self._left_braces_()
        self._pattern(r'[a-z][a-z]')
        self.ast['code'] = self.last_node
        self._right_braces_()

        self._colon_()
        self._SP_()

        def block2():
            self._tr_base_()
        self._positive_closure(block2)

        self.ast['tr'] = self.last_node
        self._WS_()

        self.ast._define(
            ['code', 'tr'],
            []
        )

    @graken()
    def _reference_(self):
        self._colon_()
        self._left_bracket_()
        self._sense_num_()
        self._right_bracket_()
        self._SP_()
        self._wikitext_()
        self._WS_()

    @graken()
    def _table_filler_(self):
        with self._group():
            with self._choice():
                with self._option():
                    self._token('{{Ü-Tabelle|Ü-links=')
                with self._option():
                    self._token('|Ü-rechts=')
                self._error('expecting one of: {{Ü-Tabelle|Ü-links= |Ü-rechts=')
        self._WS_()

    @graken()
    def _translation_section_(self):

        def block1():
            with self._choice():
                with self._option():
                    self._to_german_()
                with self._option():
                    self._from_german_()
                with self._option():
                    self._table_filler_()
                with self._option():
                    self._reference_()
                self._error('no available options')
        self._positive_closure(block1)

        self.ast['links'] = self.last_node
        with self._optional():
            self._right_braces_()

        self.ast._define(
            ['links'],
            []
        )

    @graken()
    def _line_(self):
        self._colon_()
        with self._optional():
            self._colon_()
        self._SP_()
        with self._optional():
            self._left_bracket_()
        with self._group():
            with self._choice():
                with self._option():
                    self._dash_()
                with self._option():
                    self._pattern(r'[0-9a-e]+')
                self._error('expecting one of: [0-9a-e]+')
        self.ast['num'] = self.last_node
        with self._optional():
            self._right_bracket_()
        with self._optional():
            self._SP_()
        with self._optional():
            self._template_()
        with self._optional():
            self._pseudo_link_()
        with self._group():
            with self._choice():
                with self._option():
                    self._one_line_wikitext_()
                    self.ast['sense'] = self.last_node
                    with self._optional():
                        self._SP_()
                        self._template_()
                with self._option():
                    self._text_()
                self._error('no available options')
        self._NL_()

        self.ast._define(
            ['num', 'sense'],
            []
        )

    @graken()
    def _definition_section_(self):

        def block0():
            with self._choice():
                with self._option():
                    with self._group():
                        self._bullet_()
                        self._pseudo_link_()
                with self._option():
                    self._line_()
                self._error('no available options')
        self._positive_closure(block0)


class de_wiktionarySemantics(object):
    def left_bracket(self, ast):
        return ast

    def right_bracket(self, ast):
        return ast

    def left_brace(self, ast):
        return ast

    def right_brace(self, ast):
        return ast

    def left_brackets(self, ast):
        return ast

    def right_brackets(self, ast):
        return ast

    def left_braces(self, ast):
        return ast

    def right_braces(self, ast):
        return ast

    def left_paren(self, ast):
        return ast

    def right_paren(self, ast):
        return ast

    def hash_char(self, ast):
        return ast

    def vertical_bar(self, ast):
        return ast

    def equals(self, ast):
        return ast

    def bullet(self, ast):
        return ast

    def colon(self, ast):
        return ast

    def comma(self, ast):
        return ast

    def semicolon(self, ast):
        return ast

    def slash(self, ast):
        return ast

    def dash(self, ast):
        return ast

    def plus_sign(self, ast):
        return ast

    def single_left_bracket(self, ast):
        return ast

    def single_right_bracket(self, ast):
        return ast

    def single_left_brace(self, ast):
        return ast

    def single_right_brace(self, ast):
        return ast

    def SP(self, ast):
        return ast

    def NL(self, ast):
        return ast

    def WS(self, ast):
        return ast

    def term(self, ast):
        return ast

    def term_or_punct(self, ast):
        return ast

    def comment(self, ast):
        return ast

    def html_tag(self, ast):
        return ast

    def one_line_text(self, ast):
        return ast

    def one_line_text_without_templates(self, ast):
        return ast

    def text(self, ast):
        return ast

    def image(self, ast):
        return ast

    def template_arg(self, ast):
        return ast

    def template_args(self, ast):
        return ast

    def template_args_1(self, ast):
        return ast

    def template(self, ast):
        return ast

    def text_with_links(self, ast):
        return ast

    def one_line_text_with_links(self, ast):
        return ast

    def one_line_wikitext(self, ast):
        return ast

    def wikitext(self, ast):
        return ast

    def template_NS(self, ast):
        return ast

    def template_args_NS(self, ast):
        return ast

    def wiki_link_NS(self, ast):
        return ast

    def text_with_links_NS(self, ast):
        return ast

    def one_line_wikitext_NS(self, ast):
        return ast

    def wikitext_NS(self, ast):
        return ast

    def wiki_link(self, ast):
        return ast

    def linktext(self, ast):
        return ast

    def urlpath(self, ast):
        return ast

    def url(self, ast):
        return ast

    def external_link(self, ast):
        return ast

    def pseudo_link(self, ast):
        return ast

    def num(self, ast):
        return ast

    def num_range(self, ast):
        return ast

    def sense_num(self, ast):
        return ast

    def lang_code(self, ast):
        return ast

    def gender(self, ast):
        return ast

    def bullet_no_links(self, ast):
        return ast

    def gloss(self, ast):
        return ast

    def sense(self, ast):
        return ast

    def sense_no_links(self, ast):
        return ast

    def sense_group(self, ast):
        return ast

    def link_section(self, ast):
        return ast

    def synonym_section(self, ast):
        return ast

    def to_german(self, ast):
        return ast

    def tr_base(self, ast):
        return ast

    def from_german(self, ast):
        return ast

    def reference(self, ast):
        return ast

    def table_filler(self, ast):
        return ast

    def translation_section(self, ast):
        return ast

    def line(self, ast):
        return ast

    def definition_section(self, ast):
        return ast


def main(filename, startrule, trace=False, whitespace=None):
    import json
    with open(filename) as f:
        text = f.read()
    parser = de_wiktionaryParser(parseinfo=False)
    ast = parser.parse(
        text,
        startrule,
        filename=filename,
        trace=trace,
        whitespace=whitespace)
    print('AST:')
    print(ast)
    print()
    print('JSON:')
    print(json.dumps(ast, indent=2))
    print()

if __name__ == '__main__':
    import argparse
    import string
    import sys

    class ListRules(argparse.Action):
        def __call__(self, parser, namespace, values, option_string):
            print('Rules:')
            for r in de_wiktionaryParser.rule_list():
                print(r)
            print()
            sys.exit(0)

    parser = argparse.ArgumentParser(description="Simple parser for de_wiktionary.")
    parser.add_argument('-l', '--list', action=ListRules, nargs=0,
                        help="list all rules and exit")
    parser.add_argument('-t', '--trace', action='store_true',
                        help="output trace information")
    parser.add_argument('-w', '--whitespace', type=str, default=string.whitespace,
                        help="whitespace specification")
    parser.add_argument('file', metavar="FILE", help="the input file to parse")
    parser.add_argument('startrule', metavar="STARTRULE",
                        help="the start rule for parsing")
    args = parser.parse_args()

    main(
        args.file,
        args.startrule,
        trace=args.trace,
        whitespace=args.whitespace
    )
