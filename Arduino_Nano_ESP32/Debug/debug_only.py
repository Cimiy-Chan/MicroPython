import math

a=7.8
print (math.trunc(a))

a = 68
#a_10 = math.trunc(a/10)
a_10=int(a/10.0)
b = a/10.0

a_1=int((b-int(b))*10+ 0.001)
#a_1 = b- int(b)

print (a_10, a_1)

