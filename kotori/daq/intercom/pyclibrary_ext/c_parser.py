# -*- coding: utf-8 -*-
from pyclibrary.c_parser import CParser
from pyclibrary.thirdparty.pyparsing import (Forward, Optional, Keyword, Literal, ZeroOrMore, OneOrMore, Group, nestedExpr, delimitedList, Suppress)

# taken verbatim from pyclibrary.c_parser
# 2015-11-07 make pyclibrary grok more constructor flavours

class CParserEnhanced(CParser):

    def build_parser(self):
        """Builds the entire tree of parser elements for the C language (the
        bits we support, anyway).
        """

        from pyclibrary.c_parser import \
            fund_type, kwl, size_modifiers, sign_modifiers, extra_modifier, recombine, type_qualifier, ident, \
            lparen, rparen, expression, colon, semi, integer, storage_class_spec, rbrace, lbrace, number, comma, \
            lbrack, rbrack, call_conv

        if hasattr(self, 'parser'):
            return self.parser

        self.struct_type = Forward()
        self.enum_type = Forward()
        type_ = (fund_type |
                 Optional(kwl(size_modifiers + sign_modifiers)) + ident |
                 self.struct_type |
                 self.enum_type)
        if extra_modifier is not None:
            type_ += extra_modifier
        type_.setParseAction(recombine)
        self.type_spec = (type_qualifier('pre_qual') +
                          type_("name"))

        # --- Abstract declarators for use in function pointer arguments
        #   Thus begins the extremely hairy business of parsing C declarators.
        #   Whomever decided this was a reasonable syntax should probably never
        #   breed.
        #   The following parsers combined with the process_declarator function
        #   allow us to turn a nest of type modifiers into a correctly
        #   ordered list of modifiers.

        self.declarator = Forward()
        self.abstract_declarator = Forward()

        #  Abstract declarators look like:
        #     <empty string>
        #     *
        #     **[num]
        #     (*)(int, int)
        #     *( )(int, int)[10]
        #     ...etc...
        self.abstract_declarator << Group(
            type_qualifier('first_typequal') +
            Group(ZeroOrMore(Group(Suppress('*') + type_qualifier)))('ptrs') +
            ((Optional('&')('ref')) |
             (lparen + self.abstract_declarator + rparen)('center')) +
            Optional(lparen +
                     Optional(delimitedList(Group(
                         self.type_spec('type') +
                         self.abstract_declarator('decl') +
                         Optional(Literal('=').suppress() + expression,
                             default=None)('val')
                     )), default=None) +
                     rparen)('args') +
            Group(ZeroOrMore(lbrack + Optional(expression, default='-1') +
                             rbrack))('arrays')
        )

        # Declarators look like:
        #     varName
        #     *varName
        #     **varName[num]
        #     (*fnName)(int, int)
        #     * fnName(int arg1=0)[10]
        #     ...etc...
        self.declarator << Group(
            type_qualifier('first_typequal') + call_conv +
            Group(ZeroOrMore(Group(Suppress('*') + type_qualifier)))('ptrs') +
            ((Optional('&')('ref') + ident('name')) |
             (lparen + self.declarator + rparen)('center')) +
            Optional(lparen +
                     Optional(delimitedList(
                         Group(self.type_spec('type') +
                               (self.declarator |
                                self.abstract_declarator)('decl') +
                               Optional(Literal('=').suppress() +
                                        expression, default=None)('val')
                         )),
                         default=None) +
                     rparen)('args') +
            Group(ZeroOrMore(lbrack + Optional(expression, default='-1') +
                             rbrack))('arrays')
        )
        self.declarator_list = Group(delimitedList(self.declarator))

        # Typedef
        self.type_decl = (Keyword('typedef') + self.type_spec('type') +
                          self.declarator_list('decl_list') + semi)
        self.type_decl.setParseAction(self.process_typedef)

        # Variable declaration
        self.variable_decl = (
            Group(storage_class_spec +
                  self.type_spec('type') +
                  Optional(self.declarator_list('decl_list')) +
                  Optional(Literal('=').suppress() +
                           (expression('value') |
                            (lbrace +
                             Group(delimitedList(expression))('array_values') +
                             rbrace
                                )
                               )
                  )
            ) +
            semi)
        self.variable_decl.setParseAction(self.process_variable)

        # Function definition
        self.typeless_function_decl = (self.declarator('decl') +
                                       nestedExpr('{', '}').suppress())
        self.function_decl = (storage_class_spec +
                              self.type_spec('type') +
                              self.declarator('decl') +
                              nestedExpr('{', '}').suppress())
        self.function_decl.setParseAction(self.process_function)

        # Struct definition
        self.struct_decl = Forward()
        struct_kw = (Keyword('struct') | Keyword('union'))
        self.struct_member = (
            Group(self.variable_decl.copy().setParseAction(lambda: None)) |
            # Hack to handle bit width specification.
            Group(Group(self.type_spec('type') +
                        Optional(self.declarator_list('decl_list')) +
                        colon + integer('bit') + semi)) |
            (self.type_spec + self.declarator +
             nestedExpr('{', '}')).suppress() |
            (self.declarator + nestedExpr('{', '}')).suppress()
            # 2015-11-07 make pyclibrary grok more constructor flavours::
            #
            #    struct_program()
            #    : length(13), ID(0)
            #    {}
            | (self.declarator + ':' + OneOrMore(ident + '(' + OneOrMore(number) + ')' + Optional(',')) + nestedExpr('{', '}')).suppress()
            )

        self.decl_list = (lbrace +
                          Group(OneOrMore(self.struct_member))('members') +
                          rbrace)
        self.struct_type << (struct_kw('struct_type') +
                             ((Optional(ident)('name') +
                               self.decl_list) | ident('name'))
            )
        self.struct_type.setParseAction(self.process_struct)

        self.struct_decl = self.struct_type + semi

        # Enum definition
        enum_var_decl = Group(ident('name') +
                              Optional(Literal('=').suppress() +
                                       (integer('value') | ident('valueName'))))

        self.enum_type << (Keyword('enum') +
                           (Optional(ident)('name') +
                            lbrace +
                            Group(delimitedList(enum_var_decl))('members') +
                            Optional(comma) + rbrace | ident('name'))
            )
        self.enum_type.setParseAction(self.process_enum)
        self.enum_decl = self.enum_type + semi

        self.parser = (self.type_decl | self.variable_decl |
                       self.function_decl)
        return self.parser
