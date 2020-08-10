import json
import subprocess


def get_boards(pattern):
    p = subprocess.Popen(
        ['python', '-m' 'gochan_crawler.tools.cat_boards', '-p', pattern],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    (stdout, stderr) = p.communicate()

    items = []
    for item_str in stdout.decode('utf-8').strip().split('\n'):
        item = json.loads(item_str)
        items.append(item)

    return items


def get_threads(url, pattern):
    p = subprocess.Popen(
        ['python', '-m' 'gochan_crawler.tools.cat_threads', '-u', url, '-p', pattern],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    (stdout, stderr) = p.communicate()

    items = []
    for item_str in stdout.decode('utf-8').strip().split('\n'):
        item = json.loads(item_str)
        items.append(item)

    return items


def get_posts(url, pattern):
    p = subprocess.Popen(
        ['python', '-m' 'gochan_crawler.tools.cat_posts', '-u', url, '-p', pattern],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    (stdout, stderr) = p.communicate()

    items = []
    for item_str in stdout.decode('utf-8').strip().split('\n'):
        item = json.loads(item_str)
        items.append(item)

    return items


def get_drilldown(board_name, thread_title, post_message):
    p = subprocess.Popen(
        ['python', '-m', 'gochan_crawler.tools.cat_drilldown', '--board_name={:s}'.format(board_name), '--thread_title={:s}'.format(thread_title), '--post_message={:s}'.format(post_message)],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    (stdout, stderr) = p.communicate()

    items = []
    for item_str in stdout.decode('utf-8').strip().split('\n'):
        item = json.loads(item_str)
        items.append(item)

    return items
