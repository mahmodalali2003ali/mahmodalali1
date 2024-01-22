# استيراد الوحدات اللازمة
from typing import Union
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


import sqlite3

# إنشاء تطبيق FastAPI
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# تعريف نقطة الوصول "/get" باستخدام الزر (GET) لاسترجاع جميع المنتجات
@app.get("/")
def getmedicine():
    # الاتصال بقاعدة البيانات SQLite
    conn = sqlite3.connect("reper.db")
    # استعلام SQL لاسترجاع جميع البيانات من جدول reper
    sql = "select * from reper"
    curs = conn.execute(sql)
    # استرجاع جميع الصفوف كقائمة من التفاصيل
    lst = curs.fetchall()
    # إعداد قائمة لتخزين بيانات المنتجات
    array = []
    # حلقة عبر الصفوف المسترجعة وتحويلها إلى هيكل بيانات محدد
    for i in lst:
        item = {}
        item["ExpDate"] = i[0]
        item["Qty"] = i[1]
        item["Product"] = i[2]
        item["source"] = i[3]
        item["OnHand"] = i[4]
        item["id"] = i[5]
        # إضافة هيكل البيانات إلى القائمة
        array.append(item)
    # إغلاق اتصال قاعدة البيانات
    conn.close()
    # إرجاع البيانات كقائمة
    return array

# استدعاء الدالة getproduct
getmedicine()


@app.post("/insert")
def insertmedicine(ExpDate: str, Qty: int, Product: str, source: str, OnHand: int):
    conn = sqlite3.connect("reper.db")
    # تعديل الاستعلام ليتناسب مع عدد الأعمدة في الجدول
    sql = "insert into reper(ExpDate, Qty, Product, source, OnHand) values ('{}', {}, '{}', '{}', {})".format(ExpDate, Qty, Product, source, OnHand)
    conn.execute(sql)
    conn.commit()
    conn.close()
    return {"status": " reper added in database"}


# تعريف نقطة الوصول "/updateProduct" باستخدام الزر (PUT) لتحديث بيانات المنتج
@app.put("/update")
def updatemedicine(ExpDate: str, Qty: int, Product: str, source: str, id: int):
    conn = sqlite3.connect("reper.db")
    # تحديث بيانات المنتج في جدول reper بناءً على الهوية (id)
    sql = "update reper set ExpDate='{}',Qty={} where id={} ".format(ExpDate, Qty, id)
    conn.execute(sql)
    conn.commit()
    conn.close()
    return {"status": "updated medicine on database"}

# تعريف نقطة الوصول "/deletemedicine" باستخدام الزر (DELETE) لحذف بيانات المنتج
@app.delete("/deletemedicine")
def deletemedicine(id: int):
    conn = sqlite3.connect("reper.db")
    # حذف بيانات المنتج من جدول reper بناءً على الهوية (id)
    sql = "delete from reper where id={}".format(id)
    conn.execute(sql)
    conn.commit()
    conn.close()
    return {"status": "delete medicine on database"}
# uvicorn text:app --host 0.0.0.0 --port 8000
# uvicorn text:app --reload
