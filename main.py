# from datetime import datetime,timedelta
# import time
# # old_now=datetime.now()

# # time.sleep(5)

# # now=datetime.now()
# # date=datetime.date(now-old_now)
# # subtract=now-old_now
# # print(subtract)
# # subtract.microseconds
# # print(subtract.microseconds)
# dt=timedelta(days=5,hours=10,minutes=15,seconds=12,milliseconds=11,microseconds=16)
# print(int(dt.total_seconds()))


# OOP

# def main():
#     return "main"

# my_func=main
# print(type(my_func))
# print(my_func())

# class Computer:

#     # attributlar
#     korpus="plastmassa"
#     tugmalar="plastmassa"
#     bios="software" 
#     holat=False
    
#     # bu oddiy funksiya faqat ushbu klass ichida ishlaydi
#     @staticmethod
#     def calculate(a,b):
#         return a+b

#     # self=o'sha classning bir obyektini o'zida qabul qiladi
#     # bu object method
#     def yoqish(self):
#         self.holat=True
#         return self.holat
    
#     def uchirish(self,vaqt:int)->bool:
#         print(vaqt," so'ng o'chadi!!!")
#         self.holat=False
#         return self.holat

# my_obj_one=Computer()

# my_obj_one.yoqish()

# my_obj_one.uchirish(60)
# my_obj_one.calculate()
# Computer.calculate()


# my_obj_one.korpus="metal"
# print(my_obj_one.holat)
# my_obj_one.yoqish()
# print(my_obj_one.holat)

# print(type(my_obj_one))
# print(my_obj_one.korpus)
# print(my_obj_one.__doc__())

# def my_update() -> None: ...

# def my_update() ->int:
#     return 123
# print(my_update())

