#!/usr/bin/env python3
import uuid
import subprocess

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


token = get_creds()

g = github.Github(token)


repo = g.get_repo("mergifyio/demo")

main = repo.get_branch(branch="main")
head1 = "snowflake-" + str(uuid.uuid4())
head2 = "fire-" + str(uuid.uuid4())
file1 = str(uuid.uuid4())
file2 = str(uuid.uuid4())


# get penultimate commit:
# we want to create our branch from an old commit so they are both updated for demo

base_commit = repo.get_commits(sha=main.commit.sha)[1]

repo.create_git_ref(f"refs/heads/{head1}", base_commit.sha)  # create branch
repo.create_file(f"testbed/queue/{file1}", "test", "test", branch=head1)


repo.create_git_ref(f"refs/heads/{head2}", base_commit.sha)  # create branch
repo.create_file(f"testbed/queue/{file2}", "test2", "test2", branch=head2)


body = """This is just a sample pull request for demo purpose. Enjoy!

I'm a little outdated so Mergify will have to update me before merging. 😉"""

pr1 = repo.create_pull(
    title="Snowflake pull request ❄️", body=body, head=head1, base="main"
)
pr2 = repo.create_pull(title="Fire pull request 🔥", body=body, head=head2, base="main")
