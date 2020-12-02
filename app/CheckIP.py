from flask import request


class CheckIP:

    def getIp(self):
        ip: str
        if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
            ip = request.environ['REMOTE_ADDR']
        else:
            ip = request.environ['HTTP_X_FORWARDED_FOR']

        ip = ip[0:10]

        if ip == "195.220.72" or ip == "195.220.73" or ip == "195.220.74" or ip == "195.220.75" or ip == "195.220.76" \
                or ip == "195.220.77" or ip == "195.220.78":
            return True
        else:
            return False
