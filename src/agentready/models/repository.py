"""Repository model representing the target git repository being assessed."""

from dataclasses import dataclass
from pathlib import Path


@dataclass
class Repository:
    """Represents a git repository being assessed.

    Attributes:
        path: Absolute path to repository root
        name: Repository name (derived from path)
        url: Remote origin URL if available
        branch: Current branch name
        commit_hash: Current HEAD commit SHA
        languages: Detected languages with file counts (e.g., {"Python": 42})
        total_files: Total files in repository (respecting .gitignore)
        total_lines: Total lines of code
    """

    path: Path
    name: str
    url: str | None
    branch: str
    commit_hash: str
    languages: dict[str, int]
    total_files: int
    total_lines: int

    def __post_init__(self):
        """Validate repository data after initialization."""
        if not self.path.exists():
            raise ValueError(f"Repository path does not exist: {self.path}")

        if not (self.path / ".git").exists():
            raise ValueError(f"Not a git repository: {self.path}")

        if self.total_files < 0:
            raise ValueError(f"Total files must be non-negative: {self.total_files}")

        if self.total_lines < 0:
            raise ValueError(f"Total lines must be non-negative: {self.total_lines}")

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            "path": str(self.path),
            "name": self.name,
            "url": self.url,
            "branch": self.branch,
            "commit_hash": self.commit_hash,
            "languages": self.languages,
            "total_files": self.total_files,
            "total_lines": self.total_lines,
        }
