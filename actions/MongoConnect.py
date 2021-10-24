import pymongo


def getProductDetailsFromMongo(sku):
    dbase = pymongo.MongoClient("127.0.0.1", 27017)
    db = dbase["wamia"]
    collection = db["product"]
    desc = {}
    print("Connection Successful")
    print(sku)
    for x in collection.find({"product_sku" :{ "$eq" : sku }}):
        desc = x
        print(x)

    #print("Connection closed") """collection.find({"Title" :{ "$eq" : title }}, { "_id":0}):"""
    return (desc)
    dbase.close()

def setClientInfoFromMongo(commande):
    dbase = pymongo.MongoClient("127.0.0.1", 27017)
    #print("Connection Successful")
    db = dbase["wamia"]
    collection = db["com"]
    customer = collection.insert_one(commande)
    return (commande)
    dbase.close()