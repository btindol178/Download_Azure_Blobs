
import json
from flask import Flask, render_template
#https://stackoverflow.com/questions/15321431/how-to-pass-a-list-from-python-by-jinja2-to-javascript?fbclid=IwAR31QE1dkRJl9vT8MeKyB0pIJ0cNbPxuWo8J5Gw7GfVPNVeZzSfZlgG3wZU

####################################################################################################################################################################
from azure.storage.blob import BlobServiceClient


container_name = "form-recognizer"
connect_str = "<connection string> "

blob_service_client = BlobServiceClient.from_connection_string(conn_str=connect_str)

app = Flask(__name__)

@app.route('/')
def new():
    try:
        container_client = blob_service_client.get_container_client(container=container_name) # get container client to interact with the container in which images will be stored
        container_client.get_container_properties()
        print("Container Client Properties are: ",container_client.get_container_properties())

        print("Listing Blobs")
        blob_items = container_client.list_blobs()
        print("Blob items are: ",blob_items)

        bloblist =[]
        blobnames = [] 
        res = []
        for blob in blob_items:
            if 'forms/' not in blob.name: # do this because in container the first folder is forms the first file is forms/file1 example 
                print("Wrong subfolder in form-recognizer container! Pass!")
                continue
            else:
                blobname =blob.name
                blob_name = blobname.replace('forms/','')
                blob_client = container_client.get_blob_client(blob=blob.name) 
                print("The url is ",blob_client.url)
                bloblist.append(blob_client.url)
                blobnames.append(blob_name)

                res = [{blob_name:blob_client.url}] # dict needs to be in list 
                print("DICT IS ",res)
                
                print(res)
                
    except Exception as e:
        print(e)
        print("Creating container...")
        container_client = blob_service_client.create_container(container_name) # create a container in the storage account if it does not exist

    return render_template('index3.html',data=bloblist,res = res)


if __name__ == "__main__":
    app.run(debug=True)


    