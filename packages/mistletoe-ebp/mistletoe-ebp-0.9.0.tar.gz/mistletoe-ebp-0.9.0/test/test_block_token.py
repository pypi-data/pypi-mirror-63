import unittest
from unittest.mock import patch, call
from mistletoe import block_tokens, span_tokens
from mistletoe.parse_context import get_parse_context
from mistletoe.block_tokenizer import FileWrapper, tokenize_main


class TestToken(unittest.TestCase):
    def setUp(self):
        self.addCleanup(
            lambda: get_parse_context().span_tokens.__setitem__(-1, span_tokens.RawText)
        )
        patcher = patch("mistletoe.span_tokens.RawText")
        self.mock = patcher.start()
        get_parse_context().span_tokens[-1] = self.mock
        self.addCleanup(patcher.stop)

    def _test_match(self, token_cls, lines, arg, **kwargs):
        token = next(iter(tokenize_main(lines)))
        self.assertIsInstance(token, token_cls)
        self._test_token(token, arg, **kwargs)

    def _test_token(self, token, arg, **kwargs):
        for attr, value in kwargs.items():
            self.assertEqual(getattr(token, attr), value)
        self.mock.assert_any_call(arg)


class TestATXHeading(TestToken):
    def test_match(self):
        lines = ["### heading 3\n"]
        arg = "heading 3"
        self._test_match(block_tokens.Heading, lines, arg, level=3)

    def test_children_with_enclosing_hashes(self):
        lines = ["# heading 3 #####  \n"]
        arg = "heading 3"
        self._test_match(block_tokens.Heading, lines, arg, level=1)

    def test_not_heading(self):
        lines = ["####### paragraph\n"]
        arg = "####### paragraph"
        self._test_match(block_tokens.Paragraph, lines, arg)

    def test_heading_in_paragraph(self):
        lines = ["foo\n", "# heading\n", "bar\n"]
        token1, token2, token3 = tokenize_main(lines)
        self.assertIsInstance(token1, block_tokens.Paragraph)
        self.assertIsInstance(token2, block_tokens.Heading)
        self.assertIsInstance(token3, block_tokens.Paragraph)


class TestSetextHeading(TestToken):
    def test_match(self):
        lines = ["some heading\n", "---\n"]
        arg = "some heading"
        self._test_match(block_tokens.SetextHeading, lines, arg, level=2)

    def test_next(self):
        lines = ["some\n", "heading\n", "---\n", "\n", "foobar\n"]
        tokens = iter(tokenize_main(lines))
        self.assertIsInstance(next(tokens), block_tokens.SetextHeading)
        self.assertIsInstance(next(tokens), block_tokens.Paragraph)
        self.mock.assert_has_calls([call("some"), call("heading"), call("foobar")])
        with self.assertRaises(StopIteration):
            next(tokens)


class TestQuote(unittest.TestCase):
    def test_match(self):
        with patch("mistletoe.block_tokens.Paragraph"):
            token = next(iter(tokenize_main(["> line 1\n", "> line 2\n"])))
            self.assertIsInstance(token, block_tokens.Quote)

    def test_lazy_continuation(self):
        with patch("mistletoe.block_tokens.Paragraph"):
            token = next(iter(tokenize_main(["> line 1\n", "line 2\n"])))
            self.assertIsInstance(token, block_tokens.Quote)


class TestCodeFence(TestToken):
    def test_match_fenced_code(self):
        lines = ["```sh\n", "rm dir\n", "mkdir test\n", "```\n"]
        arg = "rm dir\nmkdir test\n"
        self._test_match(block_tokens.CodeFence, lines, arg, language="sh")

    def test_match_fenced_code_with_tilda(self):
        lines = ["~~~sh\n", "rm dir\n", "mkdir test\n", "~~~\n"]
        arg = "rm dir\nmkdir test\n"
        self._test_match(block_tokens.CodeFence, lines, arg, language="sh")

    def test_mixed_code_fence(self):
        lines = ["~~~markdown\n", "```sh\n", "some code\n", "```\n", "~~~\n"]
        arg = "```sh\nsome code\n```\n"
        self._test_match(block_tokens.CodeFence, lines, arg, language="markdown")

    def test_fence_code_lazy_continuation(self):
        lines = ["```sh\n", "rm dir\n", "\n", "mkdir test\n", "```\n"]
        arg = "rm dir\n\nmkdir test\n"
        self._test_match(block_tokens.CodeFence, lines, arg, language="sh")

    def test_no_wrapping_newlines_code_fence(self):
        lines = ["```\n", "hey", "```\n", "paragraph\n"]
        arg = "hey"
        self._test_match(block_tokens.CodeFence, lines, arg, language="")

    def test_unclosed_code_fence(self):
        lines = ["```\n", "hey"]
        arg = "hey"
        self._test_match(block_tokens.CodeFence, lines, arg, language="")


