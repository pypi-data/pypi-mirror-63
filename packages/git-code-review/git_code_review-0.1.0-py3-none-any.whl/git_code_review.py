#!/usr/bin/python
""" Script for performing code reviews built into git history

Usage:

    git code-review list [ --closed ]
    git code-review open <name> <commit> <commit>
    git code-review close <name>
    git code-review view <name>

Examples:

    List open code reviews::

        git code-review list

    List closed code reviews::

        git code-review list --closed

    Open code review::

        git code-review open my-code-review HEAD~1 HEAD

    Close code review::

        git code-review close my-code-review

    View/comment on code-review:

        git code-review view my-code-review

"""
from subprocess import check_output, Popen, CalledProcessError, PIPE
from argparse import ArgumentParser
import sys
import re
import os

__VERSION__ = '0.1.0'

try:
    import msvcrt

    def getch():
        return msvcrt.getch()
except ImportError:
    import tty
    import termios

    def getch():
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

try:
    from subprocess import DEVNULL
except ImportError:
    DEVNULL = open('/dev/null')

OPEN_REVIEWS = "refs/code-reviews/open"
CLOSED_REVIEWS = "refs/code-reviews/closed"
OPEN_REVIEW_REGEX = re.compile(r"refs/code-reviews/open/([^\s]+)")
CLOSED_REVIEW_REGEX = re.compile(r"refs/code-reviews/closed/([^\s]+)")
DIFF_FILE_HEADER = re.compile(r"^diff --git a\/.* b\/(.*)$")
HUNK_HEADER = re.compile(r"\@\@ -[\d]+,([\d]+) \+[\d]+,([\d]+) \@\@")
REVIEW_TREE_REGEX = re.compile(r"040000 tree ([0-9a-f]{40})\t(.*)$")


def list_code_reviews(closed=False):
    """ Lists all th open code reviews

    Args:
        closed (bool): Whether to look for closed code reviews.
                       Defaults to false.
    """
    refs = check_output(["git", "show-ref"]).decode("utf-8")
    regex = OPEN_REVIEW_REGEX if not closed else CLOSED_REVIEW_REGEX
    reviews = regex.findall(refs)
    for name in reviews:
        print(name)


def close_code_review(name):
    """ Closes a code review

    Args:
        name (str): Name of code review to close
    """
    refhash = None
    closed_ref = "/".join([CLOSED_REVIEWS, name])
    open_ref = "/".join([OPEN_REVIEWS, name])

    proc = Popen(["git", "show-ref", "-s", open_ref],
                 stderr=DEVNULL,
                 stdout=PIPE)
    refhash = proc.communicate()[0].strip()
    if proc.returncode != 0:
        print("Code review '%s' does not exist or isn't open." % (name))
        return

    proc = Popen(["git", "update-ref", "--stdin"],
                 stderr=DEVNULL,
                 stdin=PIPE,
                 stdout=PIPE)
    open_ref = open_ref.encode("utf-8")
    closed_ref = closed_ref.encode("utf-8")
    proc.communicate(input=b"create %s %s\ndelete %s\n" % (closed_ref,
                                                           refhash,
                                                           open_ref))
    if proc.returncode == 0:
        print("Code review '%s' closed." % (name))
    else:
        print('There was a problem updating references.')


def can_run(exe):
    """ Checks if executable exists on path

    Args:
        exe (str): Name of executable
    """
    for dir in os.getenv("PATH").split(':'):
        path = os.path.join(dir, exe)
        if (os.path.exists(path)):
            return True
    return False


def prompt_for_message(prompt=None, temp_filename="INPUT-MESSAGE"):
    """ Prompts for message

    Args:
        prompt (str): Prompt to apply to message
        temp_filename (str): Name of temporary file name to use
    """
    exe = None
    if 'EDITOR' in os.environ:
        exe = os.environ.get('EDITOR')
    elif can_run('vim'):
        exe = 'vim'
    elif can_run('vi'):
        exe = 'vi'
    else:
        print('No editor seems to be available.')
        return None

    if prompt:
        with open(temp_filename, 'w') as message_file:
            for line in prompt.split('\n'):
                message_file.write("# " + line)

    if os.system("%s %s" % (exe, temp_filename)) != 0:
        return ""

    message = ""
    with open(temp_filename) as message_file:
        message = message_file.read()
    os.remove(temp_filename)

    return re.sub("#(.*)", "", message).strip()


