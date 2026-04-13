from OverleafClient import OverleafClient

if __name__ =="__main__":
    client =  OverleafClient(debug=True)
    id = client.choose_project()
    client.fetch_doc(id)
    client.fetch_project(id)
    print(f"{id} fetched!")