class TestBlockCode(TestToken):
    def test_parse_indented_code(self):
        lines = ["    rm dir\n", "    mkdir test\n"]
        arg = "rm dir\nmkdir test\n"
        self._test_match(block_tokens.BlockCode, lines, arg, language="")


class TestParagraph(TestToken):
    def test_parse(self):
        lines = ["some\n", "continuous\n", "lines\n"]
        arg = "some"
        self._test_match(block_tokens.Paragraph, lines, arg)

    def test_read(self):
        lines = ["this\n", "```\n", "is some\n", "```\n", "code\n"]
        try:
            token1, token2, token3 = tokenize_main(lines)
        except ValueError as e:
            raise AssertionError("Token number mismatch.") from e
        self.assertIsInstance(token1, block_tokens.Paragraph)
        self.assertIsInstance(token2, block_tokens.CodeFence)
        self.assertIsInstance(token3, block_tokens.Paragraph)


class TestListItem(unittest.TestCase):
    def test_parse_marker(self):
        lines = [
            "- foo\n",
            "*    bar\n",
            " + baz\n",
            "1. item 1\n",
            "2) item 2\n",
            "123456789. item x\n",
        ]
        for line in lines:
            self.assertTrue(block_tokens.ListItem.parse_marker(line))
        bad_lines = ["> foo\n", "1item 1\n", "2| item 2\n", "1234567890. item x\n"]
        for line in bad_lines:
            self.assertFalse(block_tokens.ListItem.parse_marker(line))

    def test_tokenize(self):
        lines = [" -    foo\n", "   bar\n", "\n", "          baz\n"]
        token1, token2 = next(iter(tokenize_main(lines))).children[0].children
        self.assertIsInstance(token1, block_tokens.Paragraph)
        self.assertTrue("foo" in token1)
        self.assertIsInstance(token2, block_tokens.BlockCode)

    def test_sublist(self):
        lines = ["- foo\n", "  - bar\n"]
        token1, token2 = tokenize_main(lines)[0].children[0].children
        self.assertIsInstance(token1, block_tokens.Paragraph)
        self.assertIsInstance(token2, block_tokens.List)

    def test_deep_list(self):
        lines = ["- foo\n", "  - bar\n", "    - baz\n"]
        FileWrapper(lines)
        ptoken, ltoken = tokenize_main(lines)[0].children[0].children
        self.assertIsInstance(ptoken, block_tokens.Paragraph)
        self.assertIsInstance(ltoken, block_tokens.List)
        self.assertTrue("foo" in ptoken)
        ptoken, ltoken = ltoken.children[0].children
        self.assertIsInstance(ptoken, block_tokens.Paragraph)
        self.assertTrue("bar" in ptoken)
        self.assertIsInstance(ltoken, block_tokens.List)
        self.assertTrue("baz" in ltoken)

    def test_loose_list(self):
        lines = ["- foo\n", "  ~~~\n", "  bar\n", "  \n", "  baz\n" "  ~~~\n"]
        FileWrapper(lines)
        list_item = tokenize_main(lines)[0].children[0]
        self.assertEqual(list_item.loose, False)

    def test_tight_list(self):
        lines = ["- foo\n", "\n", "# bar\n"]
        FileWrapper(lines)
        list_item = tokenize_main(lines)[0].children[0]
        self.assertEqual(list_item.loose, False)


class TestList(unittest.TestCase):
    def test_different_markers(self):
        lines = ["- foo\n", "* bar\n", "1. baz\n", "2) spam\n"]
        l1, l2, l3, l4 = tokenize_main(lines)
        self.assertIsInstance(l1, block_tokens.List)
        self.assertTrue("foo" in l1)
        self.assertIsInstance(l2, block_tokens.List)
        self.assertTrue("bar" in l2)
        self.assertIsInstance(l3, block_tokens.List)
        self.assertTrue("baz" in l3)
        self.assertIsInstance(l4, block_tokens.List)
        self.assertTrue("spam" in l4)

    def test_sublist(self):
        lines = ["- foo\n", "  + bar\n"]
        (token,) = tokenize_main(lines)
        self.assertIsInstance(token, block_tokens.List)