def open_code_review(name, first, last):
    """ Opens a code review

    Args:
        name (str): Name of the code review
        start (str): First commit in series to code review
        last (Str): Last commit in series to code review
    """
    open_ref = "%s/%s" % (OPEN_REVIEWS, name)
    closed_ref = "%s/%s" % (CLOSED_REVIEWS, name)
    proc = Popen(["git", "show-ref", "-s", open_ref, closed_ref],
                 stdin=DEVNULL,
                 stdout=PIPE,
                 stderr=DEVNULL)
    proc.communicate()
    if proc.returncode == 0:
        print("Code review '%s' already exists." % (name))
        return

    description = prompt_for_message("Enter a code review description",
                                     "CODE-REVIEW-DESCRIPTION")
    if len(description) == 0:
        print('No description provided.')
        return

    proc = Popen(["git", "diff", "%s..%s" % (first, last)],
                 stderr=DEVNULL, stdout=PIPE)
    diff = proc.communicate()[0]
    filename = None
    in_hunk = False
    before_lines = 0
    after_lines = 0
    current_before_lines = 0
    current_after_lines = 0
    review_tree_proc = Popen(["git", "mktree"], stdin=PIPE,
                             stderr=DEVNULL, stdout=PIPE)
    blob_proc = None
    part = 1
    diff = diff.decode("utf-8") if type(diff) == bytes else diff
    for line in diff.split("\n"):
        if in_hunk:
            blob_proc.stdin.write(line.encode("utf-8") + b"\n")
            if line.startswith("+"):
                current_after_lines += 1
            elif line.startswith("-"):
                current_before_lines += 1
            else:
                current_before_lines += 1
                current_after_lines += 1
            if (current_before_lines == before_lines and
                    current_after_lines == after_lines):
                in_hunk = False
                blobhash = blob_proc.communicate()[0][:-1]
                proc = Popen(["git", "mktree"], stdin=PIPE,
                             stderr=DEVNULL, stdout=PIPE)
                treehash = proc.communicate(input=b"100644 blob %s\thunk\n"
                                            % (blobhash))[0][:-1]
                review_tree_proc.stdin.write(b"040000 tree %s\t%04d\n"
                                             % (treehash, part))
                part += 1
            continue

        match = DIFF_FILE_HEADER.match(line)
        if match:
            filename = match.group(1).encode("utf-8")
            continue

        match = HUNK_HEADER.match(line)
        if match:
            blob_proc = Popen(['git', 'hash-object', '-t', 'blob',
                              '-w', '--stdin'], stderr=DEVNULL,
                              stdout=PIPE, stdin=PIPE)
            before_lines, after_lines = match.groups()
            before_lines, after_lines = int(before_lines), int(after_lines)
            in_hunk = True
            current_before_lines = 0
            current_after_lines = 0
            blob_proc.stdin.write(b"Filename: %s\n\n" % (filename))
    reviewtreehash = review_tree_proc.communicate()[0].strip()
    proc = Popen(['git', 'commit-tree', reviewtreehash],
                 stderr=DEVNULL, stdout=PIPE, stdin=PIPE)
    proc.stdin.write(description.encode("utf-8"))
    commithash = proc.communicate()[0].strip()
    proc = Popen(['git', 'update-ref', open_ref, commithash],
                 stderr=DEVNULL, stdout=DEVNULL)
    proc.communicate()
    if proc.returncode == 0:
        print("Code review '%s' created." % (name))
    else:
        print("Couldn't create code '%s'. Internal error." % (name))


