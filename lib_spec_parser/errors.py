"""lib-spec-parser exception types.

Traces: LIB-FR-01, LIB-FR-06 (fail-fast contract)
"""

from __future__ import annotations


class ParseError(Exception):
    """Spec ファイル parse 失敗を示す例外。

    US-L-06 fail-fast 契約: partial output を返さず本例外で即失敗を伝達する。
    """

    pass
