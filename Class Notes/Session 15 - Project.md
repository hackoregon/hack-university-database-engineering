# Project Work

## GIT

Each GIT node is a peer.  When you execute a clone command, you are creating a new, fully-functioning node equivalent to the original node.  You can define some basic relationships between the nodes, such as telling one node what the master node is.  What this means is that that child node tracks the last time it was refreshed with the parent node and lets you sync with a slightly simpler command.

### Github

Github is an implementation of GIT with a web interface.  It also includes free hosting and a couple other goodies.  The easiest way to work with github is to have it be the parent node and have your local nodes be clones.

### Moving Changes Between Nodes

#### New Repositories

If you have enough permission to create a GIT node on a system, there are two common approaches to doing it: init and clone.  Init creates a new node with no history.  Clone takes an existing node and copies all of it's history.  All of it.

#### Existing Repositories

If you have write access on repository P and read access on repository C, you can ask C to push changes from C to P.

If you have read access on P and write access on C, you can ask C to pull changes from P.

If you don't have write access to P, but would like to get changes there, you can create a pull request specifying what changes need to happen and why.  Someone with write access to P can then accept (or deny) the pull request.  That user needs to have read access to C to be able to make the change (they won't if C is on your local machine behind a firewall).

### Strategies

Workflow

- Everyone can push
- Everyone does pull requests and one/two people accept them (the most invested people).  With this option each person can choose to use git to make the pull requests or github.
- Something creative

Github favors a strategy where each developer has a private repository on their workstation, at least one public github repository and then one of those github repositories is designated as the master.


Branching Strategies
- Branch a lot
- Branch a little
- Don't branch

More detail at https://www.git-scm.com/book/en/v2/GitHub-Contributing-to-a-Project


## Vagrant

VagrantFile can be included in git project, meaning that the source code also includes the target machine (no compatibility issues).

There are two ways to use vagrant on AWS.  The less good approach is to create a new AWS instance, connect, upload the vagrant files, and launch a virtual machine there.  The better option is to use an AWS plugin on vagrant, create a new box using the AWS provider (we've used the virtual box provider) and have vagrant setup the new instance for you.

## Data Transformations

We've got the tools to import, transform, and publish data.  We haven't spent much time talking about how to use them to make the world a better place.  Once you get some data, start by asking these questions:

1. Do I understand the data?
2. How will people want to use the data?
3. How will the data change?
4. What transformations am I capable?

## QA

What's in place to ensure that your project doesn't blow up because someone checked in incompatible code?  What are the QA rules to go with checkins/merges?

## Assignment

1. Pick a project and discuss it.  Build it.
2. Figure out how your team will share code?
3. Figure out what the environmental requirements are?
4. Make those things happen.
