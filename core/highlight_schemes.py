#!venv/bin/python3
"""Cobra OSS OSINT Tool

BSD 3-Clause License

Copyright (c) 2024, Alexeev Bronislav

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its
   contributors may be used to endorse or promote products derived from
   this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

from pygments.style import Style
from pygments.token import (
	Text, Name, Error, Other, String, Number, Keyword, Generic, Literal,
	Comment, Operator, Whitespace, Punctuation)


class CatppuccinMocha(Style):
	BASE03 = '#1e1e2e'
	BASE02 = '#45475a'
	BASE01 = '#6c7086'
	BASE00 = "#9399b2"
	BASE0 = '#a6adc8'
	BASE1 = '#bac2de'
	BASE2 = '#bac2de'
	BASE3 = '#cdd6f4'
	YELLOW  = '#f9e2af'
	ORANGE  = '#fab387'
	RED     = '#f38ba8'
	MAGENTA = '#cba6f7'
	VIOLET  = '#f5c2e7'
	BLUE    = '#89b4fa'
	CYAN    = '#94e2d5'
	GREEN   = '#a6e3a1'

	styles = {
		Text:                   BASE0,
		Whitespace:             BASE03,
		Error:                  RED,
		Other:                  BASE0,

		Name:                   BASE1,
		Name.Attribute:         BASE0,
		Name.Builtin:           BLUE,
		Name.Builtin.Pseudo:    BLUE,
		Name.Class:             BLUE,
		Name.Constant:          YELLOW,
		Name.Decorator:         MAGENTA,
		Name.Entity:            YELLOW,
		Name.Exception:         RED,
		Name.Function:          BLUE,
		Name.Property:          BLUE,
		Name.Label:             BASE0,
		Name.Namespace:         MAGENTA,
		Name.Other:             BASE0,
		Name.Tag:               MAGENTA,
		Name.Variable:          ORANGE,
		Name.Variable.Class:    BLUE,
		Name.Variable.Global:   BLUE,
		Name.Variable.Instance: BLUE,

		String:                 GREEN,
		String.Backtick:        GREEN,
		String.Char:            CYAN,
		String.Doc:             GREEN,
		String.Double:          GREEN,
		String.Escape:          ORANGE,
		String.Heredoc:         GREEN,
		String.Interpol:        ORANGE,
		String.Other:           GREEN,
		String.Regex:           CYAN,
		String.Single:          GREEN,
		String.Symbol:          GREEN,

		Number:                 MAGENTA,
		Number.Float:           MAGENTA,
		Number.Hex:             VIOLET,
		Number.Integer:         MAGENTA,
		Number.Integer.Long:    VIOLET,
		Number.Oct:             VIOLET,

		Keyword:                CYAN,
		Keyword.Constant:       YELLOW,
		Keyword.Declaration:    CYAN,
		Keyword.Namespace:      ORANGE,
		Keyword.Pseudo:         ORANGE,
		Keyword.Reserved:       VIOLET,
		Keyword.Type:           ORANGE,

		Generic:                BASE0,
		Generic.Deleted:        BASE0,
		Generic.Emph:           BASE0,
		Generic.Error:          BASE0,
		Generic.Heading:        BASE0,
		Generic.Inserted:       BASE0,
		Generic.Output:         BASE0,
		Generic.Prompt:         BASE0,
		Generic.Strong:         BASE0,
		Generic.Subheading:     BASE0,
		Generic.Traceback:      BASE0,

		Literal:                BASE0,
		Literal.Date:           BASE0,

		Comment:                BASE01,
		Comment.Multiline:      BASE01,
		Comment.Preproc:        BASE01,
		Comment.Single:         BASE01,
		Comment.Special:        BASE01,

		Operator:               BASE0,
		Operator.Word:          GREEN,

		Punctuation:            BASE0,
	}


class SolarizedDark(Style):
	BASE03  = '#002b36' # noqa
	BASE02  = '#073642' # noqa
	BASE01  = '#586e75' # noqa
	BASE00  = '#657b83' # noqa
	BASE0   = '#839496' # noqa
	BASE1   = '#93a1a1' # noqa
	BASE2   = '#eee8d5' # noqa
	BASE3   = '#fdf6e3' # noqa
	YELLOW  = '#b58900' # noqa
	ORANGE  = '#cb4b16' # noqa
	RED     = '#dc322f' # noqa
	MAGENTA = '#d33682' # noqa
	VIOLET  = '#6c71c4' # noqa
	BLUE    = '#268bd2' # noqa
	CYAN    = '#2aa198' # noqa
	GREEN   = '#859900' # noqa

	styles = {
		Text:                   BASE0,
		Whitespace:             BASE03,
		Error:                  RED,
		Other:                  BASE0,

		Name:                   BASE1,
		Name.Attribute:         BASE0,
		Name.Builtin:           BLUE,
		Name.Builtin.Pseudo:    BLUE,
		Name.Class:             BLUE,
		Name.Constant:          YELLOW,
		Name.Decorator:         ORANGE,
		Name.Entity:            ORANGE,
		Name.Exception:         ORANGE,
		Name.Function:          BLUE,
		Name.Property:          BLUE,
		Name.Label:             BASE0,
		Name.Namespace:         YELLOW,
		Name.Other:             BASE0,
		Name.Tag:               GREEN,
		Name.Variable:          ORANGE,
		Name.Variable.Class:    BLUE,
		Name.Variable.Global:   BLUE,
		Name.Variable.Instance: BLUE,

		String:                 CYAN,
		String.Backtick:        CYAN,
		String.Char:            CYAN,
		String.Doc:             CYAN,
		String.Double:          CYAN,
		String.Escape:          ORANGE,
		String.Heredoc:         CYAN,
		String.Interpol:        ORANGE,
		String.Other:           CYAN,
		String.Regex:           CYAN,
		String.Single:          CYAN,
		String.Symbol:          CYAN,

		Number:                 CYAN,
		Number.Float:           CYAN,
		Number.Hex:             CYAN,
		Number.Integer:         CYAN,
		Number.Integer.Long:    CYAN,
		Number.Oct:             CYAN,

		Keyword:                GREEN,
		Keyword.Constant:       GREEN,
		Keyword.Declaration:    GREEN,
		Keyword.Namespace:      ORANGE,
		Keyword.Pseudo:         ORANGE,
		Keyword.Reserved:       GREEN,
		Keyword.Type:           GREEN,

		Generic:                BASE0,
		Generic.Deleted:        BASE0,
		Generic.Emph:           BASE0,
		Generic.Error:          BASE0,
		Generic.Heading:        BASE0,
		Generic.Inserted:       BASE0,
		Generic.Output:         BASE0,
		Generic.Prompt:         BASE0,
		Generic.Strong:         BASE0,
		Generic.Subheading:     BASE0,
		Generic.Traceback:      BASE0,

		Literal:                BASE0,
		Literal.Date:           BASE0,

		Comment:                BASE01,
		Comment.Multiline:      BASE01,
		Comment.Preproc:        BASE01,
		Comment.Single:         BASE01,
		Comment.Special:        BASE01,

		Operator:               BASE0,
		Operator.Word:          GREEN,

		Punctuation:            BASE0,
	}


class GruvboxDark(Style):
	BASE03  = '#1d2021' # noqa
	BASE02  = '#282828' # noqa
	BASE01  = '#3c3836' # noqa
	BASE00  = '#4c4846' # noqa
	BASE0   = '#ebdbb2' # noqa
	BASE1   = '#ebdbb2' # noqa
	BASE2   = '#ebbdb2' # noqa
	BASE3   = '#ebdbb2' # noqa
	YELLOW  = '#fabd2f' # noqa
	ORANGE  = '#fabd2f' # noqa
	RED     = '#FB4934' # noqa
	MAGENTA = '#d3869b' # noqa
	VIOLET  = '#d3869b' # noqa
	BLUE    = '#83a598' # noqa
	CYAN    = '#8ec07c' # noqa
	GREEN   = '#b8bb26' # noqa

	styles = {
		Text:                   BASE0,
		Whitespace:             BASE03,
		Error:                  RED,
		Other:                  BASE0,

		Name:                   BASE1,
		Name.Attribute:         BASE0,
		Name.Builtin:           BLUE,
		Name.Builtin.Pseudo:    BLUE,
		Name.Class:             BLUE,
		Name.Constant:          YELLOW,
		Name.Decorator:         ORANGE,
		Name.Entity:            ORANGE,
		Name.Exception:         ORANGE,
		Name.Function:          BLUE,
		Name.Property:          BLUE,
		Name.Label:             BASE0,
		Name.Namespace:         YELLOW,
		Name.Other:             BASE0,
		Name.Tag:               GREEN,
		Name.Variable:          ORANGE,
		Name.Variable.Class:    BLUE,
		Name.Variable.Global:   BLUE,
		Name.Variable.Instance: BLUE,

		String:                 CYAN,
		String.Backtick:        CYAN,
		String.Char:            CYAN,
		String.Doc:             CYAN,
		String.Double:          CYAN,
		String.Escape:          ORANGE,
		String.Heredoc:         CYAN,
		String.Interpol:        ORANGE,
		String.Other:           CYAN,
		String.Regex:           CYAN,
		String.Single:          CYAN,
		String.Symbol:          CYAN,

		Number:                 CYAN,
		Number.Float:           CYAN,
		Number.Hex:             CYAN,
		Number.Integer:         CYAN,
		Number.Integer.Long:    CYAN,
		Number.Oct:             CYAN,

		Keyword:                GREEN,
		Keyword.Constant:       GREEN,
		Keyword.Declaration:    GREEN,
		Keyword.Namespace:      ORANGE,
		Keyword.Pseudo:         ORANGE,
		Keyword.Reserved:       GREEN,
		Keyword.Type:           GREEN,

		Generic:                BASE0,
		Generic.Deleted:        BASE0,
		Generic.Emph:           BASE0,
		Generic.Error:          BASE0,
		Generic.Heading:        BASE0,
		Generic.Inserted:       BASE0,
		Generic.Output:         BASE0,
		Generic.Prompt:         BASE0,
		Generic.Strong:         BASE0,
		Generic.Subheading:     BASE0,
		Generic.Traceback:      BASE0,

		Literal:                BASE0,
		Literal.Date:           BASE0,

		Comment:                BASE01,
		Comment.Multiline:      BASE01,
		Comment.Preproc:        BASE01,
		Comment.Single:         BASE01,
		Comment.Special:        BASE01,

		Operator:               BASE0,
		Operator.Word:          GREEN,

		Punctuation:            BASE0,
	}
