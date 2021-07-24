# dictbydomain
根据URL生成强关联的目录字典

![](.\dictbydomain.png)

###### Usage

------

```python
python3 dictbydomain.py -u sub.test.com -p /
python3 dictbydomain.py -u sub.test.com -p / -o output.txt  # 保存到文件
python3 dictbydomain.py -u sub.test.com -p / -o output.txt -d db/basic.txt  # 与基础字典合并
```

###### 备注

------

目前只用来生成目录字典，目录扫描工具可以使用httpx, 如

```sh
python3 dictbydomain.py -u sub.test.com -p / -o output.txt && echo sub.test.com | httpx -status-code -content-length -paths output.txt
```
