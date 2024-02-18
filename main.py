import os
import sys
import requests
from minio import Minio
from minio.error import S3Error
from voliboli_pdf_scraper.main import process_pdf
from voliboli_sgqlc_types.main import Mutation
from sgqlc.operation import Operation

BASE = "http://voliboli-backend.voliboli.svc.cluster.local"

def store_data(team, opponent, players, date):
    mutation = Operation(Mutation)
    mutation.createTeam(name=team)
    resp = requests.post(BASE + "/teams", json={'query': str(mutation)})
    if not resp.json()["data"]["createTeam"]["success"]:
        print(resp.json()["data"]["createTeam"]["errors"])

    for p in players:
        mutation = Operation(Mutation)
        mutation.createPlayer(name=p[0], teamName=team)
        resp = requests.post(BASE + "/players", json={'query': str(mutation)})
        if not resp.json()["data"]["createPlayer"]["success"]:
            print(resp.json()["data"]["createPlayer"]["errors"])
            
        mutation = Operation(Mutation)
        mutation.updatePlayer(name=p[0],
                                votes=p[1], 
                                totalPoints=p[2],
                                breakPoints=p[3],
                                winloss=p[4],
                                totalServe=p[5],
                                errorServe=p[6],
                                pointsServe=p[7],
                                totalReception=p[8],
                                errorReception=p[9],
                                posReception=p[10],
                                excReception=p[11],
                                totalAttacks=p[12],
                                errorAttacks=p[13],
                                blockedAttacks=p[14],
                                pointsAttack=p[15],
                                posAttack=p[16],
                                pointsBlock=p[17],
                                opponent=opponent,
                                date=date)
        resp = requests.post(BASE + "/players", json={'query': str(mutation)})
        if not resp.json()["data"]["updatePlayer"]["success"]:
            sys.exit(resp.json()["data"]["updatePlayer"]["errors"])
            
if __name__ == '__main__':
    ACCESS_KEY = os.environ["MINIO_ACCESS_KEY"]
    SECRET_KEY = os.environ["MINIO_SECRET_KEY"]
    minio_client = Minio(
        "minio.minio.svc:9000",
        access_key=ACCESS_KEY,
        secret_key=SECRET_KEY,
        secure=False # NOTE: At the moment both services running on a local cluster
    )
    bucket_name = "voliboli"
    for object_name in minio_client.list_objects(bucket_name):
        print(f"Storing {object_name}...")
        try:
            data = minio_client.get_object(bucket_name, object_name)
            print(data)
            result, date, location, ateam1, ateam2, players1, players2 = process_pdf(data, debug=None)
            store_data(ateam1, ateam2, players1, date)
            store_data(ateam2, ateam1, players2, date)
        except S3Error as e:
            print(f"Error reading JSON from MinIO: {e}")
            sys.exit(1)