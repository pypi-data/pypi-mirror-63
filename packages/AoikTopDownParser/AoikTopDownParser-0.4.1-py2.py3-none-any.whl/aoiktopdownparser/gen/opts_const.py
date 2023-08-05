# coding: utf-8
from __future__ import absolute_import


# `GS` below means parser generator's setting key.

# Whether enable backtracking
GS_BACKTRACKING_ON = 'GS_BACKTRACKING_ON'

# Rule functions' name prefix
GS_RULE_FUNC_NAME_PRF = 'GS_RULE_FUNC_NAME_PRF'

GS_RULE_FUNC_NAME_PRF_V_DFT = ''

# Rule functions' name postfix
GS_RULE_FUNC_NAME_POF = 'GS_RULE_FUNC_NAME_POF'

GS_RULE_FUNC_NAME_POF_V_DFT = ''

# Prefix before embedded code
GS_CODE_PRF = 'GS_CODE_PRF'

GS_CODE_PRF_V_DFT = '# ```\n'

# Postfix after embedded code
GS_CODE_POF = 'GS_CODE_POF'

GS_CODE_POF_V_DFT = '\n# ```'

# `SS` below means parser template's substitution setting key.
#
# What substitution settings are effective is determined by the parser template
# in use. Settings below are effective for the default template, i.e.
# `aoiktopdownparser.gen.parser_tplt.py`. You are not limited to these
# settings if a custom parser template is used.

# What prefix a setting key must have to be a substitution setting key.
# Do not change this.
SS_PRF = 'SS_'

# Substitution settings below are internal. Do not specify values for them.
# ----- BEG -----

# First set mapping.
SS_RULE_FIRST_SET_MAPPING = 'SS_RULE_FIRST_SET_MAPPING'

# Follow set mapping.
SS_RULE_FOLLOW_SET_MAPPING = 'SS_RULE_FOLLOW_SET_MAPPING'

# Rule RE objects
SS_RULE_REOS = 'SS_RULE_REOS'

# Rule functions' generated code
SS_RULE_FUNCS = 'SS_RULE_FUNCS'

# Rule functions' name prefix
SS_RULE_FUNC_NAME_PRF = 'SS_RULE_FUNC_NAME_PRF'

# Rule functions' name postfix
SS_RULE_FUNC_NAME_POF = 'SS_RULE_FUNC_NAME_POF'

# Functions for supporting backtracking
SS_BACKTRACKING_FUNCS = 'SS_BACKTRACKING_FUNCS'

# ----- END -----

# Substitution settings below can be specified.

# Entry rule name.
# Default is using the first rule.
SS_ENTRY_RULE = 'SS_ENTRY_RULE'
