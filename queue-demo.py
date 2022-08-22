#!/usr/bin/env python3
import argparse
import random
import subprocess
import uuid
import sys

import github


def get_creds() -> str:
    cred = subprocess.Popen(
        "git credential fill",
        shell=True,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    stdout, stderr = cred.communicate(b"protocol=https\nhost=github.com")
    for line in stdout.split(b"\n"):
        if line.startswith(b"password="):
            return line.partition(b"=")[2].decode()

    raise RuntimeError("Unable to find github.com creds")


parser = argparse.ArgumentParser()
parser.add_argument("--number", "-n", help="Number of pull requests to create", default=3)
parser.add_argument("--mode", "-m", default="normal", choices=("normal", "manual", "batch", "speculative"))
args = parser.parse_args()


FLAVORS = (
    ("❄️", "snowflake"),
    ("🔥", "fire"),
    ("🧠", "brain"),
    ("🎸", "guitar"),
    ("🐸", "frog"),
    ("🐮", "cow"),
    ("☁", "cloud️"),
    ("🚲", "bike"),
)


PR_BODY = """This is just a sample pull request for demo purpose. Enjoy!

I'm a little outdated so Mergify will have to update me before merging. 😉"""


token = get_creds()

g = github.Github(token)


repo = g.get_repo("mergifyio/demo")
main = repo.get_branch(branch="main")

# get penultimate commit:
# we want to create our branch from an old commit so they are both updated for demo
base_commit = repo.get_commits(sha=main.commit.sha)[1]

for icon, flavor in random.sample(FLAVORS, k=args.number):
    head = f"{flavor}-{str(uuid.uuid4())}"
    filename = str(uuid.uuid4())
    repo.create_git_ref(f"refs/heads/{head}", base_commit.sha)  # create branch
    repo.create_file(f"testbed/queue/{args.mode}/{filename}", f"test {flavor}", flavor, branch=head)
    repo.create_pull(
        title=f"{flavor.capitalize()} pull request {icon}",
        body=PR_BODY,
        head=head,
        base="main",
    )