class TestTable(unittest.TestCase):
    def test_parse_align(self):
        test_func = block_tokens.Table.parse_align
        self.assertEqual(test_func(":------"), None)
        self.assertEqual(test_func(":-----:"), 0)
        self.assertEqual(test_func("------:"), 1)

    def test_parse_delimiter(self):
        test_func = block_tokens.Table.split_delimiter
        self.assertEqual(
            list(test_func("| :--- | :---: | ---:|\n")), [":---", ":---:", "---:"]
        )

    def test_match(self):
        lines = [
            "| header 1 | header 2 | header 3 |\n",
            "| --- | --- | --- |\n",
            "| cell 1 | cell 2 | cell 3 |\n",
            "| more 1 | more 2 | more 3 |\n",
        ]
        with patch("mistletoe.block_tokens.TableRow") as mock:
            token = next(iter(tokenize_main(lines)))
            self.assertIsInstance(token, block_tokens.Table)
            self.assertTrue(hasattr(token, "header"))
            self.assertEqual(token.column_align, [None, None, None])
            token.children
            calls = [
                call.read(line, [None, None, None], lineno=l)
                for line, l in zip(lines[:1] + lines[2:], [0, 2, 3])
            ]
            mock.assert_has_calls(calls)

    def test_easy_table(self):
        lines = ["header 1 | header 2\n", "    ---: | :---\n", "  cell 1 | cell 2\n"]
        with patch("mistletoe.block_tokens.TableRow") as mock:
            (token,) = tokenize_main(lines)
            self.assertIsInstance(token, block_tokens.Table)
            self.assertTrue(hasattr(token, "header"))
            self.assertEqual(token.column_align, [1, None])
            token.children
            calls = [
                call.read(line, [1, None], lineno=l)
                for line, l in zip(lines[:1] + lines[2:], [0, 2])
            ]
            mock.assert_has_calls(calls)

    def test_not_easy_table(self):
        lines = ["not header 1 | not header 2\n", "foo | bar\n"]
        (token,) = tokenize_main(lines)
        self.assertIsInstance(token, block_tokens.Paragraph)


class TestTableRow(unittest.TestCase):
    def test_match(self):
        with patch("mistletoe.block_tokens.TableCell") as mock:
            line = "| cell 1 | cell 2 |\n"
            result = block_tokens.TableRow.read(line)
            self.assertEqual(result.row_align, [None])
            self.assertEquals(len(result.children), 2)
            mock.assert_has_calls(
                [
                    call.read("cell 1", None, lineno=0),
                    call.read("cell 2", None, lineno=0),
                ]
            )

    def test_easy_table_row(self):
        with patch("mistletoe.block_tokens.TableCell") as mock:
            line = "cell 1 | cell 2\n"
            result = block_tokens.TableRow.read(line)
            self.assertEqual(result.row_align, [None])
            self.assertEquals(len(result.children), 2)
            mock.assert_has_calls(
                [
                    call.read("cell 1", None, lineno=0),
                    call.read("cell 2", None, lineno=0),
                ]
            )

    def test_short_row(self):
        with patch("mistletoe.block_tokens.TableCell") as mock:
            line = "| cell 1 |\n"
            result = block_tokens.TableRow.read(line, [None, None])
            self.assertEqual(result.row_align, [None, None])
            self.assertEquals(len(result.children), 2)
            mock.assert_has_calls(
                [call.read("cell 1", None, lineno=0), call.read("", None, lineno=0)]
            )


class TestTableCell(TestToken):
    def test_match(self):
        token = block_tokens.TableCell.read("cell 2", expand_spans=True)
        self._test_token(token, "cell 2", align=None)
        assert isinstance(token, block_tokens.TableCell)


class TestLinkDefinition(unittest.TestCase):
    def test_store(self):
        lines = ["[key 1]: value1\n", "[key 2]: value2\n"]
        token = block_tokens.Document.read(lines)
        self.assertEqual(
            token.link_definitions, {"key 1": ("value1", ""), "key 2": ("value2", "")}
        )


class TestDocument(unittest.TestCase):
    def test_store_link_definition(self):
        lines = ["[key 1]: value1\n", "[key 2]: value2\n"]
        document = block_tokens.Document.read(lines)
        self.assertEqual(document.link_definitions["key 1"], ("value1", ""))
        self.assertEqual(document.link_definitions["key 2"], ("value2", ""))

    def test_auto_splitlines(self):
        lines = "some\ncontinual\nlines\n"
        document = block_tokens.Document.read(lines)
        self.assertIsInstance(document.children[0], block_tokens.Paragraph)
        self.assertEqual(len(document.children), 1)


class TestThematicBreak(unittest.TestCase):
    def test_match(self):
        def test_case(line):
            token = next(iter(tokenize_main([line])))
            self.assertIsInstance(token, block_tokens.ThematicBreak)

        cases = ["---\n", "* * *\n", "_    _    _\n"]
        for case in cases:
            test_case(case)


class TestContains(unittest.TestCase):
    def test_contains(self):
        lines = ["# heading\n", "\n", "paragraph\n", "with\n", "`code`\n"]
        token = block_tokens.Document.read(lines)
        self.assertTrue("heading" in token)
        self.assertTrue("code" in token)
        self.assertFalse("foo" in token)
