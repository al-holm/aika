import os
from enum import Enum
from typing import Dict, List, Tuple


class DocumentType(Enum):
    TRAJECTORY = "trajectory"
    RAG = "rag"


class DocumentHandler:
    def __init__(self, max_chunk_len: int = 700) -> None:
        self.max_chunk_len = max_chunk_len

    def load_docs(self, path: str, mode: DocumentType) -> Dict[str, List[str]]:
        docs = self.read_docs(path)
        data = self.split_docs(docs, mode)
        return data

    def read_docs(self, path: str) -> List[List[str]]:
        '''
        reads text files and markdown files from a specified directory and returns a
        list of lists containing the file extension and the file content.
        
        Parameters
        ----------
        path : str
            The `path` parameter in the `read_docs` function is a string that represents the directory path
        where the function will look for text files (`.txt`) or markdown files (`.md`) to read and process.
        
        Returns
        -------
            A list of lists is being returned. Each inner list contains two elements: the file extension
        (either "txt" or "md") and the content of the file as a string.
        
        '''
        docs = []
        for filename in os.listdir(path):
            if filename.endswith(".txt") or filename.endswith(".md"):
                file_path = os.path.join(path, filename)
                extension = filename.split(".")[-1]
                with open(file_path, "r", encoding="utf-8") as f:
                    docs.append([extension, f.read()])
        return docs

    def split_docs(
        self, docs: List[List[str]], mode: DocumentType
    ) -> Dict[str, List[str]]:
        if mode == DocumentType.TRAJECTORY:
            data = self.split_trajectories(docs)
        elif mode == DocumentType.RAG:
            data = self.split_rag(docs)
        return data

    def split_trajectories(self, docs) -> Dict[str, List[str]]:
        cat_act_list, cat_val_list, context_list, chunks_list = [], [], [], []
        for item in docs:
            text = item[1]
            chunks = text.split("---")[1:]
            for chunk in chunks:
                text = chunk.split("Category: ")[1].split("\n")
                cat_act, cat_val, context = text[0].split(", ")
                chunk = "\n".join(text[1:]).strip()
                cat_act_list.append(cat_act)
                cat_val_list.append(cat_val)
                context_list.append(context)
                chunks_list.append(chunk)
        data = {
            "cat_act": cat_act_list,
            "cat_val": cat_val_list,
            "context": context_list,
            "docs": chunks_list,
        }
        return data

    def split_rag(self, docs) -> Dict[str, List[str]]:
        src_list, chunk_list = [], []
        for item in docs:
            if item[0] == "md":
                src, chunks = self.split_rag_src_md(item[1])
            else:
                src, chunks = self.split_rag_src_txt(item[1])
            chunks = self.split_recursive(chunks)
            src_list.extend([src for _ in chunks])
            chunk_list.extend(chunks)
        data = {"source": src_list, "docs": chunk_list}
        return data

    def split_rag_src_md(self, doc):
        blocks = doc.split("\n# ")
        src = blocks[1]
        chunks = blocks[2:]
        return src, chunks

    def split_rag_src_txt(self, doc):
        src = doc.split("URL: ")[1].split("\n")[0]
        chunk = doc.split("Body Text:\n")[1].split("Related:")[0]
        chunks = [chunk.strip()]
        return src, chunks

    def split_recursive(self, chunks) -> List[str]:
        """
        recursively splits a list of strings into chunks based on a
        maximum chunk length while ensuring that the split occurs at delimiter '.'.

        Returns
        -------
            List[str] -  a list of chunks
        """
        temp = True
        while temp:
            len_chunk = len(chunks)
            new_chunks = []
            for chunk in chunks:
                if len(chunk) > self.max_chunk_len:
                    dots = [i for i, char in enumerate(chunk) if char == "."]
                    if len(dots) > 1:
                        mid = len(chunk) // 2
                        ind = min(dots, key=lambda x: abs(x - mid))
                        new_chunks.extend([chunk[: ind + 1], chunk[ind + 1 :]])
                    else:
                        new_chunks.append(chunk.strip())
                else:
                    new_chunks.append(chunk.strip())
            temp = len(new_chunks) != len_chunk
            chunks = new_chunks
        return chunks
