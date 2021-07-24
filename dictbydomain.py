#!/usr/bin/env python3
import os
import sys
import re
import argparse
from loguru import logger

def cmd_line_parser():
    """
    cmd parse
    """
    argv = sys.argv
    _ = os.path.basename(argv[0])
    usage = "python3 {} fanyi.test.com".format(__file__)
    parser = argparse.ArgumentParser(prog='dictbydomain', usage=usage)
    try:
        parser.add_argument("-u", "--url", dest="url", required=True, help="url or domain")
        parser.add_argument("-d", "--dict", dest="dict", required=False, help="merge dict")
        parser.add_argument("-o", "--output", dest="output", required=False, help="output filename")
        parser.add_argument("-p", "--prefix", dest="prefix", required=False, help="add prefix")
        args = parser.parse_args()
        return args
    except:
        raise

def save_as_file(output, datas, prefix, tmp_dict):
    if tmp_dict:
        with open(tmp_dict) as f:
            tmp_dict = f.readlines()
            datas = set(datas + tmp_dict)

    if output:
        try:
            f = open(output,"w+")
            for i in datas:
                line = prefix + i.strip() + '\n'
                logger.info(line.strip())
                f.write(line)
            logger.success("save counts: {} output_file: {}".format(len(datas), output))
        except Exception as e:
            logger.error(e)
        finally:
            f.close()
    else:
        for i in datas:
            line = prefix + i.strip()
            logger.info(line)

def main(domain):
    '''
    fanyi.test.com
    '''
    results = []
    bakext = ["rar", "zip", "tar.gz", "7z"]
    notext = ["txt", "log", "bak"]
    sqlext = ["sql"]
    other  = ["swp"]
    allext = bakext + notext + sqlext
    domain = domain.replace(".com.cn", ".comcn")
    # logger.debug(domain)

    # common
    for ext in allext:
        _ = '.'.join([domain, ext])
        results.append(_)

    domain_ = "www." + domain if "www." != domain[:4] else domain.lstrip("www.")
    for ext in allext:
        _ = '.'.join([domain_, ext])
        results.append(_)

    # split
    domain_split = domain.split(".")
    domain_split.pop() # remove suffix, such as 'com'
    # logger.debug(domain_split)
    for name in domain_split:
        _ = list(map(lambda ext:'.'.join([name,ext]), allext))
        results = results + _

    # top-level domain
    domain_split = domain.lstrip("www.").split(".")
    if len(domain_split) > 2:
        top_domain = ".".join([domain_split[-2], domain_split[-1]])
        _ = list(map(lambda ext:'.'.join([top_domain,ext]), allext))
        results = results + _

    # _ replace .
    domain_ = domain.replace(".", "_")
    for ext in allext:
        _ = '.'.join([domain_, ext])
        results.append(_)

    domain_ = domain.replace(".", "_") if "www." != domain[:4] \
            else domain.lstrip("www.").replace(".", "_")
    for ext in allext:
        _ = '.'.join([domain_, ext])
        results.append(_)

    # top-level domain, _ replace .
    domain_split = domain.lstrip("www.").split(".")
    if len(domain_split) > 2:
        top_domain = "_".join([domain_split[-2], domain_split[-1]])
        _ = list(map(lambda ext:'.'.join([top_domain,ext]), allext))
        results = results + _

    # top-level domain, _bak
    domain_split = domain.split(".")
    top_domain = domain_split[-2] + "_bak"
    _ = list(map(lambda ext:'.'.join([top_domain,ext]), allext))
    results = results + _

    results = list(map(lambda x:x.replace("comcn.", "com.cn."), results))
    # logger.debug(results)
    save_as_file(output, results, prefix, _dict)

if __name__ == '__main__':
    print('''
     _ _      _   _               _                       _       
  __| (_) ___| |_| |__  _   _  __| | ___  _ __ ___   __ _(_)_ __  
 / _` | |/ __| __| '_ \| | | |/ _` |/ _ \| '_ ` _ \ / _` | | '_ \ 
| (_| | | (__| |_| |_) | |_| | (_| | (_) | | | | | | (_| | | | | |
 \__,_|_|\___|\__|_.__/ \__, |\__,_|\___/|_| |_| |_|\__,_|_|_| |_|
v1.0                        |___/
''')
    cmd = cmd_line_parser()
    logger.info(cmd)
    domain = cmd.url.lower()
    output = cmd.output if cmd.output else None
    _dict = cmd.dict if cmd.dict else None
    prefix = cmd.prefix if cmd.prefix else ""

    r = re.findall(r"(([0-9a-z-]+\.)+[a-z]+)", domain)
    if r and len(r[0]) > 1:
        domain = r[0][0]
        results = main(domain)
    else:
        logger.error("domain invaild! ex: python3 {} fanyi.test.com".format(__file__)) 
