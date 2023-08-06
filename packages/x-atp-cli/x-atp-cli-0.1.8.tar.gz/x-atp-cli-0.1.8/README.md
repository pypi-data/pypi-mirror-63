## X ATP CLI Client

X automated test platform command line client

## Sweetest of X ATP

X Sweetest is a secondary development project for [Sweetest](https://github.com/tonglei100/sweetest) according to the [Mozilla Public License Version 2.0](https://www.mozilla.org/en-US/MPL/2.0/) agreement.

Open a Cmd or Shell command window and go to the directory, for example: `D:\Autotest`, enter following command for a quick experience.

```shell
x-atp-cli -d
cd x_sweetest_example
python echo.py
```

If you have used [Sweetest](https://github.com/tonglei100/sweetest) before, just remove <del>`from sweetest import Autotest`</del> and add `from x_sweetest import Autotest` to switch to X Sweetest. for example:

```python
# from sweetest import Autotest
from x_sweetest import Autotest
import sys
......
```

### v0.1.6 change

Change content in `keywords/http.py` file to resolve issue that the `Output Data` field does not support `[{'id':1},{'id':2}]` format Json return value.

```python
        elif v == 'text':
            g.var[k] = response['text']
            logger.info('%s: %s' % (k, repr(g.var[k])))
        elif k == 'json':
            sub_str = output.get('json', '{}')
            if sub_str[0] == '[':
                index = sub_str.split(']')[0][1:]
                sub = json2dict(sub_str[len(index)+2:])
                result = check(sub, response['json'][int(index)])
            else:
                sub = json2dict(output.get('json', '{}'))
                result = check(sub, response['json'])
            # logger.info('Compare json result: %s' % result)
            var = dict(var, **result['var'])
            g.var = dict(g.var, **result['var'])
            logger.info('json var: %s' % (repr(result['var'])))
```

An example of editing the `Output Data` field of `-TestCase.xlsx` is as follows:

 - `json=[0]{'id':'<id1>'}`
 - `json=[-1]{'id':'<id2>'}`

### v0.1.7 change

Change the content in the `keywords/http.py` file, add `form` usage in `Test Data` to optimize the writing format of the import file function in the `-TestCase.xlsx` field.

```python
    if kw == 'get':
        r = getattr(http.r, kw)(http.baseurl + url,
                                params=_data['params'], timeout=timeout, **data)
        if _data['params']:
            logger.info(f'PARAMS: {_data["params"]}')

    elif kw == 'post':
        if 'form' in data:
            form_dict = json2dict(data['form'])
            try:
                if len(form_dict) == 1:
                    for form_k, form_v in form_dict.items():
                        form_name = form_k.split("/")[-1]
                form_data = MultipartEncoder(fields={'file': (form_name, open(form_k, 'rb'), form_v)})
                form_headers = {'Content-Type': form_data.content_type}
                http.r.headers.update(form_headers)
                r = getattr(http.r, kw)(http.baseurl + url, data=form_data, timeout=timeout)
            except:
                logger.exception("***form can be only one Key-value***")
        else:
            r = getattr(http.r, kw)(http.baseurl + url,
                                    data=_data['data'], json=_data['json'], files=_data['files'], timeout=timeout, **data)
        logger.info(f'BODY: {r.request.body}')

    elif kw in ('put', 'patch'):
        r = getattr(http.r, kw)(http.baseurl + url,
                                data=_data['data'], timeout=timeout, **data)
        logger.info(f'BODY: {r.request.body}')
```

An example of editing the `Test Data` field of `-TestCase.xlsx` is as follows:

 - `form={r'./files/test.xls': 'application/vnd.ms-excel'}`
 - `form={r'./files/test.zip': 'application/zip}`
