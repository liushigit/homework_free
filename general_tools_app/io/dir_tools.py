# coding=utf-8

import os
import fnmatch
import datetime
import re
import zipfile
import tarfile


def gen_list_files_with_ext(ext, path):
    for p in os.listdir(path):
        if p.endswith(ext):
            yield p


def list_files_with_ext(ext, path):
    """
    Should you use glob.glob instead?
    """
    return [i for i in os.listdir(path) if i.endswith(ext)]


def list_fn_contains(pattern, path):
    return [i for i in os.listdir(path) if fnmatch.fnmatch(i, pattern)]


def list_fn_between(start_day_str, end_day_str,
                    path, ext,
                    date_pattern='\d{4}\.\d{2}\.\d{2}'):
    
    prefix = '.+?'
    interesting_part = '(' + date_pattern + ')'
    suffix = '.*\.' + ext + '$'
    pattern = prefix + interesting_part + suffix

    c = re.compile(pattern)

    out = []
    for i in os.listdir(path):
        m = c.match(i)
        if m and m.group(1) >= start_day_str and m.group(1) <= end_day_str:
            out.append(i)

    return out


def list_files_for_nearest_day(day, path, forward, ext=".png",
                               pattern_maker=lambda d: d.strftime('%Y.%m.%d')):
    """
        return a list of filenames with ^ext in ^path
        the filenames all contain a part something like yyyy*mm*dd
        if the files for the ^day don't exist, it will searching forward day by day

    """
    import copy
    day_copy = copy.copy(day)
    all_files = list_files_with_ext(ext, path)
    
    ONE_DAY = datetime.timedelta(1)
    i = 0
    while i < forward :
        glob_pattern = pattern_maker(day_copy)
        filtered = [f for f in all_files if glob_pattern in f]
        if filtered:
            break
        i += 1
        day_copy = day_copy + ONE_DAY

    filtered.insert(0, day_copy)
    return filtered


def sha1_of_dir_by_filenames(dir_name):
    import hashlib
    s = hashlib.sha1()
    for f in os.listdir(dir_name):
        s.update(f)
    return s.hexdigest()


def md5_of_dir_by_filenames(dir_name):
    import hashlib
    s = hashlib.md5()
    for f in os.listdir(dir_name):
        s.update(f)
    return s.hexdigest()


def zip_dir(src, dst):
    src = src.rstrip('/')
    root = os.path.dirname(src)
    rootlen = len(root) + 1

    with zipfile.ZipFile(dst, 'w') as myzip:
        for base, dirs, files in os.walk(src):
            for i in files:
                fn = os.path.join(base, i)
                if os.path.islink(fn):
                    f = os.readlink(fn)
                else:
                    f = fn
                myzip.write(f, fn[rootlen:])


def tar_dir(src, dst, prefix_to_trim='', ext=''):
    src = src.rstrip('/')

    if prefix_to_trim:
        rootlen = len(prefix_to_trim) + 1
    else:
        rootlen = len(os.path.dirname(src)) + 1

    with tarfile.open(dst, 'w:gz') as myzip:
        for base, dirs, files in os.walk(src):
            for i in files:
                if i.endswith(ext):
                    fn = os.path.join(base, i)
                    if os.path.islink(fn):
                        f = os.readlink(fn)
                    else:
                        f = fn
                    myzip.add(f, fn[rootlen:])


def find_top_dir(path, orig=None):
    """"
    Look into the dir, return the first level that has more that one dir 
    as its children. If there's no such sub-dir, return the path of the 
    deepest level;
    Not very useful.

    """
    # if not orig:
    #     orig = path

    list_of_dirs = [i for i in os.listdir(path) 
                        if os.path.isdir(os.path.join(path, i))]
    dirs = len(list_of_dirs)
    if dirs == 1:
        return find_top_dir(os.path.join(path, list_of_dirs[0]), orig)
    # elif dirs > 1:
    #     return path
    # else:
    #     return orig
    else:
        return path


def gen_sub_dirs(path):
    list_of_dirs = [i for i in os.listdir(path) 
                        if os.path.isdir(os.path.join(path, i))]
    for d in list_of_dirs:
        for i in gen_sub_dirs(os.path.join(path, d)):
            yield i

    if not len(list_of_dirs):
        yield path


def sub_dir_list(path):
    l = []
    for p in gen_sub_dirs(path):
        l.append(p)
    return l



# For the dara project only


def compress_sub_dirs(top_path, dst, prefix_to_trim='', ext=''):
    """
    :param dst: where the archive goes
    :returns: nothing
    """
    dir_list = sub_dir_list(top_path)
    dirs = len(dir_list)

    if prefix_to_trim:
        common_prefix = prefix_to_trim.rstrip('/') #let user decide
    elif dirs > 1:
        common_prefix = os.path.commonprefix(dir_list).rstrip('/')
    else:
        common_prefix = ''

    for d in dir_list:
        sha1 = md5_of_dir_by_filenames(d)
        tar_fn = os.path.join(dst, sha1+'.tar.gz')

        if not os.path.exists(tar_fn):
            print '{0}:{1}'.format(d, tar_fn)
            tar_dir(d, tar_fn, common_prefix, ext)
        else:
            print 'compress_sub_dirs(): File %s already exists.' % tar_fn


if __name__ == '__main__':
    pass
