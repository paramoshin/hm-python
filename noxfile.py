import tempfile

import nox
from nox.sessions import Session

nox.options.sessions = "safety", "tests"


def install_with_constraints(session, *args, with_hashes=True, **kwargs):
    cmds = [
        "poetry",
        "export",
        "--dev",
        "--format=requirements.txt",
    ]
    if not with_hashes:
        cmds.append("--without-hashes")
    with tempfile.NamedTemporaryFile() as requirements:
        cmds.append(f"--output={requirements.name}")
        session.run(*cmds, external=True)
        session.install(f"--constraint={requirements.name}", *args, **kwargs)


@nox.session(python=["3.7", "3.8"])
def safety(session):
    with tempfile.NamedTemporaryFile() as requirements:
        session.run(
            "poetry",
            "export",
            "--dev",
            "--format=requirements.txt",
            "--without-hashes",
            f"--output={requirements.name}",
            external=True,
        )
        install_with_constraints(session, "safety", with_hashes=False)
        session.run("safety", "check", f"--file={requirements.name}", "--full-report")


@nox.session(python=["3.8", "3.7"])
def tests(session):
    """Run tests"""
    args = session.posargs or ["--cov", "-m", "not e2e"]
    session.run("poetry", "install", "--no-dev", external=True)
    install_with_constraints(session, "coverage[toml]", "pytest", "pytest-cov", "pytest-mock")
    session.run("pytest", *args)
