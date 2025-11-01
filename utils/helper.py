from db.db import ADMIN_EMAILS
import cloudinary
import cloudinary.uploader

cloudinary.config(
     cloud_name="dbrmvywb0",
    api_key="799647841433247",
    api_secret="XLtCOYXxRTnjZqwaF2oFnQ0AK7k"
)


def JSON_Parser(mongodb_cursor):
    try:
        data = []
        for i in mongodb_cursor:
            i['_id'] = str(i['_id'])
            i['created_at'] = str(i['created_at'])
            data.append(i)
        
        return data
    except:
        return False



def Check_Role(email):
    try:
        ADMINS = ADMIN_EMAILS.find_one({"admin_email":email})
        ADMINS["_id"] = str(ADMINS['_id'])
        if ADMINS:
            return {"yes":True , 'admin_data':ADMINS }
        return {"yes":False}
    except:
        return {"yes":False}



def Filter_Options(dep , year , gender , busno , date):
    try:
        vars = {"dep":dep , "year":year, "gender":gender , "date":date , "busno":busno}
        query = {}
        for key , value in vars.items():
            if value == 'all':
                pass
            else:
                query[key] = value
        
        return query
    except:
        return False


def Upload_Profile(img_url):
    try:
        img = cloudinary.uploader.upload(img_url)
        if img:
            return img['secure_url']
        else:
            return False
    except:
        return False

