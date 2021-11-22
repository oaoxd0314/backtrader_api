def create_model_dict(db_des,db_val):
    keys = [i[0] for i in db_des]
    values = list(db_val)
    return {key:values[int(idx)] for idx,key in enumerate(keys)}

def build_model(db_des, db_val, model):
    dict = create_model_dict(db_des,db_val)

    return model(**dict)