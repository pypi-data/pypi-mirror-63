aliyun-python-sdk-green-extension

# dependencies

* aliyun-python-sdk-core>=2.11.5
* aliyun-python-sdk-green>=3.5.0
* oss2>=2.5.0

# install

* method 1
copy source code folder of aliyunsdkgreenextension to your project

* method 2
cd aliyun-python-sdk-green-extension/
python setup.py build
python setup.py install


# usage in developing
1. import
```
from aliyunsdkgreenextension.request.extension import ClientUploader
```
2. uploader
* upload from public network
```
uploader = ClientUploader.getImageClientUploader(clt);
```

* upload from ecs internal network

```
uploader = ClientUploader.getImageClientUploader(clt, True);
```