def view_code_review(name):
    """ Views a code review

    Args:
        name (str): Code review to view
    """
    open_ref = "%s/%s" % (OPEN_REVIEWS, name)
    proc = Popen(["git", "show-ref", "-s", open_ref], stderr=DEVNULL,
                 stdout=PIPE)
    reviewhash = proc.communicate()[0][:-1]
    if proc.returncode != 0:
        print("No open code review named '%s'" % (name))
        return

    os.system("git log %s | more" % (reviewhash))

    proc = Popen(["git", "ls-tree", reviewhash], stderr=DEVNULL, stdout=PIPE)
    reviewtree = proc.communicate()[0].strip()
    if proc.returncode != 0:
        print('Internal error.')
        return
    original_reviewtree = reviewtree
    author = None
    continue_review = True
    comments = 0
    try:
        username = check_output(["git", "config", "--get",
                                "user.name"]).strip()
        useremail = check_output(["git", "config", "--get",
                                 "user.email"]).strip()
        author = "%s<%s>" % (username, useremail)
    except CalledProcessError:
        print("Git user not configured. Commenting disabled.")
    for line in reviewtree.split('\n'):
        hunktreehash, hunkid = line.split(' ')[-1].split("\t")
        proc = Popen(["git", "ls-tree", hunktreehash],
                     stderr=DEVNULL, stdout=PIPE)
        hunktree = proc.communicate()[0].strip()
        original_hunktree = hunktree
        for line in hunktree.split('\n'):
            blobhash, blobid = line.split(' ')[-1].split("\t")
            os.system("git cat-file -p %s | more" % (blobhash))
            while True:
                if author:
                    print("(c)omment (s)kip (q)uit")
                else:
                    print("(s)kip (q)uit")

                response = getch()
                if response == "s":
                    break
                elif response == "q":
                    continue_review = False
                    break
                elif response == "c" and author:
                    message = "subject %s\n" % (blobhash)
                    message += "author %s\n\n" % (author)
                    body = prompt_for_message("Enter your comment",
                                              "CODE-COMMENT")
                    if len(body) > 0:
                        message += body
                        proc = Popen(['git', 'hash-object', '-t', 'blob',
                                     '-w', '--stdin'], stderr=DEVNULL,
                                     stdout=PIPE, stdin=PIPE)
                        hash_ = proc.communicate(input=message)[0].strip()
                        hunktree += "\n100644 blob %s\thunk-comment" % (hash_)
                        comments += 1
                        break
            if not continue_review:
                break
        if hunktree != original_hunktree:
            proc = Popen(["git", "mktree"], stderr=DEVNULL, stdout=PIPE,
                         stdin=PIPE)
            newhunktreehash = proc.communicate(input=hunktree+"\n")[0].strip()
            before = "040000 tree %s\t%s" % (hunktreehash, hunkid)
            after = "040000 tree %s\t%s" % (newhunktreehash, hunkid)
            reviewtree = reviewtree.replace(before, after)
        if not continue_review:
            break

    if reviewtree != original_reviewtree:
        proc = Popen(["git", "mktree"], stderr=DEVNULL, stdout=PIPE,
                     stdin=PIPE)
        newreviewtreehash = proc.communicate(input=reviewtree+"\n")[0].strip()
        proc = Popen(["git", "commit-tree", "-p", reviewhash,
                     newreviewtreehash], stderr=DEVNULL, stdin=PIPE,
                     stdout=PIPE)
        commithash = proc.communicate(input="Adding comments.")[0].strip()
        proc = Popen(['git', 'update-ref', open_ref, commithash],
                     stderr=DEVNULL, stdout=DEVNULL)
        proc.communicate()
    print("Finished code review.")
    print("Comments added: %d" % (comments))


def main(args=sys.argv[1:]):
    """ Command line interface entrypoint

    Args:
        args (:obj:`list`): List of arguments
    """
    parser = ArgumentParser(description='A simple git code review tool')

    subparsers = parser.add_subparsers(dest="subcommands")

    list_parser = subparsers.add_parser("list", help="List code reviews")
    list_parser.add_argument("--closed", action="store_true",
                             help="List closed reviews")

    close_parser = subparsers.add_parser("close", help="Close a code review")
    close_parser.add_argument("name", help="Code review to close.")

    open_parser = subparsers.add_parser("open", help="Open a code review")
    open_parser.add_argument("name", help="Code review to open.")
    open_parser.add_argument("first", help="First commit in series to"
                                           "code review.")
    open_parser.add_argument("last", help="Last commit in series to"
                                          "code review.")

    view_parser = subparsers.add_parser("view", help="View a code review")
    view_parser.add_argument("name", help="Code review to view.")

    args = parser.parse_args(args)
    if args.subcommands == "list":
        list_code_reviews(args.closed)
    elif args.subcommands == "close":
        close_code_review(args.name)
    elif args.subcommands == "open":
        open_code_review(args.name, args.first, args.last)
    elif args.subcommands == "view":
        view_code_review(args.name)
    else:
        parser.print_usage()


if __name__ == '__main__':
    main()
