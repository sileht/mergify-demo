# Demo of Mergify

You can use this demo by creating pull requests.

## Use Cases

### 🔀 Automatic merge

1. Create a new file in
   [testbed](https://github.com/Mergifyio/demo/new/main/testbed) and submit a
   pull request (do not push directly!)
2. Add the ``automerge`` label.

### 🎯 Add a label on regex

1. Create a new file in
   [testbed](https://github.com/Mergifyio/demo/new/main/testbed) that contains the word **javascript** in its name and submit a
   pull request (do not push directly!)
2. The label `javascript` will be added to it.

### 👉  Flexible Assignment

1. Create a new Python file in
   [testbed](https://github.com/Mergifyio/demo/new/main/testbed) that ends up with the suffix **.py** in its name and submit a
   pull request (do not push directly!).
2. The pull request will be assigned to `another-jd`.

### 🐛 Merge Queue

1. Run the `queue-demo.py` script on your computer.
2. Two pull requests will be created and automatically queued, and then merged.
