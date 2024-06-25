import sys, os
testdir = os.path.dirname(__file__)
sys.path.insert(0, os.path.abspath(os.path.join(testdir, '../../../')))
from agent_service.rag.rag import RAG
import unittest
from unittest.mock import patch, mock_open, MagicMock

class TestRAG(unittest.TestCase):

    def setUp(self):
        self.rag = RAG(init=False, llm='bedrock', test=True)
        self.rag.max_chunk_len = 50


    def test_get_src_chunks_txt_complex_split(self):
        text = ("URL: http://example.com\nBody Text:\nThis is a complex text. It contains several sentences. "
                "Each sentence should be handled properly. The splitting logic must find the closest period. "
                "This ensures that we do not split mid-sentence. Related: None")
        src, chunks = self.rag.get_src_chunks_txt(text)
        expected_src = ["http://example.com", "http://example.com", "http://example.com", "http://example.com", "http://example.com"]

        expected_chunks = ["This is a complex text.",
                           ' It contains several sentences.',
                           ' Each sentence should be handled properly.',
                           ' The splitting logic must find the closest period.',
                           " This ensures that we do not split mid-sentence."]
        self.assertEqual(chunks, expected_chunks)
        self.assertEqual(src, expected_src)

    def test_read_markdown_folder(self):
        test_dir = 'test_md_folder'
        os.makedirs(test_dir, exist_ok=True)
        with open(os.path.join(test_dir, 'file1.md'), 'w') as f:
            f.write('sample markdown text 1')
        with open(os.path.join(test_dir, 'file2.md'), 'w') as f:
            f.write('sample markdown text 2')

        result = self.rag.read_markdown_folder(test_dir)
        self.assertEqual(result, ['sample markdown text 1', 'sample markdown text 2'])

        os.remove(os.path.join(test_dir, 'file1.md'))
        os.remove(os.path.join(test_dir, 'file2.md'))
        os.rmdir(test_dir)

    def test_read_txt_folder(self):
        test_dir = 'test_txt_folder'
        os.makedirs(test_dir, exist_ok=True)
        with open(os.path.join(test_dir, 'file1.txt'), 'w') as f:
            f.write('sample text content 1')
        with open(os.path.join(test_dir, 'file2.txt'), 'w') as f:
            f.write('sample text content 2')

        result = self.rag.read_txt_folder(test_dir)
        self.assertEqual(result, ['sample text content 1', 'sample text content 2'])

        os.remove(os.path.join(test_dir, 'file1.txt'))
        os.remove(os.path.join(test_dir, 'file2.txt'))
        os.rmdir(test_dir)

    def test_parse_info_md(self):
        text_list = ["\n# Title\n# Section 1\nContent 1", "\n# Title\n# Section 2\nContent 2"]
        src, docs = self.rag.parse_info(text_list, mode="md")
        self.assertEqual(src, ["Title", "Title"])
        self.assertEqual(docs, ["Section 1\nContent 1", "Section 2\nContent 2"])

    def test_parse_info_txt(self):
        text_list = ["URL: http://example.com\nBody Text:\nContent 1\nRelated:"]
        src, docs = self.rag.parse_info(text_list, mode="txt")
        self.assertEqual(src, ["http://example.com"])
        self.assertEqual(docs, ["Content 1"])

    def test_load_docs(self):
        test_dir = 'test_load_docs_folder'
        os.makedirs(test_dir, exist_ok=True)
        with open(os.path.join(test_dir, 'file1.md'), 'w') as f:
            f.write('\n# sample src\n# markdown text 1')
        with open(os.path.join(test_dir, 'file2.txt'), 'w') as f:
            f.write('URL: http://example.com\nBody Text:\nsample text content 2\nRelated:')

        self.rag.DOC_PATH = test_dir
        self.rag.load_docs()

        self.assertEqual(self.rag.list_docs, ['markdown text 1', 'sample text content 2'])
        self.assertEqual(self.rag.list_src, ['sample src', 'http://example.com'])

        os.remove(os.path.join(test_dir, 'file1.md'))
        os.remove(os.path.join(test_dir, 'file2.txt'))
        os.rmdir(test_dir)

    def test_get_src_chunks_txt_single_chunk(self):
        text = "URL: http://example.com\nBody Text:\nThis is a short text. Related: None"
        src, chunks = self.rag.get_src_chunks_txt(text)
        expected_src = ["http://example.com"]
        expected_chunks = ["This is a short text."]
        self.assertEqual(src, expected_src)
        self.assertEqual(chunks, expected_chunks)

    def test_get_src_chunks_txt_multiple_chunks(self):
        text = ("URL: http://example.com\nBody Text:\nThis is a longer text. It should be split into multiple chunks. "
                "This is additional content to ensure splitting. Related: None")
        src, chunks = self.rag.get_src_chunks_txt(text)
        expected_src = ["http://example.com", "http://example.com", "http://example.com"]
        expected_chunks = ["This is a longer text.", ' It should be split into multiple chunks.',
                           " This is additional content to ensure splitting."]
        self.assertEqual(src, expected_src)
        self.assertEqual(chunks, expected_chunks)

    def test_get_src_chunks_txt_no_url(self):
        text = "Body Text:\nThis is a text without a URL. Related: None"
        with self.assertRaises(IndexError):
            self.rag.get_src_chunks_txt(text)

    def test_get_src_chunks_txt_no_body_text(self):
        text = "URL: http://example.com\nRelated: None"
        with self.assertRaises(IndexError):
            self.rag.get_src_chunks_txt(text) 
if __name__ == '__main__':
    unittest.main()