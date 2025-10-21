from db.db import ADMIN_EMAILS

def JSON_Parser(mongodb_cursor):
    try:
        data = []
        for i in mongodb_cursor:
            i['_id'] = str(i['_id'])
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



