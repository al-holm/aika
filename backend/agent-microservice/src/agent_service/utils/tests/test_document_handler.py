import os
import unittest
from unittest.mock import patch, mock_open
from agent_service.utils.document_handler import DocumentHandler


class TestDocumentHandler(unittest.TestCase):
    mock_md_content = (
        "URL: http://example.com\nBody Text:\nThis is a short text. Related: None"
    )

    mock_txt_content = (
        "URL: http://example.com\nBody Text:\nThis is a short text. Related: None"
    )

    def setUp(self):
        self.document_handler = DocumentHandler(max_chunk_len=5)

    def test_recursive_split(self):
        docs = [
            "Hallo. Ich bin ein Testfall. Wie gehts dir?",
            "Wir waren im Sommer in Italien. Wir wollten nach Rom fahren.",
            "Das Wetter heute ist gut. Ich bin nicht sicher, ob mein Code funktioniert. Ich muss dafür Tests schreiben.",
        ]
        res_docs = self.document_handler.split_recursive(docs)
        expected_docs = [
            "Hallo.",
            "Ich bin ein Testfall.",
            "Wie gehts dir?",
            "Wir waren im Sommer in Italien.",
            "Wir wollten nach Rom fahren.",
            "Das Wetter heute ist gut.",
            "Ich bin nicht sicher, ob mein Code funktioniert.",
            "Ich muss dafür Tests schreiben.",
        ]
        self.assertEqual(res_docs, expected_docs)

    def test_split_rag_src_chunks_txt_single_chunk(self):
        text = (
            "URL: http://example.com\nBody Text:\nThis is a short text. Related: None"
        )
        src, chunks = self.document_handler.split_rag_src_txt(text)
        expected_src = "http://example.com"
        expected_chunks = ["This is a short text."]
        self.assertEqual(src, expected_src)
        self.assertEqual(chunks, expected_chunks)

    def test_split_rag_src_chunks_txt_no_url(self):
        text = "Body Text:\nThis is a text without a URL. Related: None"
        with self.assertRaises(IndexError):
            self.document_handler.split_rag_src_txt(text)

    def test_split_rag_src_chunks_txt_no_body_text(self):
        text = "URL: http://example.com\nRelated: None"
        with self.assertRaises(IndexError):
            self.document_handler.split_rag_src_txt(text)

    def test_split_rag_src_chunks_md_single_chunk(self):
        text = "\n# Some source\n# Text 1\n# Text 2"
        src, chunks = self.document_handler.split_rag_src_md(text)
        expected_src = "Some source"
        expected_chunks = ["Text 1", "Text 2"]
        self.assertEqual(src, expected_src)
        self.assertEqual(chunks, expected_chunks)

    def test_split_rag(self):
        docs = [
            [
                "md",
                "\n# Some source\n# Text 1. Ich gehe spazieren. Ciao, Ali.\n# Text 2",
            ],
            [
                "txt",
                "URL: http://example.com\nBody Text:\nThis is a short text. Ich gehe spazieren. Ciao, Ali. Related: None",
            ],
        ]
        data = self.document_handler.split_rag(docs)
        expected_data = {
            "source": [
                "Some source",
                "Some source",
                "Some source",
                "Some source",
                "http://example.com",
                "http://example.com",
                "http://example.com",
            ],
            "docs": [
                "Text 1.",
                "Ich gehe spazieren.",
                "Ciao, Ali.",
                "Text 2",
                "This is a short text.",
                "Ich gehe spazieren.",
                "Ciao, Ali.",
            ],
        }
        self.assertEqual(data, expected_data)

    def test_split_trajectories(self):
        text = """
---
Category: good_a, good_v, grammar
This is the first example of a trajectory.
---
Category: bad_a, good_v, situative
This is the second example of a trajectory.
"""
        docs = [["md", text]]
        data = self.document_handler.split_trajectories(docs)
        expected_data = {
            "cat_act": ["good_a", "bad_a"],
            "cat_val": ["good_v", "good_v"],
            "context": ["grammar", "situative"],
            "docs": [
                "This is the first example of a trajectory.",
                "This is the second example of a trajectory.",
            ],
        }
        self.assertEqual(data, expected_data)

    @patch("os.listdir")
    @patch("builtins.open", new_callable=mock_open)
    @patch("os.path.join", side_effect=lambda *args: "/".join(args))
    def test_read_files(self, mock_join, mock_open, mock_listdir):
        mock_listdir.return_value = ["test1.txt", "test2.md", "test3.pdf"]

        mock_file_handles = [
            mock_open(read_data="This is a test text file.").return_value,
            mock_open(read_data="# This is a test markdown file.").return_value,
            mock_open(read_data="%PDF-1.4").return_value,
        ]

        for handle in mock_file_handles:
            handle.__enter__.return_value.read.side_effect = [
                "This is a test text file.",
                "# This is a test markdown file.",
                "%PDF-1.4",
            ]

        mock_open.side_effect = mock_file_handles

        result = self.document_handler.read_docs("/fake/path")
        expected_output = [
            ["txt", "This is a test text file."],
            ["md", "# This is a test markdown file."],
        ]

        self.assertEqual(result, expected_output)
        mock_listdir.assert_called_once_with("/fake/path")
        mock_open.assert_any_call("/fake/path/test1.txt", "r", encoding="utf-8")
        mock_open.assert_any_call("/fake/path/test2.md", "r", encoding="utf-8")


if __name__ == "__main__":
    unittest.main()
