import pytest

from darker.verification import verify_ast_unchanged, NotEquivalentError


@pytest.mark.parametrize(
    "src_lines, dst_content, expect",
    [
        (["if True: pass"], "if False: pass\n", AssertionError),
        (["if True: pass"], "if True:\n    pass\n", None),
    ],
)
def test_verify_ast_unchanged(src_lines, dst_content, expect):
    black_chunks = [(1, ["black"], ["chunks"])]
    edited_linenums = [1, 2]
    try:
        verify_ast_unchanged(src_lines, dst_content, black_chunks, edited_linenums)
    except NotEquivalentError:
        assert expect is AssertionError
    else:
        assert expect is None
