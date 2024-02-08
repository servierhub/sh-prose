import os

from prose.dao.blob.blob_repository import BlobRepository
from prose.dao.blob.commit_repository import CommitRepository
from prose.dao.blob.ref_repository import RefRepository
from prose.dao.blob.stage_repository import StageRepository
from prose.dao.blob.tree_repository import TreeRepository
from prose.domain.blob.tree import Tree


class TreeWalker:
    def __init__(self):
        self.stage_repo = StageRepository()
        self.commit_repo = CommitRepository()
        self.tree_repo = TreeRepository()
        self.blob_repo = BlobRepository()

    def cat(self, digest: str) -> None:
        print(self.blob_repo.load(digest))

    def walk(self) -> None:
        stage = self.stage_repo.load()
        if stage is None:
            return

        print("stage", stage.tree)
        print()

        root = self.tree_repo.load(stage.tree)
        if root is None:
            return

        self._walk_rec(root, "")

    def _walk_rec(self, tree: list[Tree] | None, path: str) -> None:
        if tree is not None:
            for node in tree:
                if node.type == "tree":
                    self._walk_rec(self.tree_repo.load(node.digest), os.path.join(path, node.name))
                elif node.type == "file":
                    self._walk_file(node, path)

    def _walk_file(self, file: Tree, path: str) -> None:
        comments_or_tests = self.tree_repo.load(file.digest)
        if comments_or_tests is None:
            return

        for comment_or_test in comments_or_tests:
            print(comment_or_test.type, comment_or_test.digest)
            print(f"Path: {os.path.join(path, comment_or_test.name)}")
            print()
            print(self.blob_repo.load(comment_or_test.digest))
            print()
