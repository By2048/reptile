FROM python
COPY requirements_dev.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
VOLUME ["/home/mzitu","/home/bing","/home/wallpaper"]