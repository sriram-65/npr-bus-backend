
def Show_Bad_Error(error_name):
    return {"Success":False , "Error":error_name}

def Show_Server_Error(error_name='Internal Server Error"'):
    return {"Success":False , "Error":error_name}

def Show_Success_Msg(msg_name ,  new , role):
    return {"Success":True , 'new':new , 'role':role, "msg":msg_name}


    