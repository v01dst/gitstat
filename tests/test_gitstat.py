import unittest
import os
import sys
import io
from contextlib import redirect_stdout
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from gitstat import git, cmd_stats, cmd_contributors


class TestGit(unittest.TestCase):
    def test_git_log(self):
        out = git(["log", "--oneline"])
        self.assertIsInstance(out, str)

    def test_stats(self):
        buf = io.StringIO()
        with redirect_stdout(buf):
            cmd_stats(type("A", (), {})())
        out = buf.getvalue()
        self.assertIn("commits:", out)
        self.assertIn("files:", out)


class TestContributors(unittest.TestCase):
    def test_contributors(self):
        import subprocess
        # create a temp git repo with a commit
        d = os.path.join(os.path.dirname(__file__), "tmprepo")
        os.makedirs(d, exist_ok=True)
        subprocess.run(["git", "init"], cwd=d, capture_output=True)
        subprocess.run(["git", "config", "user.email", "test@test.com"], cwd=d, capture_output=True)
        subprocess.run(["git", "config", "user.name", "tester"], cwd=d, capture_output=True)
        with open(os.path.join(d, "f.txt"), "w") as fh:
            fh.write("x")
        subprocess.run(["git", "add", "."], cwd=d, capture_output=True)
        subprocess.run(["git", "commit", "-m", "init"], cwd=d, capture_output=True)
        old = os.getcwd()
        os.chdir(d)
        try:
            buf = io.StringIO()
            with redirect_stdout(buf):
                cmd_contributors(type("A", (), {})())
            out = buf.getvalue()
            self.assertIn("tester", out)
        finally:
            os.chdir(old)
            import shutil
            shutil.rmtree(d, ignore_errors=True)


if __name__ == "__main__":
    unittest.main()
