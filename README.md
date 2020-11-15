# Google Cloud Platformを使ったWeb API

GCPのCloud RunでPythonアプリ(tornado)をビルド，デプロイ

## FaceNet
 ### [学習済みモデル](https://drive.google.com/open?id=1EXPBSXwTaqrSC0OhUdXNmKSh9qJUQ55-)

`20180402-114759-vggface2.pt` を`./models/`にコピー

## gcloud認証
```bash
gcloud auth login
```

## Build
```sh
gcloud builds submit --tag gcr.io/[project_id]/[tag]
```

## Deploy
```sh
gcloud run deploy --image gcr.io/[project_id]/[tag] --platform managed --set-env-vars="username"="[username]","password"="[database_password]","host"="[public_ip]","database"="postgres"
```

---
## ローカルからGoogle Cloud SQLに接続
```bash
gcloud sql connect [instance-id] --user=[user_name]
```


## Licence

### [MIT](https://github.com/davidsandberg/facenet/blob/master/LICENSE.md)