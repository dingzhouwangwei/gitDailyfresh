from itsdangerous import TimedJSONWebSignatureSerializer as tj
from dailyfresh2 import settings
tt=tj(settings.SECRET_KEY,3600)
aa=b'eyJhbGciOiJIUzUxMiIsImlhdCI6MTYwMjMzNzgxMywiZXhwIjoxNjAyMzQxNDEzfQ.eyJ1c2VyX2lkIjo5fQ._akN09jGSih4ISsg8mqxkYnHgHEtDaPwQyL5z6L1jzA_XIHo12bIRvpkdhozQokpzOPQ2TtJW8Ge5A_q1ZAHSQ'
bb=tt.loads(aa)
print(bb)





