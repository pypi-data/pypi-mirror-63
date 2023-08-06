import re
from .translators import TokenType, Rule


class Grammar(object):

    def __init__(self, case_sensitive=True, wspace=[" ", "\t", "\r", "\n"]):
        self._wspace_chars = wspace
        self._comment_delims = []
        self._string_delims = []
        self._patterns = []
        self._case_sensitive = case_sensitive
        self._set_wspace_chars(wspace)
        self._rules = {}
        self._root_rule = ""
        self._transformations = {}
        self._multiple_types_per_token = True
        
    def get_whitespace_chars(self):
        return self._wspace_chars
    
    def add_comment(self, start, end, nestable=False):
        self._comment_delims.append((start, end, nestable))
        return self
        
    def get_comments(self):
        return self._comment_delims
    
    def add_string(self, start, end, escape="\\", name="STRING"):
        self._string_delims.append((name, start, end, escape))
        return self
        
    def get_strings(self):
        return self._string_delims   
    
    def get_token_patterns(self):
        return self._patterns

    def enable_multiple_types_per_token(self, enable=True):
        self._multiple_types_per_token = enable

    def multiple_types_per_token_enabled(self):
        return self._multiple_types_per_token

    def _set_wspace_chars(self, chars):
        self._wspace_pattern = "[" + "".join(chars) + "]"

    def add_token(self, name, pattern):
        self._patterns.append((name, re.compile("^(" + pattern + ")")))
        return self

    def add_keyword(self, keyword, name=""):
        name_ = name or keyword.upper()
        if self._case_sensitive:
            kw = keyword
        else:
            kw = ""
            for ch in keyword:
                kw += "({}|{})".format(ch.lower(), ch.upper())
        pattern = "^(" + kw + ")(?:" + self._wspace_pattern + "|\Z)"
        self._patterns.insert(0, (name_, re.compile(pattern)))
        return self

    def _regex_escape(self, s):
        ret = ""
        for ch in s:
            if ch in ["*", "+", "?", "\\", "(", ")", "|"]:
                ret += "\\"
            ret += ch
        return ret

    def _not_pattern(self, s):
        ret = ""
        left = ""
        right = s
        while right:
            if left:
                ret += "|({}[^{}]?)".format(self._regex_escape(left), right[0])
            else:
                ret += "[^{}]".format(right[0])
            left += right[0]
            right = right[1:]
        return ret

    def rule(self, name, translator, is_root=False):
        self._rules[name] = translator
        if is_root:
            self._root_rule = name

    def get_rule(self, name):
        return self._rules[name]

    def get_root_rule(self):
        return self._root_rule

    def ast_transform(self, rule_name):
        return _AstTransformation(self, rule_name)

    def set_ast_transform(self, rule_name, transform_fn):
        self._transformations[rule_name] = transform_fn

    def get_ast_transform(self, rule_name):
        if rule_name in self._transformations:
            return self._transformations[rule_name]
        else:
            return None

    def __getattr__(self, name):
        for token_type, _ in self._patterns:
            if name == token_type:
                return TokenTypeMaker(name)
        for string_name, _, _, _ in self._string_delims:
            if name == string_name:
                return TokenTypeMaker(name)
        return RuleMaker(name)

class RuleMaker(object):

    def __init__(self, name):
        self._name = name

    def __call__(self, id=""):
        return Rule(self._name, id)

class TokenTypeMaker(object):

    def __init__(self, name):
        self._name = name

    def __call__(self, id=""):
        return TokenType(self._name, id)

class _AstTransformation(object):

    def __init__(self, grammar, rule_name):
        self._grammar = grammar
        self._rule_name = rule_name

    def __call__(self, transform_fn):
        self._grammar.set_ast_transform(self._rule_name, transform_fn)
        return transform_fn
