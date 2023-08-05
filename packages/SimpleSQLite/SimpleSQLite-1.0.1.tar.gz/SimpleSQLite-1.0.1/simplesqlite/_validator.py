import re

from pathvalidate import unprintable_ascii_chars
from pathvalidate.error import (
    InvalidCharError,
    InvalidReservedNameError,
    NullNameError,
    ValidReservedNameError,
)


__SQLITE_VALID_RESERVED_KEYWORDS = [
    "ABORT",
    "ACTION",
    "AFTER",
    "ANALYZE",
    "ASC",
    "ATTACH",
    "BEFORE",
    "BEGIN",
    "BY",
    "CASCADE",
    "CAST",
    "COLUMN",
    "CONFLICT",
    "CROSS",
    "CURRENT_DATE",
    "CURRENT_TIME",
    "CURRENT_TIMESTAMP",
    "DATABASE",
    "DEFERRED",
    "DESC",
    "DETACH",
    "EACH",
    "END",
    "EXCLUSIVE",
    "EXPLAIN",
    "FAIL",
    "FOR",
    "FULL",
    "GLOB",
    "IGNORE",
    "IMMEDIATE",
    "INDEXED",
    "INITIALLY",
    "INNER",
    "INSTEAD",
    "KEY",
    "LEFT",
    "LIKE",
    "MATCH",
    "NATURAL",
    "NO",
    "OF",
    "OFFSET",
    "OUTER",
    "PLAN",
    "PRAGMA",
    "QUERY",
    "RAISE",
    "RECURSIVE",
    "REGEXP",
    "REINDEX",
    "RELEASE",
    "RENAME",
    "REPLACE",
    "RESTRICT",
    "RIGHT",
    "ROLLBACK",
    "ROW",
    "SAVEPOINT",
    "TEMP",
    "TEMPORARY",
    "TRIGGER",
    "VACUUM",
    "VIEW",
    "VIRTUAL",
    "WITH",
    "WITHOUT",
]
__SQLITE_INVALID_RESERVED_KEYWORDS = [
    "ADD",
    "ALL",
    "ALTER",
    "AND",
    "AS",
    "AUTOINCREMENT",
    "BETWEEN",
    "CASE",
    "CHECK",
    "COLLATE",
    "COMMIT",
    "CONSTRAINT",
    "CREATE",
    "DEFAULT",
    "DEFERRABLE",
    "DELETE",
    "DISTINCT",
    "DROP",
    "ELSE",
    "ESCAPE",
    "EXCEPT",
    "EXISTS",
    "FOREIGN",
    "FROM",
    "GROUP",
    "HAVING",
    "IN",
    "INDEX",
    "INSERT",
    "INTERSECT",
    "INTO",
    "IS",
    "ISNULL",
    "JOIN",
    "LIMIT",
    "NOT",
    "NOTNULL",
    "NULL",
    "ON",
    "OR",
    "ORDER",
    "PRIMARY",
    "REFERENCES",
    "SELECT",
    "SET",
    "TABLE",
    "THEN",
    "TO",
    "TRANSACTION",
    "UNION",
    "UNIQUE",
    "UPDATE",
    "USING",
    "VALUES",
    "WHEN",
    "WHERE",
]

__SQLITE_VALID_RESERVED_KEYWORDS_TABLE = __SQLITE_VALID_RESERVED_KEYWORDS
__SQLITE_INVALID_RESERVED_KEYWORDS_TABLE = __SQLITE_INVALID_RESERVED_KEYWORDS + ["IF"]

__SQLITE_VALID_RESERVED_KEYWORDS_ATTR = __SQLITE_VALID_RESERVED_KEYWORDS + ["IF"]
__SQLITE_INVALID_RESERVED_KEYWORDS_ATTR = __SQLITE_INVALID_RESERVED_KEYWORDS

__RE_INVALID_CHARS = re.compile(
    "[{:s}]".format(re.escape("".join(unprintable_ascii_chars))), re.UNICODE
)


def validate_sqlite_table_name(name: str) -> None:
    """
    :param str name: Name to validate.
    :raises pathvalidate.InvalidCharError:
        If the ``name`` includes unprintable character(s).
    :raises pathvalidate.InvalidReservedNameError:
        |raises_sqlite_keywords|
        And invalid as a table name.
    :raises pathvalidate.ValidReservedNameError:
        |raises_sqlite_keywords|
        However, valid as a table name.
    """

    if not name:
        raise NullNameError("null name")

    if __RE_INVALID_CHARS.search(name):
        raise InvalidCharError("unprintable character found")

    name = name.upper()

    if name in __SQLITE_INVALID_RESERVED_KEYWORDS_TABLE:
        raise InvalidReservedNameError("'{:s}' is a reserved keyword by sqlite".format(name))

    if name in __SQLITE_VALID_RESERVED_KEYWORDS_TABLE:
        raise ValidReservedNameError("'{:s}' is a reserved keyword by sqlite".format(name))


def validate_sqlite_attr_name(name: str) -> None:
    """
    :param str name: Name to validate.
    :raises pathvalidate.InvalidCharError:
        If the ``name`` includes unprintable character(s).
    :raises pathvalidate.InvalidReservedNameError:
        |raises_sqlite_keywords|
        And invalid as an attribute name.
    :raises pathvalidate.ValidReservedNameError:
        |raises_sqlite_keywords|
        However, valid as an attribute name.
    """

    if not name:
        raise NullNameError("null name")

    if __RE_INVALID_CHARS.search(name):
        raise InvalidCharError("unprintable character found")

    name = name.upper()

    if name in __SQLITE_INVALID_RESERVED_KEYWORDS_ATTR:
        raise InvalidReservedNameError("'{}' is a reserved keyword by sqlite".format(name))

    if name in __SQLITE_VALID_RESERVED_KEYWORDS_ATTR:
        raise ValidReservedNameError("'{}' is a reserved keyword by sqlite".format(name))
