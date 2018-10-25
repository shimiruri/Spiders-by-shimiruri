# Debug JavaScript for Crwaler

(1)'Sina.py'文件用于模拟登录新浪微博。
该程序中， 表单参数'su', 'servertime', 'nonce', 'rsakv', 'sp', 'prelt'都需要通过模拟JS才可以获得。
参数'su'：对用户名进行base64加密
参数'servertime', 'nonce', 'rsakv'：对参数进行搜索找到对应的请求，再构造对应的url获取响应
参数'sp'：需要上述的三个参数和一个公钥，完成对密码的rsa加密
最后通过验证用户名是否存在的方式，判断是否成功登录。

